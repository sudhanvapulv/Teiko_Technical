import sqlite3
from pathlib import Path

import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns


DB_PATH = Path("cell_counts.db")
OUTPUT_DIR = Path("outputs")
POPULATIONS = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]


def get_summary_table(conn):
    df = pd.read_sql_query("SELECT * FROM cell_counts", conn)

    summary = df.melt(
        id_vars=["sample"],
        value_vars=POPULATIONS,
        var_name="population",
        value_name="count"
    )

    totals = df[["sample"] + POPULATIONS].copy()
    totals["total_count"] = totals[POPULATIONS].sum(axis=1)

    summary = summary.merge(
        totals[["sample", "total_count"]],
        on="sample",
        how="left"
    )

    summary["percentage"] = (summary["count"] / summary["total_count"]) * 100

    return summary[["sample", "total_count", "population", "count", "percentage"]]


def responder_analysis(conn, summary):
    metadata = pd.read_sql_query(
        """
        SELECT sample, condition, treatment, response, sample_type
        FROM cell_counts
        """,
        conn
    )

    merged = summary.merge(metadata, on="sample", how="left")

    filtered = merged[
        (merged["condition"] == "melanoma") &
        (merged["treatment"] == "miraclib") &
        (merged["sample_type"] == "PBMC") &
        (merged["response"].isin(["yes", "no"]))
    ].copy()

    stats_rows = []

    for population in POPULATIONS:
        pop_df = filtered[filtered["population"] == population]

        responders = pop_df[pop_df["response"] == "yes"]["percentage"].dropna()
        non_responders = pop_df[pop_df["response"] == "no"]["percentage"].dropna()

        if len(responders) == 0 or len(non_responders) == 0:
            p_value = None
        else:
            _, p_value = mannwhitneyu(
                responders,
                non_responders,
                alternative="two-sided"
            )

        stats_rows.append({
            "population": population,
            "responder_mean_percentage": responders.mean(),
            "non_responder_mean_percentage": non_responders.mean(),
            "p_value": p_value,
            "significant": p_value is not None and p_value < 0.05
        })

    stats_df = pd.DataFrame(stats_rows)

    if not filtered.empty:
        plt.figure(figsize=(10, 6))
        sns.boxplot(
            data=filtered,
            x="population",
            y="percentage",
            hue="response"
        )
        plt.title("Cell Population Frequencies: Responders vs Non-Responders")
        plt.xlabel("Cell population")
        plt.ylabel("Relative frequency (%)")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "responder_boxplot.png")
        plt.close()

    return filtered, stats_df


def subset_analysis(conn):
    query = """
    SELECT *
    FROM cell_counts
    WHERE condition = 'melanoma'
      AND sample_type = 'PBMC'
      AND treatment = 'miraclib'
      AND time_from_treatment_start = 0
    """

    baseline = pd.read_sql_query(query, conn)

    by_project = baseline.groupby("project").size().reset_index(name="sample_count")
    by_response = baseline.groupby("response")["subject"].nunique().reset_index(name="subject_count")
    by_sex = baseline.groupby("sex")["subject"].nunique().reset_index(name="subject_count")

    return baseline, by_project, by_response, by_sex


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    summary = get_summary_table(conn)
    summary.to_csv(OUTPUT_DIR / "summary_table.csv", index=False)

    responder_data, stats_df = responder_analysis(conn, summary)
    responder_data.to_csv(OUTPUT_DIR / "responder_analysis_data.csv", index=False)
    stats_df.to_csv(OUTPUT_DIR / "statistical_results.csv", index=False)

    baseline, by_project, by_response, by_sex = subset_analysis(conn)
    baseline.to_csv(OUTPUT_DIR / "baseline_melanoma_pbmc_miraclib.csv", index=False)
    by_project.to_csv(OUTPUT_DIR / "baseline_by_project.csv", index=False)
    by_response.to_csv(OUTPUT_DIR / "baseline_by_response.csv", index=False)
    by_sex.to_csv(OUTPUT_DIR / "baseline_by_sex.csv", index=False)

    conn.close()

    print("Generated outputs successfully.")


if __name__ == "__main__":
    main()