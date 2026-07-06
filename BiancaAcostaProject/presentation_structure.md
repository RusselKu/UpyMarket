# Slide Presentation Structure: Purchases by Gender Analysis

**Course:** UNIT 2 - Data Science Presentation & ETL Pipelines  
**Topic:** Purchases by Gender on UpyMarket  
**Format:** PDF Presentation (Max 12 Slides)  
**Language:** English

This document outlines the visual structure, layout, and content of each slide for the final presentation. It avoids walls of text, emphasizing diagrams, tables, and visualization placements.

---

## Slide 1: Title Slide (Welcome)

- **Title:** Which Gender Makes More Purchases on the Platform?
- **Subtitle:** An Empirical Analysis of Purchase Behavior by Gender Using the Chi-Square Test of Independence
- **Presenter Info:** Bianca Acosta, Universidad Politécnica de Yucatán

### Visuals
- UPY logo and UpyMarket emblem.
- Modern, minimalist layout using dark teal (`#0B2E33`) with mint (`#02C39A`) accents.
- High-contrast white typography.

### Layout
Centered title, clean whitespace, author information at the bottom.

---

## Slide 2: Research Objectives

### Header
**Research Objectives**

### Content

**Primary Objective**
- Determine whether student gender influences purchasing behavior within the UpyMarket student e-commerce platform.

**Secondary Objective**
- Develop a clean, reproducible, read-only ETL pipeline that extracts, transforms, and analyzes purchase telemetry without modifying the shared database.

**Key Indicators**
- `genero`
- `tipo_evento`
- `total_purchases`
- Purchase percentage by gender

### Visuals
Two-column grid layout:

- **Left:** ETL Pipeline Goals
- **Right:** Scientific Research Goals

Use icon bullet points for each objective.

---

## Slide 3: Research Question & Hypotheses

### Header
**Research Question & Hypotheses**

### Research Question

> *"Which gender makes more purchases on the UpyMarket platform?"*

### Hypotheses

- **Null Hypothesis ($H_0$):** Student gender and purchase behavior are independent.
- **Alternative Hypothesis ($H_1$):** Student gender and purchase behavior are associated.

### Significance Level

- **$\alpha$ = 0.05**

### Visuals
- Large callout box highlighting the research question.
- Side-by-side hypothesis cards.

---

## Slide 4: Problem Statement

### Header
**Problem Statement & Context**

### Context

- UpyMarket records user interactions including views, cart additions, and completed purchases.
- Understanding purchasing behavior helps improve marketing decisions.

### The Problem

- Should promotions be segmented according to gender?
- Are observed purchase differences statistically meaningful or simply due to sampling variability?

### Value

Determines whether gender-based personalization is supported by statistical evidence before making business decisions.

### Visuals

Architectural flow diagram:

**Student → Telemetry → ETL Pipeline → Statistical Test → Business Decision**

---

## Slide 5: State of the Art: Telemetry & Statistical Analysis

### Header
**State of the Art: Purchase Behavior Analysis**

### Core Concepts

#### Purchase Telemetry
Purchasing events provide valuable behavioral information for understanding customer decisions.

#### Chi-Square Test of Independence
The standard statistical method for evaluating relationships between categorical variables.

#### Medallion Architecture
Bronze → Silver → Gold processing enables reproducible analytics workflows.

### Visuals

Three-layer chevron diagram illustrating:

1. Bronze Layer
2. Silver Layer
3. Gold Layer

---

## Slide 6: Our Approach: The ETL Pipeline

### Header
**The Modular ETL Pipeline Architecture**

### Pipeline Characteristics (Fully Functional, Modular, Logged)

#### `extract_raw_data()`
- Reads `usuarios_sesion`
- Reads `interacciones_telemetria`
- Read-only operations

#### `clean_and_augment_locally()`
- Removes duplicates
- Validates gender values
- Filters invalid records
- Performs in-memory joins

#### `test_hypothesis_p6()`
- Builds contingency table
- Executes Chi-Square Test (`chi2_contingency`)

#### Local Output
Generates:
- CSV
- Markdown report
- Charts

All outputs are saved only inside Bianca's local project directory.

### Visuals

Four-stage ETL workflow diagram connected with arrows and logging outputs.

---

## Slide 7: Quality Standards & Logging Outputs

### Header
**Quality Assurance & Logging Outputs**

### Code Implementation Details

- Logging enabled throughout every ETL stage.
- Read-only interaction with Supabase.
- Modular implementation with exception handling.

### Sample Pipeline Execution Log

```text
INFO - Starting Extraction Stage...
INFO - ✓ Users extracted: 15
INFO - ✓ Telemetry extracted: 158

INFO - Starting Cleaning Stage...
INFO - ✓ Events after cleaning: 110

INFO - Starting Gold Stage...
INFO - ✓ Purchase statistics generated.
INFO - ✓ Chi-Square Test completed.
```

### Visuals

Mock terminal screenshot displaying log outputs.

---

## Slide 8: Exploratory Data Analysis (EDA)

### Header
**Exploratory Data Analysis Results**

### Descriptive Statistics

| Gender | Purchases | Percentage |
|---------|----------:|-----------:|
| Male | 37 | 94.87% |
| Female | 2 | 5.13% |

### Visual Key Findings

Within the cleaned dataset, male students account for nearly all recorded purchases.

### Visuals

- Pie chart
- Percentage callout cards
- Reference to the generated visualization

---

## Slide 9: Statistical Assumptions & Test

### Header
**Statistical Test Results**

### Statistical Method

Chi-Square Test of Independence

### Results

- **Chi-Square Statistic ($\chi^2$):** 0.0
- **Degrees of Freedom:** 1
- **p-value:** 1.000
- **Significance Level ($\alpha$):** 0.05

### Decision

The null hypothesis is **not rejected**.

There is **no statistically significant association** between gender and purchasing behavior.

### Visuals

Four statistical cards showing:

- Chi-Square Statistic
- Degrees of Freedom
- p-value
- α

Followed by a highlighted conclusion card.

---

## Slide 10: Hypothesis Testing Interpretation

### Header
**Interpretation & Limitations**

### Interpretation

Although males represent **94.87%** of purchases, statistical testing indicates that this observed difference is **not statistically significant**.

### Main Limitation

- Only **15 users**
- **110** cleaned telemetry events
- Limited statistical power

### Recommendation

Repeat the analysis using a larger and more balanced dataset to obtain stronger statistical evidence.

### Visuals

Split layout:

**Left**
- Sample size limitations

**Right**
- Correct interpretation of the hypothesis test

---

## Slide 11: Conclusions & Acknowledgements

### Header
**Conclusions & Acknowledgements**

### Conclusions

- A fully traceable, read-only ETL pipeline was successfully implemented.
- Male students accounted for **94.87%** of observed purchases.
- The Chi-Square Test found no statistically significant association between gender and purchasing behavior.
- Larger datasets are recommended for future analyses.

### Acknowledgements

- Course professor.
- UPY Data Engineering Team.
- UpyMarket development team.

### Visuals

- Structured conclusion bullet list.
- UPY logo.
- Final **"Thank You / Q&A"** callout box.
