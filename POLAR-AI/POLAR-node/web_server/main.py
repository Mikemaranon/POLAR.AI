from flask import Flask
import sys
import threading
from cli_m.cli_server import CliServer
import server 

app = Flask(__name__, template_folder='../web_app', static_folder='../web_app/static')

def run_flask():
    print("||=================================||")
    print("||       Starting NODE server      ||")
    print("||=================================||")
    server = server.Server(app)
    app.run(host="0.0.0.0", port=5000)

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
    cli_thread = threading.Thread(target=run_cli, daemon=False)
    cli_thread.start()

    # The main thread waits for both to finish
    flask_thread.join()
    cli_thread.join()