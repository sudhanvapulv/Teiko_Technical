# Teiko Technical Assessment

## Overview

This project analyzes immune cell population data from a clinical trial and provides both statistical analyses and an interactive dashboard for exploring the results.

The pipeline:

1. Loads cell count data from `cell-count.csv` into a SQLite database.
2. Calculates relative frequencies for immune cell populations within each sample.
3. Compares responders versus non-responders among melanoma patients receiving miraclib treatment.
4. Performs statistical testing to identify populations associated with treatment response.
5. Generates visualizations and summary outputs.
6. Provides an interactive dashboard for data exploration.

---

## Repository Structure

```text
.
├── cell-count.csv
├── load_data.py
├── analysis.py
├── dashboard.py
├── requirements.txt
├── Makefile
├── README.md
├── cell_counts.db
└── outputs/
```

---

## Setup

Install dependencies:

```bash
make setup
```

or

```bash
pip install -r requirements.txt
```

---

## Running the Pipeline

Execute the complete pipeline:

```bash
make pipeline
```

This will:

1. Create the SQLite database.
2. Load all records from `cell-count.csv`.
3. Generate summary tables.
4. Run statistical analyses.
5. Produce plots and output files.

Generated outputs are written to the `outputs/` directory.

---

## Launching the Dashboard

Start the dashboard locally:

```bash
make dashboard
```

Then open:

```text
http://127.0.0.1:8050
```

Dashboard features include:

* Cell population frequency summaries
* Responder vs. non-responder comparisons
* Statistical analysis results
* Baseline melanoma PBMC subset analysis

---

## Database Schema

The dataset is stored in a single SQLite table named `cell_counts`.

### Columns

| Column                    | Description                           |
| ------------------------- | ------------------------------------- |
| project                   | Clinical project identifier           |
| subject                   | Subject identifier                    |
| condition                 | Disease indication                    |
| age                       | Subject age                           |
| sex                       | Subject sex                           |
| treatment                 | Treatment received                    |
| response                  | Treatment response                    |
| sample                    | Sample identifier                     |
| sample_type               | Sample type (e.g. PBMC)               |
| time_from_treatment_start | Timepoint relative to treatment start |
| b_cell                    | B cell count                          |
| cd8_t_cell                | CD8 T cell count                      |
| cd4_t_cell                | CD4 T cell count                      |
| nk_cell                   | NK cell count                         |
| monocyte                  | Monocyte count                        |

### Design Rationale

For this assessment, a single-table design provides a simple and efficient representation of the provided dataset.

For larger production datasets involving hundreds of projects and thousands of samples, the schema would be normalized into separate entities such as:

* Projects
* Subjects
* Samples
* Treatments
* Responses
* Cell Population Measurements

This normalization would:

* Reduce data redundancy
* Improve maintainability
* Support additional immune cell populations
* Enable more complex analytical queries
* Improve scalability as data volume grows

Indexes would be added on frequently queried fields such as:

* project
* subject
* treatment
* response
* sample_type

to improve query performance.

---

## Part 2: Relative Frequency Analysis

For each sample:

1. Total cell count is calculated as the sum of all immune cell populations.
2. Relative frequency is calculated as:

Percentage = (Population Count / Total Count) × 100

The resulting summary table contains:

- sample
- total_count
- population
- count
- percentage

### Output Files

- `outputs/summary_table.csv`

This file contains one row per sample-population combination and serves as the primary output for Part 2.
## Part 3: Statistical Analysis

The analysis focuses on:

- Melanoma patients
- PBMC samples
- Miraclib treatment

Responder (`response = yes`) and non-responder (`response = no`) groups are compared using the Mann-Whitney U test.

For each immune cell population:

- Mean relative frequency is calculated
- Statistical significance is evaluated
- Relative frequency distributions are visualized using boxplots

### Output Files

- `outputs/statistical_results.csv`
  - Summary statistics and p-values for each immune cell population.

- `outputs/responder_analysis_data.csv`
  - Filtered melanoma PBMC miraclib dataset used for responder vs. non-responder analysis.

- `outputs/responder_boxplot.png`
  - Boxplot visualization comparing relative frequencies of each immune cell population between responders and non-responders.
---
## Part 4: Baseline Subset Analysis

The database is queried to identify baseline samples meeting the following criteria:

- Condition = melanoma
- Sample type = PBMC
- Treatment = miraclib
- Time from treatment start = 0

Among the resulting samples, the analysis reports:

- Number of samples from each project
- Number of responder and non-responder subjects
- Number of male and female subjects

### Output Files

- `outputs/baseline_melanoma_pbmc_miraclib.csv`
  - All melanoma PBMC baseline samples from subjects treated with miraclib.

- `outputs/baseline_by_project.csv`
  - Counts of baseline samples grouped by project.

- `outputs/baseline_by_response.csv`
  - Counts of unique responder and non-responder subjects.

- `outputs/baseline_by_sex.csv`
  - Counts of unique male and female subjects.

  
## Code Structure

### load_data.py

Responsible for:

* Database creation
* Schema initialization
* CSV ingestion

### analysis.py

Responsible for:

* Summary table generation
* Statistical analysis
* Plot generation
* Subset analysis

### dashboard.py

Responsible for:

* Interactive visualizations
* Displaying generated outputs
* User-facing exploration interface

This separation keeps ingestion, analysis, and presentation layers independent and easier to maintain.

---

## Dashboard Link

Local dashboard:

```text
http://127.0.0.1:8050
```
