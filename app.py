from flask import Flask, render_template, request, session, url_for, redirect, flash

import os
app = Flask(__name__) #create instance of class flask

# app.secret_key = os.urandom(32)


app.route("/", methods = ["GET", "POST"])
def index():
    print("Cowabunga!")
    return "No hablo queso!"


if __name__ == "__main__":
    app.debug = True
    app.run()
