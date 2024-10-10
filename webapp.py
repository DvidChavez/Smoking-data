from flask import Flask, request, render_template, flash
from markupsafe import Markup

import os
import json

app = Flask(__name__)

@app.route("/")
def render_main():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
