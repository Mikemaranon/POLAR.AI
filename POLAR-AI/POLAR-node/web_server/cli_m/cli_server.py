import sys
from cli_m.cli_manager import CliManager
from colorama import Fore, Style, init

init(autoreset=True)

class CliServer:
    def __init__(self):
        self.cli = CliManager()
        self.user_context = {
            "username": "cli_admin",
            "level": 4  # default admin level
        }

    def start(self):
        print(Fore.CYAN + "\n╔══════════════════════════════════════════════╗")
        print("║        Welcome to POLAR Node CLI Shell       ║")
        print("╚══════════════════════════════════════════════╝\n")
        print("type 'exit' to close session.\n")


        # TODO: change all the bellow content
        while True:
            try:
                command = input(Fore.GREEN + "> " + Style.RESET_ALL).strip()
                if not command:
                    continue
                if command.lower() in ("exit"):
                    print(Fore.YELLOW + "exiting...\n")
                    break

                result = self.cli.process_command(command, self.user_context)
                print(result)

            except KeyboardInterrupt:
                print(Fore.YELLOW + "\n[!] Ctrl+C detected. Closing...\n")
                break
            except EOFError:
                print(Fore.YELLOW + "\n[!] Ctrl+D detected. Closing...\n")
                break
            except Exception as e:
                print(Fore.RED + f"[CLI ERROR] unexpected exception: {e}")
