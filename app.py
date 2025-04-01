from flask import Flask, render_template, request, jsonify
import numpy as np


app = Flask(__name__)


@app.route("/")
def home() -> str:
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    print(request.json)
    return jsonify(message=request.json)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
