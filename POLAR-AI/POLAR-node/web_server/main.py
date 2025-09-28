# POLAR-AI/POLAR-node/web_server/main.py

from flask import Flask
import threading
from cli_m.cli_server import CliServer
from flask_server import Server

app = Flask(__name__, template_folder='../web_app', static_folder='../web_app/static')

def run_flask():
    print("||=================================||")
    print("||       Starting NODE server      ||")
    print("||=================================||")
    Server(app)

def run_cli():
    print("||=================================||")
    print("||       Starting CLI server       ||")
    print("||=================================||")
    cli = CliServer()
    cli.start()

if __name__ == "__main__":
    # Thread for Flask, daemon so it closes with the main process
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Thread for CLI, also as daemon or not depending on whether you want it to close with the process
    cli_thread = threading.Thread(target=run_cli, daemon=True)
    cli_thread.start()

    # The main thread waits for both to finish
    flask_thread.join()
    cli_thread.join()