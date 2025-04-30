import numpy as np
import polars as pl
import plotly.graph_objects as go

path: str = "data/processed/"


def create_bmi_density_plot(
    df: pl.DataFrame, plotname: str, bmi_cutoff: int = 60
) -> go.Figure:
    filtered_df: pl.DataFrame = df.filter(pl.col("BMI") <= bmi_cutoff)

    bmi_no_cvd: list[int] = filtered_df.filter(pl.col("CVD") == 0)["BMI"].to_list()
    bmi_cvd: list[int] = filtered_df.filter(pl.col("CVD") == 1)["BMI"].to_list()

    bin_edges: np.ndarray = np.linspace(
        min(filtered_df["BMI"]), max(filtered_df["BMI"]), 50
    )
    dens_nc, _ = np.histogram(bmi_no_cvd, bins=bin_edges, density=True)
    dens_c, _ = np.histogram(bmi_cvd, bins=bin_edges, density=True)

    bin_centers: np.ndarray = (bin_edges[:-1] + bin_edges[1:]) / 2

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=bin_centers,
            y=dens_nc,
            mode="lines",
            name="No CVD",
            line=dict(width=2, color="#72b7b2"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=bin_centers,
            y=dens_c,
            mode="lines",
            name="CVD",
            line=dict(width=2, color="#e45756"),
        )
    )

    fig.update_layout(
        title="BMI Density Curve",
        xaxis_title="Body Mass Index",
        yaxis_title="Probability Density",
        legend_title="CVD Status",
        template="ggplot2",
    )

    fig.update_layout(height=625)
    fig.write_html(f"{path}/html/{plotname}.html", include_plotlyjs="cdn")
    fig.update_layout(height=800)
    fig.write_image(f"{path}/imgs/{plotname}.png", width=1500)
    return fig
