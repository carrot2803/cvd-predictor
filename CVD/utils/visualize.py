import polars as pl
from sklearn.calibration import LabelEncoder
import numpy as np
import plotly.graph_objects as go


def correlation_matrix(df: pl.DataFrame, drop_cols: list[str]) -> go.Figure:
    label_encoders: dict = {}
    copy = df.drop(drop_cols)

    for col in copy.columns:
        le = LabelEncoder()
        encoded_col: np.ndarray = le.fit_transform(copy[col].to_numpy())
        copy: pl.DataFrame = copy.with_columns(pl.Series(col, encoded_col))
        label_encoders[col] = le

    correlation_matrix: np.ndarray = copy.corr().to_numpy()
    formatted_text: list[list[str]] = [
        [f"{value:.2f}" for value in row] for row in correlation_matrix
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=correlation_matrix,
            x=copy.columns,
            y=copy.columns,
            colorscale="rdbu",
            zmin=-1,
            zmax=1,
            reversescale=True,
            text=formatted_text,
            texttemplate="%{text}",
            colorbar=dict(title="Correlation"),
        )
    )

    fig.update_layout(
        title="Feature Correlation Heatmap",
        xaxis=dict(tickangle=45, title="Features"),
        yaxis=dict(title="Features"),
        width=900,
        height=900,
    )

    return fig


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
