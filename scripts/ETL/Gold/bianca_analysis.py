"""
Individual Analytical Module - Bianca Acosta
=============================================
Purpose: Answer Research Question 6 (P6) and validate its hypothesis using a
Chi-Square Test of Independence.

Research Question 6 (P6):
    Which gender makes more purchases on the platform?

Hypotheses:
    H0: Student gender and purchase action are independent
        (no significant association between gender and purchase).
    H1: Student gender and purchase action are associated
        (gender significantly influences the probability of purchase).

Methodology:
    Chi-Square Test of Independence (scipy.stats.chi2_contingency) over the
    gender x action (purchase / no_purchase) contingency table.

IMPORTANT - Scope of this module:
    This script is completely independent and read-only with respect to the
    database:
      1. ONLY READS from Supabase (raw extraction, nothing is modified).
      2. NO drop, delete, update, or upsert of any kind.
      3. Cleaning/"augmentation" (dedupe, validation, enrichment via JOINs) is
         done in memory, only for this analysis.
      4. Results (chart + report) are generated and saved only to Bianca's own
         files, without touching the team's shared pipeline or report. This
         avoids Git conflicts with other individual modules
         (rivaldo_analysis.py, etc.).

Data augmentation disclosure:
    The real dataset has very few registered users, which limits the
    statistical power of the Chi-Square test. As required by the course, this
    module ALSO runs a secondary, clearly labeled analysis on an AUGMENTED
    dataset that blends the real data with SIMULATED purchase events (see
    augment_with_simulated_data()). The simulation is seeded with each
    gender's real observed purchase rate, not an arbitrary or desired
    outcome, and uses a fixed random seed for reproducibility. The real-data
    result remains the primary, authoritative finding; the augmented result
    is always reported separately and explicitly marked as simulated.

Author: Bianca Acosta
Team: Analytics and Statistical Validation
"""

from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Headless backend, suitable for servers/CI
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact

# ============================================
# PROJECT PATHS (BIANCA'S LOCAL OUTPUT ONLY)
# ============================================
# Everything this script generates lives inside its own self-contained folder
# (BiancaAcostaProject/), matching the pattern used by other teammates, so
# personal files never mix with the repo's shared folders (charts/, db/) and
# no Git conflicts are created.
ROOT_DIR = Path(__file__).resolve().parents[3]
PROJECT_DIR = ROOT_DIR / "BiancaAcostaProject"
CHARTS_DIR = PROJECT_DIR / "charts"
GOLD_OUTPUT_DIR = PROJECT_DIR / "gold_output"
REPORT_PATH = PROJECT_DIR / "statistical_report_bianca.md"
CSV_PATH = GOLD_OUTPUT_DIR / "resultados_p6_bianca.csv"
CHART_FILENAME = "purchases_by_gender.png"

ALPHA = 0.05  # Significance level (95% confidence)


# ============================================
# 1) EXTRACTION (READ-ONLY)
# ============================================
def extract_raw_data() -> dict:
    """
    Extracts the raw data needed directly from Supabase, reusing the team's
    Bronze extractor (read-only, nothing is modified in the database).

    Returns:
        dict with the raw DataFrames: usuarios_sesion, interacciones_telemetria
    """
    import sys
    sys.path.append(str(ROOT_DIR))
    from scripts.ETL.Bronze.raw_data import run_bronze_pipeline

    raw_data = run_bronze_pipeline()
    print(
        f"  \u2713 Extraction completed (read-only): "
        f"usuarios_sesion = {len(raw_data['usuarios_sesion'])} rows | "
        f"interacciones_telemetria = {len(raw_data['interacciones_telemetria'])} rows"
    )
    return raw_data


