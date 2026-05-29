import sqlite3
from pathlib import Path

import pandas as pd


DB_PATH = Path("cell_counts.db")
CSV_PATH = Path("cell-count.csv")


def create_schema(conn):
    conn.execute("DROP TABLE IF EXISTS cell_counts")

    conn.execute("""
        CREATE TABLE cell_counts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project TEXT NOT NULL,
            subject TEXT NOT NULL,
            condition TEXT NOT NULL,
            age INTEGER,
            sex TEXT,
            treatment TEXT,
            response TEXT,
            sample TEXT NOT NULL UNIQUE,
            sample_type TEXT,
            time_from_treatment_start INTEGER,
            b_cell INTEGER,
            cd8_t_cell INTEGER,
            cd4_t_cell INTEGER,
            nk_cell INTEGER,
            monocyte INTEGER
        )
    """)

    conn.commit()

def clean_column_name(col):
    return col.strip().replace("\\", "").replace(" ", "_")


def load_csv(conn):
    df = pd.read_csv(CSV_PATH)
    df.columns = [clean_column_name(col) for col in df.columns]

    df.to_sql(
        "cell_counts",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError("cell-count.csv not found in repo root")

    conn = sqlite3.connect(DB_PATH)

    create_schema(conn)
    load_csv(conn)

    count = conn.execute("SELECT COUNT(*) FROM cell_counts").fetchone()[0]
    conn.close()

    print(f"Created {DB_PATH}")
    print(f"Loaded {count} rows into cell_counts")


if __name__ == "__main__":
    main()