# web_server/cli_m/cli_manager.py

import threading
from data_m.database import Database

class CliManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(CliManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initiated') and self.initiated:
            return
        self.initiated = True
        self.get_command = Database().t_commands.get_command  # alias for easier access


    # ||================================================================================================||
    # ||                          CLI MANAGER METHODS                                                   ||           
    # ||                                                                                                ||                          
    # ||        [parse_command_input]       parse the command input string                              ||
    # ||        [load_command_metadata]     load command metadata from the database                     ||  
    # ||        [validate_subcommand]       validate the subcommand and its arguments                   ||
    # ||        [process_command]           process the command input and return the result             ||
    # ||        [import_command_module]     dynamically import the module containing the command        ||
    # ||        [get_command_function]      get the function object for the subcommand                  ||
    # ||        [execute_command_function]  execute the resolved function with given arguments          ||
    # ||================================================================================================||

    def parse_command_input(self, command_str: str):
        parts = command_str.strip().split()
        if len(parts) < 2:
            print("[ERROR - CLI_MANAGER] Invalid command format. Expected 'command_id subcommand [args]'.")
            return None, None, [], "Invalid command format. Expected 'command_id subcommand [args]'."

        command_id = parts[0]
        subcommand = parts[1]
        args = parts[2:]
        return command_id, subcommand, args, None

    def load_command_metadata(self, command_id: str):
        cmd_data = self.get_command(command_id)
        if not cmd_data:
            print(f"[ERROR - CLI_MANAGER] Command '{command_id}' not found.")
            return None, f"Command '{command_id}' not found."
        return cmd_data, None
    
    def validate_subcommand(self, cmd_data: dict, subcommand: str, args_list: list):
        subcommands = cmd_data.get("sub_commands", {})
        if subcommand not in subcommands:
            print(f"[ERROR - CLI_MANAGER] Subcommand '{subcommand}' not found in command '{cmd_data['id']}'.")
            return None, None, f"Subcommand '{subcommand}' not found in command '{cmd_data['id']}'."

        sub_meta = subcommands[subcommand]
        args_spec = sub_meta.get("args", {})

        if not args_spec:
            if args_list:
                return None, None, f"This subcommand does not accept arguments, but got: {args_list}"
            return sub_meta, {}, None

        # Parse args
        parsed_args, error = self.parse_named_args(args_list)
        if error:
            return None, None, error

        # Validate unknown args
        invalid_args = [arg for arg in parsed_args if arg not in args_spec]
        if invalid_args:
            print(f"[ERROR - CLI_MANAGER] Invalid arguments: {', '.join(invalid_args)}")
            return None, None, f"Invalid arguments: {invalid_args}"

        # Validate missing required args
        missing = [
            flag for flag, requirement in args_spec.items()
            if requirement == "required" and flag not in parsed_args
        ]
        if missing:
            print(f"[ERROR - CLI_MANAGER] Missing required arguments: {', '.join(missing)}")
            return None, None, f"Missing required arguments: {missing}"

        return sub_meta, parsed_args, None  # return args as a dictionary

    def parse_named_args(self, args_list: list):
        parsed = {}
        i = 0
        while i < len(args_list):
            arg = args_list[i]
            if arg.startswith("-") and len(arg) > 1:
                key = arg[1:]
                if i + 1 < len(args_list) and not args_list[i + 1].startswith("-"):
                    parsed[key] = args_list[i + 1]
                    i += 2
                else:
                    parsed[key] = True # flag without value
                    i += 1
            else:
                print(f"[WARNING - CLI_MANAGER] Ignored unrecognized argument: {arg}")
                i += 1
        return parsed, None
    
    def import_command_module(self, module_name: str, command_id: str):
        try:
            module = __import__(f"cli_m.commands.{module_name}.{command_id}", fromlist=[command_id])
            return module, None
        except ModuleNotFoundError:
            print(f"[ERROR - CLI_MANAGER] File '{command_id}.py' not found in module '{module_name}'.")
            return None, f"File '{command_id}.py' not found in module '{module_name}'."
        except Exception as e:
            print(f"[ERROR - CLI_MANAGER] Error importing module '{module_name}.{command_id}': {e}")
            return None, f"Error importing module: {e}"

    def get_command_function(self, module, sub_meta: dict, subcommand: str, command_id: str):
        function_name = sub_meta.get("function")
        if not function_name:
            print(f"[ERROR - CLI_MANAGER] Subcommand '{subcommand}' has no assigned method.")
            return None, f"Subcommand '{subcommand}' has no assigned method."

        try:
            func = getattr(module, function_name)
            return func, None
        except AttributeError:
            print(f"[ERROR - CLI_MANAGER] Method '{function_name}' not found in file '{command_id}.py'.")
            return None, f"Method '{function_name}' not found in file '{command_id}.py'."

    def execute_command_function(self, func, user_context: dict, kwargs: dict, function_name: str):
        try:
            return func(arg=kwargs, user_context=user_context)
        except Exception as e:
            print(f"[ERROR - CLI_MANAGER] Error running '{function_name}': {e}")
            return f"Error running '{function_name}': {e}"


    # ||======================================================================||
    # ||                      CLI MANAGER MAIN METHOD                         ||
    # ||======================================================================||

    def process_command(self, command_str: str, user_context: dict):
        # step 1: parse the command input
        command_id, subcommand, args, error = self.parse_command_input(command_str)
        if error:
            return "No input", error

        # step 2: obtain command metadata
        cmd_data, error = self.load_command_metadata(command_id)
        if error:
            return "Unknown command", error
        
        # sep 3: validate the subcommand and its arguments
        sub_meta, kwargs, error = self.validate_subcommand(cmd_data, subcommand, args)
        if error:
            return "subcomand or args not found", error
        
       # step 4: import the module
        module, error = self.import_command_module(cmd_data["module"], command_id)
        if error:
            return "module error", error

        # step 5: get the function
        func, error = self.get_command_function(module, sub_meta, subcommand, command_id)
        if error:
            return "execution error", error

        # step 6: execute it
        return self.execute_command_function(func, user_context, kwargs, func.__name__), None