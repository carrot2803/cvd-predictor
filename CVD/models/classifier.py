import pickle
from lightgbm import LGBMClassifier
import numpy as np
from sklearn.preprocessing import StandardScaler
import polars as pl
from ..constants import MODEL, SCALER


class CVDClassifier:
    def __init__(self) -> None:
        self._scaler: StandardScaler = pickle.load(open(SCALER, "rb"))
        self._model: LGBMClassifier = pickle.load(open(MODEL, "rb"))

    def predict(
        self, json: dict, top_n: int = 5
    ) -> tuple[float, list[tuple[str, float]]]:
        df = pl.DataFrame(json)
        X: np.ndarray = self._scaler.transform(df.to_numpy())
        feature_names: np.ndarray = np.array(df.columns)
        contribs = self._model.predict(X, pred_contrib=True)[0]
        contrib = contribs[:-1]
        logit = contrib.sum() + contribs[-1]
        proba = 1.0 / (1.0 + np.exp(-logit))  # sigmoid
        idx = np.argpartition(-contrib, top_n)[:top_n]
        return proba, list(zip(feature_names[idx], contrib[idx]))
