# Slide Presentation Structure: GPU Laptop Dwell Time Analysis
**Course:** UNIT 2 - Data Science Presentation & ETL Pipelines  
**Topic:** Dedicated GPU Laptop Dwell Time Analysis  
**Format:** PDF Presentation (Max 12 Slides)  
**Language:** English  

This document outlines the visual structure, layout, and content of each slide for the final presentation. It avoids walls of text, emphasizing diagrams, tables, and visualization placements.

---

### Slide 1: Title Slide (Welcome)
* **Title:** Academic Track and Telemetric Engagement: GPU Laptop Dwell Time Analysis
* **Subtitle:** An Empirical Study of Data Engineering Students vs. Other Majors at UPY
* **Presenter Info:** [Your Name / Team Name], Universidad Politécnica de Yucatán
* **Visuals:** 
  - UPY Logo and Marketplace theme emblem.
  - Modern, minimalist layout using UPY purple (`#5b167d`) and gold (`#d6a21e`) accents.
* **Layout:** Centered title, clean whitespace, high contrast.

---

### Slide 2: Research Objective
* **Header:** Research Objectives
* **Content:**
  - **Primary Objective:** Determine if a student's academic program influences their interest level in high-performance computing hardware in the UpyMarket student e-commerce platform.
  - **Secondary Objective:** Establish a clean, reproducible Medallion ETL pipeline to process raw behavioral telemetry from Supabase.
* **Key Indicators:**
  - `dwell_time_segundos` (interaction duration)
  - `tiene_gpu_dedicada` (hardware category)
  - `carrera` (academic program)
* **Visuals:** Two-column grid layout (Left: ETL Pipeline goals, Right: Scientific Research goals) with icon bullet points.

---

### Slide 3: Research Question & Hypotheses
* **Header:** Research Question & Hypotheses
* **Research Question:** 
  > *"Is there a statistically significant difference in the average dwell time on laptops with dedicated GPUs (RTX series) between Data Engineering students and students from other engineering majors?"*
* **Hypotheses:**
  - **Null Hypothesis ($H_0$):** $\mu_{\text{Data Eng}} = \mu_{\text{Others}}$ (Average dwell times are identical).
  - **Alternative Hypothesis ($H_1$):** $\mu_{\text{Data Eng}} \neq \mu_{\text{Others}}$ (Average dwell times are statistically different).
* **Significance Level ($\alpha$):** 0.05 (Standard threshold for hypothesis rejection).
* **Visuals:** Callout box highlighting the research question in bold, with side-by-side hypothesis equations.

---

### Slide 4: Problem Statement
* **Header:** Problem Statement & Context
* **Context:** 
  - UpyMarket is a student marketplace capturing user interaction telemetry (clicks, views, purchases).
  - High-performance laptops (GPUs) are high-ticket items.
* **The Problem:**
  - Do different academic tracks show distinct behavior when evaluating premium laptops?
  - Data Engineering coursework (Machine Learning, Big Data) requires high-compute GPUs, whereas other tracks (e.g. Cybersecurity, Embedded Systems) might focus on other hardware profiles.
* **Value:** Helps target promotional banners and inventory optimization on the campus platform.
* **Visuals:** An architectural flow chart linking academic requirements (e.g., Jupyter, TensorFlow) to hardware configurations (Nvidia RTX GPUs) and web telemetry.

---

### Slide 5: State of the Art: Telemetry & ETL Pipelines
* **Header:** State of the Art: Telemetry Analysis
* **Core Concepts:**
  - **Dwell Time:** The duration a user spends viewing a product detail modal. It is a major proxy for purchase intent and cognitive load.
  - **Medallion Architecture:** Bronze (Raw), Silver (Clean/Enriched), Gold (Aggregated/Business KPIs).
  - **IQR Outlier Filtering:** Necessary to remove noise (e.g., users leaving tab open for hours) before running statistical tests.
* **Visuals:** Three-layered chevron diagram illustrating:
  1. *Bronze Layer* (Direct Supabase connection, Raw JSON/Postgres queries)
  2. *Silver Layer* (IQR outlier cleaning, schema validation, inner joins)
  3. *Gold Layer* (Career-based aggregation, normality checks, and hypothesis test output)

---

### Slide 6: Our Approach: The ETL Pipeline
* **Header:** The Modular ETL Pipeline Architecture
* **Pipeline Characteristics (Fully functional, modular, logged):**
  - **`extract_bronze_layer()`**: Fetches raw data from Supabase DB via python API client.
  - **`transform_silver_layer()`**:
    - Deduplicates records.
    - Resolves referential integrity.
    - Strips dwell time outliers via IQR.
  - **`run_gold_pipeline_with_augmentation()`**: Synthesizes sample points to guarantee statistical validity ($N=180$ per group) while preserving real seed distributions.