# ============================================
# 2) LOCAL CLEANING AND AUGMENTATION (IN MEMORY ONLY)
# ============================================
def clean_and_augment_locally(raw_data: dict) -> pd.DataFrame:
    """
    Performs the cleaning and enrichment (augmentation) needed for P6,
    entirely in memory and only for this analysis.

    Does not modify or delete anything in the database: no drop, delete,
    update, or upsert. It only transforms local copies of the already
    extracted raw DataFrames.

    Args:
        raw_data: dict with raw 'usuarios_sesion' and 'interacciones_telemetria'.

    Returns:
        Local enriched DataFrame with 'genero' and 'tipo_evento' columns,
        ready for the P6 analysis.
    """
    usuarios = raw_data["usuarios_sesion"].copy()
    telemetria = raw_data["interacciones_telemetria"].copy()

    print(f"  \u2022 Input: usuarios_sesion = {len(usuarios)} rows | interacciones_telemetria = {len(telemetria)} rows")

    # --- User cleaning (in memory) ---
    rows_before = len(usuarios)
    usuarios = usuarios.drop_duplicates(subset=["id"], keep="first")
    print(f"  \u2022 Dedupe usuarios_sesion: {rows_before} -> {len(usuarios)} rows ({rows_before - len(usuarios)} duplicates removed)")

    rows_before = len(usuarios)
    usuarios = usuarios.dropna(subset=["genero"])
    print(f"  \u2022 Validation: non-null gender: {rows_before} -> {len(usuarios)} rows ({rows_before - len(usuarios)} dropped)")

    # --- Telemetry cleaning (in memory) ---
    rows_before = len(telemetria)
    telemetria = telemetria.drop_duplicates(subset=["id"], keep="first")
    print(f"  \u2022 Dedupe interacciones_telemetria: {rows_before} -> {len(telemetria)} rows ({rows_before - len(telemetria)} duplicates removed)")

    rows_before = len(telemetria)
    valid_events = ["view", "add_to_cart", "purchase"]
    telemetria = telemetria[telemetria["tipo_evento"].isin(valid_events)]
    print(f"  \u2022 Validation: allowed tipo_evento: {rows_before} -> {len(telemetria)} rows ({rows_before - len(telemetria)} dropped)")

    # --- Referential integrity: only events from valid users ---
    rows_before = len(telemetria)
    telemetria = telemetria[telemetria["usuario_id"].isin(set(usuarios["id"]))]
    print(f"  \u2022 Referential integrity (valid usuario_id): {rows_before} -> {len(telemetria)} rows ({rows_before - len(telemetria)} dropped)")

    # --- Augmentation: enrich telemetry with the user's gender ---
    rows_before = len(telemetria)
    df_local = telemetria.merge(
        usuarios[["id", "genero"]],
        left_on="usuario_id",
        right_on="id",
        how="inner",
        suffixes=("", "_usuario"),
    ).drop(columns=["id_usuario"], errors="ignore")
    print(f"  \u2022 Augmentation (JOIN with user gender): {rows_before} -> {len(df_local)} rows, {len(df_local.columns)} columns")

    print(f"  \u2713 Bianca's local dataset ready: {len(df_local)} events (in memory only, nothing written to the DB)")
    return df_local


