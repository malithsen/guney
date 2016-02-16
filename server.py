from flask import Flask
from flask import request
from flask import render_template
import markov

app = Flask(__name__)
messages = []

mark = markov.Markov()

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def process():
    text = request.form['text']
    messages.append(text)
    response = mark.main(text)
    messages.append(response)
    return render_template("index.html", data=messages)

if __name__ == "__main__":
    app.debug = True
    app.run()