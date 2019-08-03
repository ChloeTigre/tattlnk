from flask import Flask, render_template



app = Flask(__name__)

@app.route("/")
def home():
    return "<>"


@app.route("/r:<code>")
def code_redirect(code):
    return dict(code=code)