# ============================================
# 2B) DATA AUGMENTATION (SIMULATED DATA, CLEARLY LABELED)
# ============================================
def augment_with_simulated_data(df: pd.DataFrame, n_per_gender: int = 100, random_seed: int = 42) -> pd.DataFrame:
    """
    Augments the real, cleaned dataset with SIMULATED purchase events, so the
    Chi-Square test has adequate statistical power (expected cell frequencies
    >= 5 per the standard rule of thumb). This is required because the
    platform currently has very few registered users.

    IMPORTANT - Methodology and transparency:
        - This does NOT modify, inflate, or replace the real dataset used for
          the descriptive analysis (see test_hypothesis_p6 on the real data).
          It creates a SEPARATE augmented copy, used ONLY for a secondary,
          clearly labeled robustness analysis.
        - Synthetic events are generated using a Bernoulli simulation seeded
          with each gender's REAL observed purchase rate (purchases / total
          events for that gender in the real, cleaned dataset). This means
          the simulation reproduces the real signal at a larger sample size,
          instead of fabricating an arbitrary or desired outcome.
        - A fixed random seed is used for full reproducibility.
        - Every output (script, report, slides) explicitly labels this as
          SIMULATED / AUGMENTED data, never merged silently with real events.

    Args:
        df: local enriched DataFrame (output of clean_and_augment_locally).
        n_per_gender: number of simulated events to generate per gender.
        random_seed: seed for reproducibility.

    Returns:
        A new DataFrame combining the real events with the simulated ones,
        with an added 'is_simulated' column (True/False) so the two sources
        can always be told apart.
    """
    rng = np.random.default_rng(random_seed)

    real = df.copy()
    real["is_simulated"] = False

    simulated_rows = []
    for gender, group in real.groupby("genero"):
        real_purchase_rate = (group["tipo_evento"] == "purchase").mean()
        simulated_events = rng.choice(
            ["purchase", "view"],
            size=n_per_gender,
            p=[real_purchase_rate, 1 - real_purchase_rate],
        )
        for event in simulated_events:
            simulated_rows.append({"genero": gender, "tipo_evento": event, "is_simulated": True})

    simulated_df = pd.DataFrame(simulated_rows)
    augmented_df = pd.concat([real, simulated_df], ignore_index=True)

    print(
        f"  \u26a0 AUGMENTED DATASET (simulated): added {len(simulated_df)} simulated events "
        f"({n_per_gender} per gender, seed={random_seed}), on top of {len(real)} real events. "
        f"Total augmented sample = {len(augmented_df)}. This is a SEPARATE, clearly labeled "
        f"dataset used only for the robustness analysis \u2014 the real dataset is unchanged."
    )
    return augmented_df


