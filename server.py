#!/usr/bin/python
# -*- coding: utf-8 -*-

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
    messages.append('you: ' + text)
    response = mark.main(text)
    messages.append('ගුණේ: '.decode('utf-8') + response)
    return render_template("index.html", data=messages)

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
