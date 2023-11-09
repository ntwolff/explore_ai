from flask import Flask
from assistant_interactor import assist

app = Flask(__name__)

# Home page
@app.route("/")
def info():
    return "<p>openai assistant - function calling demo</p>"

# Start the chat
@app.route("/start")
def start_assisting():
    # TODO
    # assist()

# Stop the chat
@app.route("/stop")
def stop_assisting():
    # TODO