def build_contingency_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Builds the gender x action (purchase / no_purchase) contingency table
    required by the Chi-Square Test of Independence.

    Args:
        df: local enriched DataFrame, with 'genero' and 'tipo_evento' columns.

    Returns:
        DataFrame (contingency table) with genders as rows and
        columns ['purchase', 'no_purchase'].
    """
    data = df.copy()
    data["action"] = np.where(data["tipo_evento"] == "purchase", "purchase", "no_purchase")

    table = pd.crosstab(data["genero"], data["action"])

    for column in ["purchase", "no_purchase"]:
        if column not in table.columns:
            table[column] = 0

    return table[["purchase", "no_purchase"]]


# ============================================
# 4) RESEARCH QUESTION 6
# ============================================
def test_hypothesis_p6(df: pd.DataFrame) -> dict:
    """
    P6 (Bianca Acosta): Which gender makes more purchases on the platform?

    Hypothesis: There is no statistically significant difference in purchase
    volume based on gender (H0 of independence).

    Args:
        df: local enriched DataFrame (output of clean_and_augment_locally).

    Returns:
        Dictionary with summary, contingency table, statistics, and conclusion.
    """
    purchases = df[df["tipo_evento"] == "purchase"].copy()
    summary = purchases.groupby("genero").size().reset_index(name="total_purchases")
    summary["percentage"] = (
        summary["total_purchases"] / summary["total_purchases"].sum() * 100
    ).round(2)
    summary = summary.sort_values("total_purchases", ascending=False).reset_index(drop=True)

    contingency_table = build_contingency_table(df)
    chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

    reject_h0 = p_value < ALPHA

    # --- Robustness check: Fisher's Exact Test ---
    # The Chi-Square test is an asymptotic approximation that assumes expected
    # cell frequencies of at least 5. With a small sample (few registered
    # users), this assumption can be violated. Fisher's Exact Test computes
    # the exact probability instead of relying on that approximation, and is
    # the recommended alternative for small 2x2 contingency tables. It is
    # only defined for a 2x2 table (exactly two genders), so it is computed
    # only when that shape applies.
    fisher_p_value = None
    fisher_odds_ratio = None
    min_expected_frequency = float(expected.min())
    if contingency_table.shape == (2, 2):
        fisher_odds_ratio, fisher_p_value = fisher_exact(contingency_table.values)

    if reject_h0:
        conclusion = (
            "H0 is rejected: there is a statistically significant association "
            "between the student's gender and the probability of purchase "
            f"(p-value = {p_value:.6f} < alpha = {ALPHA})."
        )
    else:
        conclusion = (
            "H0 is not rejected: there is not enough statistical evidence to "
            "state that gender is associated with the probability of purchase "
            f"(p-value = {p_value:.6f} >= alpha = {ALPHA})."
        )

    result = {
        "summary": summary,
        "contingency_table": contingency_table,
        "expected_frequencies": pd.DataFrame(
            expected,
            index=contingency_table.index,
            columns=contingency_table.columns,
        ).round(2),
        "chi2_statistic": round(float(chi2_stat), 4),
        "p_value": float(p_value),
        "degrees_of_freedom": int(dof),
        "min_expected_frequency": round(min_expected_frequency, 2),
        "fisher_p_value": float(fisher_p_value) if fisher_p_value is not None else None,
        "fisher_odds_ratio": float(fisher_odds_ratio) if fisher_odds_ratio is not None else None,
        "alpha": ALPHA,
        "reject_h0": bool(reject_h0),
        "conclusion": conclusion,
    }

    print(f"  \u2713 P6 completed: {len(summary)} genders analyzed")
    print(f"  \u2713 Chi2 = {result['chi2_statistic']} | p-value = {p_value:.6f} | df = {dof}")
    print(f"  \u2022 Min expected cell frequency = {result['min_expected_frequency']} (rule of thumb: should be >= 5 for Chi-Square to be reliable)")
    if fisher_p_value is not None:
        print(f"  \u2022 Robustness check \u2014 Fisher's Exact Test: p-value = {fisher_p_value:.6f} (odds ratio = {fisher_odds_ratio:.4f})")
    h0_status = "\u2713 H0 rejected" if reject_h0 else "\u2717 H0 not rejected"
    print(f"  {h0_status} (alpha = {ALPHA})")

    return result


# ============================================
# 5) VISUALIZATION (LOCAL OUTPUT, FILE ONLY)
# ============================================
def generate_purchases_by_gender_chart(summary: pd.DataFrame, output_path: Path = None) -> Path:
    """
    Generates a chart with the total and proportion of purchases by gender
    and saves it as a local file at charts/purchases_by_gender.png. Nothing
    is sent or saved to the database.

    Args:
        summary: DataFrame [genero, total_purchases, percentage].
        output_path: optional path where the chart should be saved.

    Returns:
        Path of the generated image file.
    """
    if output_path is None:
        CHARTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = CHARTS_DIR / CHART_FILENAME

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    colors = plt.cm.Set2(np.linspace(0, 1, len(summary)))
    axes[0].bar(summary["genero"], summary["total_purchases"], color=colors)
    axes[0].set_title("Total purchases by gender")
    axes[0].set_xlabel("Gender")
    axes[0].set_ylabel("Number of purchases")
    axes[0].tick_params(axis="x", rotation=20)
    for i, value in enumerate(summary["total_purchases"]):
        axes[0].text(i, value, str(int(value)), ha="center", va="bottom")

    axes[1].pie(
        summary["total_purchases"],
        labels=summary["genero"],
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
    )
    axes[1].set_title("Proportion of purchases by gender")

    fig.suptitle("P6: Purchases by Gender", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"  \u2713 Chart saved to: {output_path}")
    return output_path


# ============================================
# 6) CSV EXPORT (LOCAL DISK ONLY, NOT THE DB)
# ============================================
def export_local_csv(result: dict, augmented_result: dict = None, csv_path: Path = CSV_PATH) -> Path:
    """
    Exports the P6 results to a CSV file on local disk. This is just a text
    file on your computer/repository: it involves no connection to, or write
    into, Supabase or any database.

    Saves the REAL data results first, and — if provided — the AUGMENTED
    (simulated) robustness results in a clearly separated, labeled section
    afterwards. The two are never merged into a single set of numbers.

    Args:
        result: dictionary returned by test_hypothesis_p6, computed on the
            real (non-simulated) dataset.
        augmented_result: optional dictionary returned by test_hypothesis_p6,
            computed on the augmented/simulated dataset (see
            augment_with_simulated_data). If provided, it's saved in a
            separate, explicitly labeled block.
        csv_path: local path where the CSV should be saved.

    Returns:
        Path of the generated CSV file.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    summary = result["summary"].copy()
    table = result["contingency_table"].reset_index()

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        f.write("# ========== REAL DATA (primary, authoritative result) ==========\n")
        f.write("# Summary: purchases by gender\n")
        summary.to_csv(f, index=False)
        f.write("\n# Contingency table (purchase vs no_purchase)\n")
        table.to_csv(f, index=False)
        f.write("\n# Statistical test\n")
        f.write(f"chi2_statistic,{result['chi2_statistic']}\n")
        f.write(f"p_value,{result['p_value']}\n")
        f.write(f"degrees_of_freedom,{result['degrees_of_freedom']}\n")
        f.write(f"alpha,{result['alpha']}\n")
        f.write(f"min_expected_frequency,{result['min_expected_frequency']}\n")
        f.write("\n# Robustness check: Fisher's Exact Test (recommended for small 2x2 samples)\n")
        f.write(f"fisher_p_value,{result['fisher_p_value']}\n")
        f.write(f"fisher_odds_ratio,{result['fisher_odds_ratio']}\n")

        if augmented_result is not None:
            f.write("\n\n# ========== AUGMENTED DATA (SIMULATED - secondary/robustness result) ==========\n")
            f.write("# WARNING: this section blends the real data with SIMULATED purchase events,\n")
            f.write("# seeded from each gender's real observed purchase rate, generated only to\n")
            f.write("# reach adequate statistical power. It does NOT represent real user behavior\n")
            f.write("# beyond what was actually observed. See augment_with_simulated_data() in\n")
            f.write("# bianca_analysis.py for the exact simulation method and random seed used.\n")
            aug_summary = augmented_result["summary"].copy()
            aug_table = augmented_result["contingency_table"].reset_index()
            f.write("\n# Summary: purchases by gender (augmented)\n")
            aug_summary.to_csv(f, index=False)
            f.write("\n# Contingency table (augmented)\n")
            aug_table.to_csv(f, index=False)
            f.write("\n# Statistical test (augmented)\n")
            f.write(f"chi2_statistic,{augmented_result['chi2_statistic']}\n")
            f.write(f"p_value,{augmented_result['p_value']}\n")
            f.write(f"degrees_of_freedom,{augmented_result['degrees_of_freedom']}\n")
            f.write(f"min_expected_frequency,{augmented_result['min_expected_frequency']}\n")
            f.write(f"fisher_p_value,{augmented_result['fisher_p_value']}\n")
            f.write(f"fisher_odds_ratio,{augmented_result['fisher_odds_ratio']}\n")

    print(f"  \u2713 Local CSV saved to: {csv_path}")
    return csv_path


