#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
import os
import json
import markov

app = Flask(__name__)
messages = []

mark = markov.Markov()

@app.route("/")
def main():
    return render_template("index.html", data=messages)

@app.route('/chat', methods=['POST'])
def process():
    data = json.loads(request.data)
    text = data['text']
    response = mark.main(text)
    response = 'ගුණේ: '.decode('utf-8') + response
    response = {'response': response}
    return jsonify(**response)

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
