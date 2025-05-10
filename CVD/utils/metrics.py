from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    recall_score,
    roc_curve,
)
from sklearn.metrics import confusion_matrix, precision_score, roc_auc_score
import plotly.graph_objects as go
import polars as pl
import numpy as np


def get_metrics(y_true: np.ndarray, y_pred: np.ndarray, model_name: str) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    sensitivity: float = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity: float = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    balanced_acc = balanced_accuracy_score(y_true, y_pred)

    return {
        "Model": model_name,
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, zero_division=1),
        "Recall": recall_score(y_true, y_pred),
        "Specificity": specificity,
        "F1 Score": f1_score(y_true, y_pred),
        "ROC AUC": roc_auc_score(y_true, y_pred),
        "ROC Curve": roc_curve(y_true, y_pred),
    }
