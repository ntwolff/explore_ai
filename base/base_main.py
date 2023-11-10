from flask import Flask

app = Flask(__name__)

# Home page
@app.route("/")
def info():
    return "<p>OpenAI Assistant - Function Calling Demo</p>"