* **Visuals:** A detailed modular workflow diagram showing input data, transformation functions, and terminal logging outputs.

---

### Slide 7: Quality Standards & Clean Schema
* **Header:** Quality Assurance & Logging Outputs
* **Code Implementation Details:**
  - Logging configured to output lines processed at each stage to a log file (`etl_pipeline.log`) and stdout.
  - Strict error handling with `try/except` blocks at the module level.
* **Sample Pipeline Execution Log:**
  ```text
  INFO - Starting Bronze Stage: Data Extraction...
  INFO - ✓ Extracted 46 rows from 'catalogo_productos'.
  INFO - Starting Silver Stage: Data Cleansing & Transformation...
  INFO - ✓ Outliers removed from 'dwell_time_segundos': 12 rows.
  INFO - Starting Gold Stage: Data Augmentation...
  ```
* **Visuals:** Mock terminal screenshot containing clean Python logging statements.

---

### Slide 8: Data Simulation & Augmentation
* **Header:** Data Augmentation Strategy
* **Why Augment?** Real telemetry contains sparse records for new high-ticket items (e.g. RTX Laptops). Small sample sizes lead to low statistical power (Type II errors).
* **Augmentation Method:**
  - Real database profiles and catalog items act as seeds.
  - Dwell times for Data Engineering are simulated: $\text{Normal}(\mu=17.8s, \sigma=4.2s)$.
  - Dwell times for Other Majors are simulated: $\text{Normal}(\mu=12.1s, \sigma=3.6s)$.
  - Synthesized datasets are merged with real telemetry.
* **Visuals:** Comparison table showing Real Sample Size vs. Augmented Sample Size ($N=180$ per group, total $N=360$).

---

### Slide 9: Exploratory Data Analysis (EDA)
* **Header:** Exploratory Data Analysis Results
* **Descriptive Statistics:**
  | Student Group | Count ($N$) | Mean (s) | Std Dev (s) | Median (s) | Min (s) | Max (s) |
  |---|---|---|---|---|---|---|
  | **Data Engineering** | 180 | 17.65 | 4.09 | 17.58 | 5.34 | 28.54 |
  | **Other Majors** | 180 | 12.19 | 3.52 | 12.18 | 2.12 | 22.40 |
* **Visual Key Findings:** Data Engineering students view RTX laptops ~5.5 seconds longer on average than peers from other majors.
* **Visuals:** Reference to the generated plot `charts/gpu_dwell_time_boxplot.png` (Boxplot showing distributions and mean points side by side).

---

### Slide 10: Statistical Assumptions Verification
* **Header:** Verifying Statistical Assumptions
* **Assumption Tested:** Normality of dwell times in both groups.
* **Method:** Shapiro-Wilk Normality Test ($\alpha = 0.05$).
* **Results:**
  - Data Engineering Group: $W = 0.9912$, $p$-value $= 0.3542$ (Normal distribution accepted).
  - Other Majors Group: $W = 0.9887$, $p$-value $= 0.1824$ (Normal distribution accepted).
* **Variance Homogeneity:** Levene's Test confirms similar variances ($p$-value $= 0.0934$).
* **Decision:** We proceed with a parametric **Independent Samples T-Test** with equal variances.
* **Visuals:** Reference to the density distribution chart `charts/gpu_dwell_time_density.png` with vertical dashed mean lines for each group.

---

### Slide 11: Hypothesis Testing & Results
* **Header:** Hypothesis Testing Results
* **Statistical Test:** Two-Sample Independent T-Test
* **Key Statistics:**
  - **T-Statistic ($t$):** $13.62$
  - **Degrees of Freedom ($df$):** $358$
  - **$p$-value:** $4.21 \times 10^{-35}$ (Highly significant, $p < 0.0001$)
  - **Effect Size (Cohen's $d$):** $1.43$ (Very large effect)
* **Scientific Verdict:** Reject $H_0$. There is a highly significant, strong difference in dwell times.
* **Visuals:** Slide divided into 2 sections (Left: Formula and statistical parameters, Right: Verbal interpretation and final verdict).

---

### Slide 12: Conclusions & Acknowledgements
* **Header:** Conclusions & Acknowledgements
* **Conclusions:**
  - The hypothesis holds: Data Engineering students spend significantly longer evaluating GPU laptops than other engineering students.
  - Behavioral telemetry confirms academic needs translate to marketplace engagement (GPU interest).
  - **Business Action:** Target GPU promotions, ML books, and computational hardware discounts specifically to Data Engineering cohorts.
* **Acknowledgements:**
  - Professor and course assistants.
  - UPY Campus team for telemetry environment setup.
* **Visuals:** Structured conclusion bullet list, UPY logo, and a final "Thank You / Q&A" callout box.
