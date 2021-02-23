from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    number_strings = [str(i) for i in range(0, 99000, 500)]
    return "\n".join(number_strings)
