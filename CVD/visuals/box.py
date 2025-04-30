from plotly.graph_objs import Figure
import polars as pl
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

path: str = "data/processed/"

def plot_bmi_vs_health(df: pl.DataFrame, plotname: str) -> Figure:
    health_statuses: list[int] = (
        df.select("GeneralHealth").unique().get_column("GeneralHealth").to_list()
    )
    health_mapping: dict[int, str] = {
        1: "Excellent",
        2: "Very good",
        3: "Good",
        4: "Fair",
        5: "Poor",
    }
    custom_colors: list[str] = px.colors.qualitative.Prism
    fig = go.Figure()
    
    for i, health in enumerate(health_statuses):
        # Get the filtered DataFrame for this health status
        health_df = df.filter(pl.col("GeneralHealth") == health)
        
        # Use the filtered DataFrame for calculating the boxplot
        # But filter out points above 80 for display
        bmi_values = health_df.select("BMI").get_column("BMI").to_list()
        
        # Only show points ≤ 80 in the boxplot display
        display_values = [bmi for bmi in bmi_values if bmi <= 80]
        
        display_name: str = health_mapping.get(health, str(health))
        
        fig.add_trace(
            go.Box(
                y=display_values,
                name=display_name,
                boxmean=True,  # Show the mean
                marker_color=custom_colors[i % len(custom_colors)],
                line_color=custom_colors[i % len(custom_colors)],
            )
        )
    
    fig.update_layout(
        title="BMI Distribution by General Health Status",
        yaxis_title="Body Mass Index",
        xaxis_title="General Health Status",
        xaxis={
            "categoryorder": "array",
            "categoryarray": ["Excellent", "Very good", "Good", "Fair", "Poor"],
        },
        template="seaborn",
        yaxis_range=[0, 80],  # Limit y-axis to 80
        colorway=px.colors.qualitative.Prism,
    )
    fig.update_layout(height=625)
    fig.write_html(f"{path}/html/{plotname}.html", include_plotlyjs="cdn")
    fig.update_layout(height=800)
    fig.write_image(f"{path}/imgs/{plotname}.png", width=1500)
    return fig
    