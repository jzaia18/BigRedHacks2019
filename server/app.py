from flask import Flask, render_template
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(16)


@app.route("/")
def root():
    pass

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
