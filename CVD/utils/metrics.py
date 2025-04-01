from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.metrics import confusion_matrix, precision_score, roc_auc_score
import plotly.graph_objects as go
import polars as pl
import numpy as np


def get_metrics(y_true: np.ndarray, y_pred: np.ndarray, model_name: str) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return {
        "Model": model_name,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=1),
        "Recall": recall_score(y_true, y_pred),
        "F1 Score": f1_score(y_true, y_pred),
        "ROC AUC": roc_auc_score(y_true, y_pred),
        # "True Negative": tn,
        # "False Positive": fp,
        # "False Negative": fn,
        # "True Positive": tp,
    }
