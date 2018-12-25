#!/usr/bin/env python
# -*- coding:utf-8 -*-
import flask

app = flask.Flask(__name__)

@app.route("/")
def hello():
    return "hello world"

Config = {
    "host": "0.0.0.0",
    "port": 8888,
    "debug": True
}

if __name__=="__main__":
    app.run(**Config)