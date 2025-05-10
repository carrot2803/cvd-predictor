import os
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from CVD import CVDClassifier

app = Flask(__name__)
CORS(app)
cvd = CVDClassifier()


@app.route("/")
def home() -> str:
    return "Healthy"


@app.route("/predict/<int:top_n>", methods=["POST"])
def predict(top_n: int) -> Response:
    prob, top_features = cvd.predict(request.json, top_n)
    results: dict[str, str | list[dict]] = {
        "probability": prob,
        "top_features": top_features,
    }
    return jsonify(results)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