# ============================================
# 7) BIANCA'S OWN STATISTICAL REPORT (INDIVIDUAL FILE)
# ============================================
def generate_bianca_report(result: dict, augmented_result: dict = None, report_path: Path = REPORT_PATH) -> Path:
    """
    Generates the P6 statistical report in Bianca's own file
    (BiancaAcostaProject/statistical_report_bianca.md), separate from other
    teammates' reports to avoid Git conflicts while each person works on
    their own module.

    Args:
        result: dictionary returned by test_hypothesis_p6, computed on the
            real (non-simulated) dataset. This is the primary, authoritative
            result.
        augmented_result: optional dictionary returned by test_hypothesis_p6,
            computed on the augmented/simulated dataset. If provided, it is
            included in a separate, clearly labeled section of the report.
        report_path: path of the individual report.

    Returns:
        Path of the generated report.
    """
    summary = result["summary"]
    table = result["contingency_table"]

    summary_rows = "\n".join(
        f"| {row.genero} | {row.total_purchases} | {row.percentage}% |"
        for row in summary.itertuples()
    )

    table_rows = "\n".join(
        f"| {gender} | {row['purchase']} | {row['no_purchase']} |"
        for gender, row in table.iterrows()
    )

    augmented_section = ""
    if augmented_result is not None:
        aug_summary_rows = "\n".join(
            f"| {row.genero} | {row.total_purchases} | {row.percentage}% |"
            for row in augmented_result["summary"].itertuples()
        )
        aug_table_rows = "\n".join(
            f"| {gender} | {row['purchase']} | {row['no_purchase']} |"
            for gender, row in augmented_result["contingency_table"].iterrows()
        )
        augmented_section = f"""
---

## Secondary Analysis: Data Augmentation (SIMULATED DATA)

> **Disclosure:** the platform currently has very few registered users, which
> limits the statistical power of the Chi-Square test on real data alone (see
> the minimum expected cell frequency above). To demonstrate the test with
> adequate power, this section blends the real, cleaned dataset with
> **simulated purchase events**, generated via a Bernoulli simulation seeded
> with each gender's **real observed purchase rate** (not an arbitrary or
> desired outcome). A fixed random seed guarantees reproducibility. This
> augmented result is a **secondary, clearly labeled robustness check** \u2014
> it does **not** replace or get merged with the real-data result above,
> which remains the primary, authoritative finding of this analysis. See
> `augment_with_simulated_data()` in `bianca_analysis.py` for the exact
> simulation method.

### Descriptive summary (augmented)

| Gender | Total purchases | Percentage |
|---|---|---|
{aug_summary_rows}

### Contingency table (augmented)

| Gender | Purchase | No Purchase |
|---|---|---|
{aug_table_rows}

### Statistical test result (augmented)

| Statistic | Value |
|---|---|
| Chi-Square (\u03c7\u00b2) | {augmented_result['chi2_statistic']} |
| Degrees of freedom | {augmented_result['degrees_of_freedom']} |
| p-value | {augmented_result['p_value']:.6f} |
| Minimum expected cell frequency | {augmented_result['min_expected_frequency']} |
| Fisher's Exact Test p-value | {f"{augmented_result['fisher_p_value']:.6f}" if augmented_result['fisher_p_value'] is not None else "N/A"} |

### Conclusion (augmented)
{augmented_result['conclusion']}
"""

    content = f"""# Individual Statistical Report - Bianca Acosta

## P6: Which gender makes more purchases on the platform?

**Author:** Bianca Acosta
**Run timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Hypotheses
- **H0:** Student gender and purchase action are independent.
- **H1:** Student gender and purchase action are associated.
- **Significance level (\u03b1):** {result['alpha']}

### Methodology
Chi-Square Test of Independence (`scipy.stats.chi2_contingency`) over the
gender x action (purchase / no_purchase) contingency table. Raw data was
extracted from Supabase (read-only) and cleaning/augmentation was performed
locally, in memory, without writing anything to the database.

## Primary Analysis: Real Data

### Descriptive summary

| Gender | Total purchases | Percentage |
|---|---|---|
{summary_rows}

### Contingency table (observed)

| Gender | Purchase | No Purchase |
|---|---|---|
{table_rows}

### Statistical test result

| Statistic | Value |
|---|---|
| Chi-Square (\u03c7\u00b2) | {result['chi2_statistic']} |
| Degrees of freedom | {result['degrees_of_freedom']} |
| p-value | {result['p_value']:.6f} |
| Minimum expected cell frequency | {result['min_expected_frequency']} |

### Robustness check: Fisher's Exact Test
The Chi-Square test is an asymptotic approximation that assumes expected cell
frequencies of at least 5. With a small sample, this assumption can be
violated, which can make the Chi-Square p-value unreliable. Fisher's Exact
Test computes the exact probability instead of relying on that approximation,
and is the recommended alternative for small 2x2 contingency tables.

| Statistic | Value |
|---|---|
| Fisher's Exact Test p-value | {f"{result['fisher_p_value']:.6f}" if result['fisher_p_value'] is not None else "N/A (table is not 2x2)"} |
| Odds ratio | {f"{result['fisher_odds_ratio']:.4f}" if result['fisher_odds_ratio'] is not None else "N/A"} |

### Conclusion (real data \u2014 primary finding)
{result['conclusion']}

![Purchases by gender](charts/{CHART_FILENAME})
{augmented_section}"""

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(content, encoding="utf-8")
    print(f"  \u2713 Individual report saved to: {report_path}")
    return report_path


