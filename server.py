from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)
messages = []

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def process():
    text = request.form['text']
    messages.append(text)
    return render_template("index.html", data=messages)

if __name__ == "__main__":
    app.run()