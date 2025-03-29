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


def plot_feature_importances(model, X, top_n=15, model_name="Model") -> None:
    """
    - model: A trained model with the attribute `feature_importances_`.
    - X: A Polars DataFrame or any object with a `columns` attribute for feature names.
    - top_n: The number of top features to display (default is 15).
    - model_name: A name to display in the plot title.
    """
    if hasattr(model, "feature_importances_"):
        # Create a Polars DataFrame
        df = pl.DataFrame(
            {"feature": X.columns, "importance": model.feature_importances_}
        )

        df_top: pl.DataFrame = (
            df.sort("importance", descending=True)
            .head(top_n)
            .sort("importance", descending=False)
        )

        features = df_top["feature"].to_list()
        importances = df_top["importance"].to_list()

        colors: list[str] = [
            f"rgb({int(255 * (1 - i / len(features)))}, {int(100 * (1 - i / len(features)))}, {int(200 * (i / len(features)))})"
            for i in range(len(features))
        ]

        fig = go.Figure(
            go.Bar(
                x=importances, y=features, orientation="h", marker=dict(color=colors)
            )
        )

        fig.update_layout(
            title=f"Top {top_n} Feature Importances - {model_name}",
            xaxis_title="Feature Importance Score",
            yaxis_title="Features",
            margin=dict(l=150),
        )

        fig.show()
    else:
        print(f"{model_name} does not have feature_importances_ attribute.")
