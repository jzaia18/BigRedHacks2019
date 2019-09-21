from flask import Flask, render_template
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route("/hello")
def root():
    return 'Hello World'

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
