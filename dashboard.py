from pathlib import Path

import pandas as pd
from dash import Dash, dcc, html, dash_table
import plotly.express as px


OUTPUT_DIR = Path("outputs")

summary = pd.read_csv(OUTPUT_DIR / "summary_table.csv")
stats = pd.read_csv(OUTPUT_DIR / "statistical_results.csv")
responder_data = pd.read_csv(OUTPUT_DIR / "responder_analysis_data.csv")
baseline = pd.read_csv(OUTPUT_DIR / "baseline_melanoma_pbmc_miraclib.csv")
by_project = pd.read_csv(OUTPUT_DIR / "baseline_by_project.csv")
by_response = pd.read_csv(OUTPUT_DIR / "baseline_by_response.csv")
by_sex = pd.read_csv(OUTPUT_DIR / "baseline_by_sex.csv")

app = Dash(__name__)

boxplot = px.box(
    responder_data,
    x="population",
    y="percentage",
    color="response",
    title="Melanoma PBMC Miraclib: Responders vs Non-Responders",
    labels={
        "population": "Cell Population",
        "percentage": "Relative Frequency (%)",
        "response": "Response"
    }
)

project_bar = px.bar(
    by_project,
    x="project",
    y="sample_count",
    title="Baseline Melanoma PBMC Miraclib Samples by Project"
)

response_bar = px.bar(
    by_response,
    x="response",
    y="subject_count",
    title="Baseline Subjects by Response"
)

sex_bar = px.bar(
    by_sex,
    x="sex",
    y="subject_count",
    title="Baseline Subjects by Sex"
)

app.layout = html.Div(
    style={"fontFamily": "Arial", "margin": "30px"},
    children=[
        html.H1("Immune Cell Population Analysis Dashboard"),

        html.P(
            "This dashboard summarizes immune cell frequencies, compares miraclib responders "
            "against non-responders, and explores baseline melanoma PBMC samples."
        ),

        html.H2("Part 2: Summary Table"),
        dash_table.DataTable(
            data=summary.head(100).to_dict("records"),
            columns=[{"name": col, "id": col} for col in summary.columns],
            page_size=10,
            sort_action="native",
            filter_action="native",
            style_table={"overflowX": "auto"},
        ),

        html.H2("Part 3: Responder vs Non-Responder Analysis"),
        dcc.Graph(figure=boxplot),

        html.H3("Statistical Results"),
        dash_table.DataTable(
            data=stats.to_dict("records"),
            columns=[{"name": col, "id": col} for col in stats.columns],
            page_size=10,
            sort_action="native",
            style_table={"overflowX": "auto"},
        ),

        html.H2("Part 4: Baseline Subset Analysis"),
        html.H3("Baseline Melanoma PBMC Miraclib Samples"),
        dash_table.DataTable(
            data=baseline.to_dict("records"),
            columns=[{"name": col, "id": col} for col in baseline.columns],
            page_size=10,
            sort_action="native",
            filter_action="native",
            style_table={"overflowX": "auto"},
        ),

        dcc.Graph(figure=project_bar),
        dcc.Graph(figure=response_bar),
        dcc.Graph(figure=sex_bar),
    ],
)
if __name__ == "__main__":
    app.run(debug=True)