# ============================================
# MAIN MODULE PIPELINE (INDEPENDENT)
# ============================================
def run_bianca_analysis(include_augmented: bool = True, n_per_gender: int = 100) -> dict:
    """
    Runs Bianca Acosta's full analytical module (P6), completely
    independently:
        1. Extracts raw data (read-only from Supabase).
        2. Cleans and enriches locally, in memory (without touching the DB).
        3. Runs the Chi-Square test on the REAL data (primary, authoritative result).
        4. Optionally runs the same test again on an AUGMENTED dataset that
           blends the real data with clearly labeled simulated events, seeded
           from the real observed purchase rates, to demonstrate the test
           with adequate statistical power (expected frequencies >= 5). This
           secondary result is always reported separately and explicitly
           marked as simulated \u2014 it never replaces or is mixed silently
           with the real result.
        5. Generates the chart and reports, all saved only to Bianca's own
           files.

    Args:
        include_augmented: whether to also run the augmented/simulated
            robustness analysis (step 4). Set to False to run only the real
            data analysis.
        n_per_gender: number of simulated events per gender for the
            augmented analysis.

    Returns:
        Dictionary with both the real and (if requested) augmented results,
        plus the generated file paths.
    """
    print("\n" + "=" * 50)
    print("ANALYTICAL MODULE - BIANCA ACOSTA (P6)")
    print("=" * 50)

    print("\n[1/5] Extracting raw data (read-only)...")
    raw_data = extract_raw_data()

    print("\n[2/5] Cleaning and enriching locally (in memory)...")
    df_local = clean_and_augment_locally(raw_data)

    print("\n[3/5] Computing P6 on REAL data (primary result)...")
    real_result = test_hypothesis_p6(df_local)

    augmented_result = None
    if include_augmented:
        print("\n[4/5] Computing P6 on AUGMENTED data (simulated robustness check)...")
        augmented_df = augment_with_simulated_data(df_local, n_per_gender=n_per_gender)
        augmented_result = test_hypothesis_p6(augmented_df)
    else:
        print("\n[4/5] Skipping augmented analysis (include_augmented=False)...")

    print("\n[5/5] Generating chart, CSV, and individual report (all local)...")
    chart_path = generate_purchases_by_gender_chart(real_result["summary"])
    csv_path = export_local_csv(real_result, augmented_result)
    report_path = generate_bianca_report(real_result, augmented_result)

    print("\n" + "=" * 50)
    print("P6 SUMMARY \u2014 REAL DATA (primary result)")
    print("=" * 50)
    print(real_result["summary"].to_string(index=False))
    print(f"\nChi2 = {real_result['chi2_statistic']} | p-value = {real_result['p_value']:.6f}")
    print(real_result["conclusion"])

    if augmented_result is not None:
        print("\n" + "=" * 50)
        print("P6 SUMMARY \u2014 AUGMENTED DATA (simulated, secondary/robustness result)")
        print("=" * 50)
        print(augmented_result["summary"].to_string(index=False))
        print(f"\nChi2 = {augmented_result['chi2_statistic']} | p-value = {augmented_result['p_value']:.6f}")
        print(augmented_result["conclusion"])

    real_result["chart_path"] = chart_path
    real_result["csv_path"] = csv_path
    real_result["report_path"] = report_path
    real_result["augmented_result"] = augmented_result
    return real_result


# ============================================
# EXECUTION
# ============================================
if __name__ == "__main__":
    p6_result = run_bianca_analysis()