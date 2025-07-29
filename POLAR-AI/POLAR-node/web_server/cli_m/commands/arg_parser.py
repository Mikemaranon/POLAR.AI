def extract_arguments(args_list, arg):
    if isinstance(args_list, dict) and arg in arg:
        value = args_list[arg]
        return value
    return None