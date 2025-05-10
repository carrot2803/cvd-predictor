import numpy as np
import plotly.graph_objects as go
import polars as pl


age_labels: dict[int, str] = {
    1: "18-24",
    2: "25-29",
    3: "30-34",
    4: "35-39",
    5: "40-44",
    6: "45-49",
    7: "50-54",
    8: "55-59",
    9: "60-64",
    10: "65-69",
    11: "70-74",
    12: "75-79",
    13: "80+",
}


def _prepare_rates(df: pl.DataFrame, by: str) -> pl.DataFrame:
    return (
        df.group_by(["AgeCategory", by])
        .agg([pl.mean("CVD").alias("cvd_rate"), pl.len().alias("n")])
        .sort("AgeCategory")
        .with_columns(
            [
                pl.col("AgeCategory")
                .map_elements(lambda i: age_labels.get(i, str(i)), return_dtype=pl.Utf8)
                .alias("age_label")
            ]
        )
    )


def plot_cvd_by_smoking(
    df: pl.DataFrame, plotname: str, path: str = "data/processed/"
) -> go.Figure:
    rates: pl.DataFrame = _prepare_rates(df, "SmokerStatus")

    fig = go.Figure()
    color_map: dict[int, str] = {
        0: "steelblue",
        1: "lightcoral",
    }  # Non-smokers  # Smokers

    for status_val, name in [(0, "Non-smokers"), (1, "Smokers")]:
        sub = rates.filter(pl.col("SmokerStatus") == status_val)
        fig.add_trace(
            go.Bar(
                x=sub["age_label"].to_list(),
                y=sub["cvd_rate"].to_list(),
                name=name,
                text=[f"{r:.1%}" for r in sub["cvd_rate"].to_list()],
                textposition="auto",
                marker_color=color_map[status_val],
                customdata=sub["n"].to_list(),
            )
        )

    fig.update_layout(
        template="plotly_white",
        title="CVD Rate by Age and Smoking Status",
        xaxis_title="Age Category",
        yaxis_title="CVD Rate",
        barmode="group",
        height=700,
        width=1200,
        font_size=16,
        showlegend=True,
        legend=dict(
            x=0.01,
            y=0.99,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.5)",
            bordercolor="lightgrey",
            borderwidth=1,
        ),
    )

    fig.update_xaxes(showgrid=False, gridcolor="lightgrey", zeroline=False)
    fig.update_yaxes(showgrid=True)

    fig.write_image(
        f"{path}/imgs/{plotname}_smoking.png", width=1000, height=700, scale=3
    )

    return fig


def plot_cvd_by_drinking(
    df: pl.DataFrame, plotname: str, path: str = "data/processed/"
) -> go.Figure:
    rates: pl.DataFrame = _prepare_rates(df, "AlcoholDrinkers")
    fig = go.Figure()

    fig = go.Figure()
    color_map: dict[int, str] = {
        0: "steelblue",  # Non-smokers
        1: "lightcoral",  # Smokers
    }

    for status_val, name in [(0, "Non-drinkers"), (1, "Drinkers")]:
        sub: pl.DataFrame = rates.filter(pl.col("AlcoholDrinkers") == status_val)
        fig.add_trace(
            go.Bar(
                x=sub["age_label"].to_list(),
                y=sub["cvd_rate"].to_list(),
                name=name,
                text=[f"{r:.1%}" for r in sub["cvd_rate"].to_list()],
                textposition="auto",
                marker_color=color_map[status_val],
                customdata=sub["n"].to_list(),
            )
        )

    fig.update_layout(
        template="plotly_white",
        title="CVD Rate by Age and Drinking Status",
        xaxis_title="Age Category",
        yaxis_title="CVD Rate",
        barmode="group",
        height=700,
        width=1200,
        font_size=16,
        showlegend=True,
        legend=dict(
            x=0.01,
            y=0.99,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.5)",  # optional: semi-transparent background
            bordercolor="lightgrey",
            borderwidth=1,
        ),
    )

    fig.update_xaxes(showgrid=False, gridcolor="lightgrey", zeroline=False)
    fig.update_yaxes(showgrid=True)

    fig.write_image(
        f"{path}/imgs/{plotname}drinking.png", width=1000, height=700, scale=3
    )
    return fig


def plot_age_distribution(df: pl.DataFrame, plot_name: str) -> go.Figure:
    df = df.filter(pl.col("CVD") == 1)
    age_counts: pl.DataFrame = (
        df.group_by("AgeCategory").agg(pl.len().alias("Count")).sort("AgeCategory")
    )

    numeric_categories: list[int] = age_counts["AgeCategory"].to_list()
    counts: list[int] = age_counts["Count"].to_list()

    categories: list[str] = [
        age_labels.get(cat, str(cat)) for cat in numeric_categories
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=categories,
            y=counts,
            text=counts,
            textposition="auto",
            marker=dict(color="steelblue"),
            hovertemplate="%{x}<br>Count: %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_white",
        title="Distribution of CVD Cases by Age Group",
        xaxis_title="Age Group",
        yaxis_title="CVD Cases",
        bargap=0.1,
        # width=1000,
        # height=800,
        font_size=16,
        # margin=dict(l=160, r=40, t=50, b=40),
        xaxis=dict(tickangle=0, tickmode="array", tickvals=categories),
    )

    # Axis formatting
    fig.update_xaxes(showgrid=False, gridcolor="lightgrey", zeroline=False)
    fig.update_yaxes(showgrid=True)

    # Save high-quality image
    fig.write_image(
        f"data/processed/imgs/{plot_name}.png", width=1000, height=700, scale=3
    )
    return fig


def create_bmi_density_plot(
    df: pl.DataFrame, plot_name: str, bmi_cutoff: int = 60
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
        title="BMI Probability Density Curve",
        xaxis_title="Body Mass Index",
        yaxis_title="Probability Density",
        legend_title="CVD Status",
        template="plotly_white",
        font_size=16,
        showlegend=True,
        legend=dict(
            x=0.01,
            y=0.99,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.5)",  # optional: semi-transparent background
            bordercolor="lightgrey",
            borderwidth=1,
        ),
    )

    fig.update_xaxes(showgrid=True, gridcolor="lightgrey", zeroline=False)
    fig.update_yaxes(showgrid=True)

    fig.write_image(
        f"data/processed/imgs/{plot_name}.png", width=1000, height=700, scale=3
    )
    return fig
