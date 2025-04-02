import pickle
from flask import Flask, Response, render_template, request, jsonify
import numpy as np
import polars as pl
from xgboost import XGBClassifier

app = Flask(__name__)
model: XGBClassifier = pickle.load(open("models/lightgbm_cvd.pkl", "rb"))
# model = XGBClassifier()
# model.load_model("models/xgb_cvd.json")


@app.route("/")
def home() -> str:
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict() -> Response:
    print(request.json)
    df = pl.DataFrame(request.json)
    matrix: np.ndarray = model.predict_proba(df[0])
    prediction = str(matrix[:, 1][0])
    print("Prediction is ", prediction)
    return jsonify(message=str(prediction))


@app.route("/results")
def results() -> str:
    return render_template("results.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
