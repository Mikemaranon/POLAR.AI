from data_m import get_command

class CliManager:
    def __init__(self):
        self.initiated = True

    # ||========================================================================================||
    # ||                          CLI MANAGER METHODS                                           ||           
    # ||                                                                                        ||                          
    # ||        [parse_command_input]       parse the command input string                      ||
    # ||        [load_command_metadata]     load command metadata from the database             ||  
    # ||        [validate_subcommand]       validate the subcommand and its arguments           ||
    # ||        [process_command]           process the command input and return the result     ||
    # ||========================================================================================||

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
        
        # TODO [abstract into method] step 4: dynamically import the command module
        module_name = cmd_data["module"]  # ej: user_commands
        try:
            module = __import__(f"cli_m.commands.{module_name}.{command_id}", fromlist=[command_id])
        except ModuleNotFoundError:
            return f"[CLI_MANAGER] File '{command_id}.py' not found in module '{module_name}'."
        except Exception as e:
            return f"[CLI_MANAGER] Error importing module: {e}"
        
         # TODO [abstract into method] step 5: get the function to execute
        function_name = sub_meta.get("function")
        if not function_name:
            return f"[CLI_MANAGER] Subcomand '{subcommand}' has no assigned method."

        try:
            func = getattr(module, function_name)
        except AttributeError:
            return f"[CLI_MANAGER] method '{function_name}' not found in file '{command_id}.py'."

        # TODO [abstract into method] step 6: execute the function with the arguments and user context
        try:
            result = func(user_context, **kwargs)
            return result
        except Exception as e:
            return f"[CLI_MANAGER] Error running '{function_name}': {e}"