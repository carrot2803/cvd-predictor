from plotly.graph_objs import Figure
import polars as pl
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

path: str = "data/processed/"


def count_plot(y_train) -> Figure:
    df: pl.DataFrame = pl.DataFrame({"CVD": y_train}).group_by("CVD").len().sort("CVD")
    map: dict[str, str] = {"0": "No CVD", "1": "CVD"}
    df = df.with_columns(
        pl.col("CVD").cast(pl.Utf8).replace(map).alias("label"),
        pl.col("len").alias("count"),
    )

    fig: Figure = px.bar(
        df,
        x="label",
        y="count",
        text="count",
        height=500,
        template="ggplot2",
        title="CVD Class Distribution",
        color="label",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_layout(yaxis_title="Count", xaxis_title="CVD Status")
    return fig


def add_health_bar(fig, df, health_status, mobility_status) -> None:
    COLOR_MAP: dict[str, str] = {"Yes": "#FF6692", "No": "#00CC96"}
    show_legend: bool = health_status == "Poor"

    filtered: pl.DataFrame = df.filter(
        (pl.col("GeneralHealth") == health_status)
        & (pl.col("Mobility") == mobility_status)
    )
    if filtered.height > 0:
        fig.add_trace(
            go.Bar(
                x=[health_status],
                y=filtered["count"].to_list(),
                name=mobility_status,
                marker_color=COLOR_MAP[mobility_status],
                text=filtered["percentage"].to_list(),
                texttemplate="%{text}%",
                textposition="auto",
                showlegend=show_legend,
            )
        )


def plot_mobility_issues(df: pl.DataFrame, plotname: str) -> Figure:
    GENERAL_HEALTH: dict[int, str] = {
        5: "Poor",
        4: "Fair",
        3: "Good",
        2: "Very Good",
        1: "Excellent",
    }
    MOBILITY_STATUS: dict[int, str] = {0: "No", 1: "Yes"}
    columns: list[str] = ["GeneralHealth", "Mobility"]

    health_mobility: pl.DataFrame = df.select(columns).with_columns(
        pl.col("GeneralHealth").map_elements(GENERAL_HEALTH.get, pl.String),
        pl.col("Mobility").map_elements(MOBILITY_STATUS.get, pl.String),
    )

    health_mobility: pl.DataFrame = (
        health_mobility.group_by(columns)
        .agg(pl.len().alias("count"))
        .with_columns(
            (pl.col("count") / pl.sum("count").over("GeneralHealth") * 100)
            .round(1)
            .alias("percentage")
        )
    )

    fig: Figure = go.Figure()

    health_order: list[str] = ["Poor", "Fair", "Good", "Very Good", "Excellent"]
    for health_status in health_order:
        add_health_bar(fig, health_mobility, health_status, "No")
        add_health_bar(fig, health_mobility, health_status, "Yes")

    fig.update_layout(
        title="Mobility Issues by General Health Status",
        xaxis_title="Self-Reported General Health",
        yaxis_title="Number of Individuals",
        legend_title="Mobility Issues",
        barmode="stack",
        template="ggplot2",
    )

    fig.update_layout(height=625)
    fig.write_html(f"{path}/html/{plotname}.html", include_plotlyjs="cdn")
    fig.update_layout(height=800)
    fig.write_image(f"{path}/imgs/{plotname}.png", width=1500)

    return fig


def plot_chronic_disease_prevalence(df: pl.DataFrame, plotname: str) -> Figure:
    health_conditions: list[str] = [
        "HadAsthma",
        "HadCOPD",
        "HadKidneyDisease",
        "HadArthritis",
        "HadDiabetes",
        "CVD",
    ]

    conditions: list = []
    percentages: list = []

    for condition in health_conditions:
        if condition not in df.columns:
            continue

        value_counts: pl.DataFrame = (
            df.group_by(condition).agg(pl.count()).sort(condition)
        )

        total_count: int = df.shape[0]

        if value_counts.shape[0] > 0:
            condition_values: list[int] = value_counts.get_column(condition).to_list()

            # Special case for HadAsthma which has flipped logic
            if condition == "HadAsthma":
                if 0 in condition_values:
                    yes_count = (
                        value_counts.filter(pl.col(condition) == 0)
                        .select(pl.col("count"))
                        .item()
                    )
                    percentage = (yes_count / total_count) * 100
                else:
                    continue
            # Standard logic for other conditions
            else:
                if 1 in condition_values:
                    yes_count = (
                        value_counts.filter(pl.col(condition) == 1)
                        .select(pl.col("count"))
                        .item()
                    )
                    percentage = (yes_count / total_count) * 100
                elif "Yes" in condition_values:
                    yes_count = (
                        value_counts.filter(pl.col(condition) == "Yes")
                        .select(pl.col("count"))
                        .item()
                    )
                    percentage = (yes_count / total_count) * 100
                else:
                    continue

            conditions.append(condition)
            percentages.append(percentage)

    fig = go.Figure(
        data=[
            go.Bar(
                x=conditions,
                y=percentages,
                text=[f"{p:.1f}%" for p in percentages],
                textposition="auto",
                marker_color=px.colors.qualitative.Prism,
            )
        ]
    )

    fig.update_layout(
        title="Prevalence of Chronic Conditions",
        xaxis_title="Condition",
        yaxis_title="Percentage of Population (%)",
        yaxis_range=[0, max(percentages) * 1.1] if percentages else [0, 100],
        template="ggplot2",
    )

    fig.update_layout(height=625)
    fig.write_html(f"{path}/html/{plotname}.html", include_plotlyjs="cdn")
    fig.update_layout(height=800)
    fig.write_image(f"{path}/imgs/{plotname}.png", width=1500)

    return fig


def plot_cvd_by_risk_factors(df: pl.DataFrame, plotname: str) -> Figure:
    risk_factors: list[str] = [
        "Sex",
        "SmokerStatus",
        "AlcoholDrinkers",
        "HaveHighCholesterol",
    ]

    label_mappings: dict[str, dict[int, str]] = {
        "Sex": {0: "Female", 1: "Male"},
        "SmokerStatus": {0: "Non-Smoker", 1: "Smoker"},
        "AlcoholDrinkers": {0: "Non-Drinker", 1: "Drinker"},
        "HaveHighCholesterol": {0: "Normal Cholesterol", 1: "High Cholesterol"},
    }

    subtitle = "Percentages represent CVD prevalence within each group"

    fig: Figure = make_subplots(rows=2, cols=2, subplot_titles=risk_factors)

    positions: list[tuple[int, int]] = [(1, 1), (1, 2), (2, 1), (2, 2)]

    for i, factor in enumerate(risk_factors):
        # Get categories and calculate CVD rates
        categories: pl.Series = df[factor].unique().sort()
        cvd_rates: list[float] = []
        labels: list[str] = []

        for cat in categories:
            subset: pl.DataFrame = df.filter(pl.col(factor) == cat)
            cvd_rate: float = (
                subset.filter(pl.col("CVD") == 1).shape[0] / subset.shape[0] * 100
            )
            cvd_rates.append(cvd_rate)

            labels.append(label_mappings[factor].get(cat, str(cat)))

        row, col = positions[i]
        fig.add_trace(
            go.Bar(
                x=labels,
                y=cvd_rates,
                name=factor,
                text=[f"{r:.1f}%" for r in cvd_rates],
                textposition="auto",
                marker_color=px.colors.qualitative.Prism[
                    i % len(px.colors.qualitative.Prism)
                ],
            ),
            row=row,
            col=col,
        )

    fig.update_layout(
        height=800,
        template="ggplot2",
        showlegend=False,
        title={
            "text": f"CVD Rates by Risk Factors<br><sup>{subtitle}</sup>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    for i in range(1, 5):
        fig.update_yaxes(
            title_text="CVD Prevalence (%)", row=(i - 1) // 2 + 1, col=(i - 1) % 2 + 1
        )

    fig.update_layout(height=625)
    fig.write_html(f"{path}/html/{plotname}.html", include_plotlyjs="cdn")
    fig.update_layout(height=800)
    fig.write_image(f"{path}/imgs/{plotname}.png", width=1500)
    return fig
