from flask import Flask, render_template, request, jsonify
import numpy as np


app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    return "Yes"


if __name__ == "__main__":
    app.run(debug=True)
