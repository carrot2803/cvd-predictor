from plotly.graph_objs import Figure
import polars as pl
import plotly.graph_objects as go


path: str = "data/processed/"


def plot_age_distribution(df: pl.DataFrame, plotname: str) -> go.Figure:
    age_labels: dict[int, str] = {
        1: "Age 18 to 24",
        2: "Age 25 to 29",
        3: "Age 30 to 34",
        4: "Age 35 to 39",
        5: "Age 40 to 44",
        6: "Age 45 to 49",
        7: "Age 50 to 54",
        8: "Age 55 to 59",
        9: "Age 60 to 64",
        10: "Age 65 to 69",
        11: "Age 70 to 74",
        12: "Age 75 to 79",
        13: "Age 80 or older",
    }

    age_counts: pl.DataFrame = (
        df.group_by("AgeCategory").agg(pl.count().alias("Count")).sort("AgeCategory")
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
            marker_color="#6CC3A0",
            hovertemplate="%{x}<br>Count: %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        template="ggplot2",
        title="Distribution of Age Categories",
        xaxis_title="Age Category",
        yaxis_title="Count",
        bargap=0.1,
        height=625,
        xaxis=dict(tickangle=45, tickmode="array", tickvals=categories),
    )

    fig.write_html(f"{path}/html/{plotname}.html", include_plotlyjs="cdn")
    fig.update_layout(height=800)
    fig.write_image(f"{path}/imgs/{plotname}.png", width=1500)

    return fig
