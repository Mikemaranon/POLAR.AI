# web_server/cli_m/cli_manager.py

import threading
from data_m import get_command

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
            return None, None, [], "[CLI_MANAGER] Petition is not valid, must have a command"

        command_id = parts[0]
        subcommand = parts[1]
        args = parts[2:]
        return command_id, subcommand, args, None

    def load_command_metadata(self, command_id: str):
        cmd_data = get_command(command_id)
        if not cmd_data:
            return None, f"[CLI_MANAGER] Command '{command_id}' not found."
        return cmd_data, None
    
    def validate_subcommand(self, cmd_data: dict, subcommand: str, args_list: list):
        subcommands = cmd_data.get("sub_commands", {})
        if subcommand not in subcommands:
            return None, None, f"[CLI_MANAGER] Subcommand '{subcommand}' not found."

        sub_meta = subcommands[subcommand]
        args_spec = sub_meta.get("args", {})
        if not args_spec:
            return sub_meta, {}, None  # no expected args, return empty dict

        # parse args like a shell command
        parsed_args, error = CliManager.parse_named_args(args_list)
        if error:
            return None, None, error

        # validate required arguments
        missing = [
            flag for flag, requirement in args_spec.items()
            if requirement == "required" and flag not in parsed_args
        ]
        if missing:
            return None, None, f"[CLI_MANAGER] missing arguments are required : {missing}"

        # return valid args
        kwargs = {k: v for k, v in parsed_args.items() if k in args_spec}
        return sub_meta, kwargs, None
    
    def import_command_module(self, module_name: str, command_id: str):
        try:
            module = __import__(f"cli_m.commands.{module_name}.{command_id}", fromlist=[command_id])
            return module, None
        except ModuleNotFoundError:
            return None, f"[CLI_MANAGER] File '{command_id}.py' not found in module '{module_name}'."
        except Exception as e:
            return None, f"[CLI_MANAGER] Error importing module: {e}"

    def get_command_function(self, module, sub_meta: dict, subcommand: str, command_id: str):
        function_name = sub_meta.get("function")
        if not function_name:
            return None, f"[CLI_MANAGER] Subcommand '{subcommand}' has no assigned method."

        try:
            func = getattr(module, function_name)
            return func, None
        except AttributeError:
            return None, f"[CLI_MANAGER] Method '{function_name}' not found in file '{command_id}.py'."

    def execute_command_function(self, func, user_context: dict, kwargs: dict, function_name: str):
        try:
            return func(user_context, **kwargs)
        except Exception as e:
            return f"[CLI_MANAGER] Error running '{function_name}': {e}"


    # ||======================================================================||
    # ||                      CLI MANAGER MAIN METHOD                         ||
    # ||======================================================================||

    def process_command(self, command_str: str, user_context: dict):
        # step 1: parse the command input
        command_id, subcommand, args, error = self.parse_command_input(command_str)
        if error:
            return error

        # step 2: obtain command metadata
        cmd_data, error = self.load_command_metadata(command_id)
        if error:
            return error
        
        # sep 3: validate the subcommand and its arguments
        sub_meta, kwargs, error = self.validate_subcommand(cmd_data, subcommand, args)
        if error:
            return error
        
       # step 4: import the module
        module, error = self.import_command_module(cmd_data["module"], command_id)
        if error:
            return error

        # step 5: get the function
        func, error = self.get_command_function(module, sub_meta, subcommand, command_id)
        if error:
            return error

        # step 6: execute it
        return self.execute_command_function(func, user_context, kwargs, func.__name__)