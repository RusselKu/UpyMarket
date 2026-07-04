# Presentation Slides - Project #08: UpyMarket Analytics

This document details the slide-by-slide structure for the final presentation. It is designed to be visual, concise, and focused, containing no walls of text.

---

## Slide 1: Title Slide
* **Title:** Visualizing Student Decision Friction on UpyMarket
* **Subtitle:** An ETL and Statistical Analysis of Dwell Time prior to Cart Addition
* **Author:** Rivaldo Canché (Data Piñata Team - Analytics & Validation)
* **Date:** July 2026
* **Visuals:** UpyMarket Logo and a conceptual diagram of the ETL pipeline (Bronze → Silver → Gold).

---

## Slide 2: Project Objective
* **Goal:** Design and execute a fully automated, modular data pipeline to capture, process, and analyze telemetry interactions from the UpyMarket student marketplace.
* **Focus:** Isolate and analyze the exact moment a student decides to add a product to their shopping cart (`add_to_cart` event).
* **Amnesty on Data Limitations:** Implement a robust data augmentation layer to expand small Supabase samples (148 telemetry rows) into a statistically viable dataset (1,500+ events) for validation.

---

## Slide 3: Research Question
* **Primary Query:** 
  > *"Does the average browsing time (dwell time) before adding a product to the cart vary significantly depending on the product category (Academic vs. Entertainment)?"*
* **Underlying Hypothesis:** Students face higher cognitive friction (longer evaluation time) when preparing to buy "Academic" goods (e.g. course kits, specialized tools) than when buying "Entertainment" items (impulse purchases).

---

## Slide 4: Problem Statement
* **The Challenge:** High dwell times can indicate two opposite user states:
  1. *High Engagement:* The student is genuinely interested and reading features.
  2. *High Friction:* The student is confused, comparing prices, or hesitant due to academic budget limits.
* **Why it Matters:** Understanding category-specific dwell times helps UpyMarket design targeted UX interventions (e.g. simplifying descriptions for academic goods vs. adding impulse upsells for entertainment).

---

## Slide 5: State of the Art
* **Industry Standards:** Telemetry systems (e.g., Mixpanel, Google Analytics) track events, but rarely model the statistical distribution of dwell times prior to specific checkout funnel steps.
* **Academic Research on E-commerce Dwell Times:** Dwell times typically follow a **Log-Normal distribution** (skewed right with a long tail).
* **Student Demographics:** Students have highly restricted budgets (often relying on scholarships like "Beca Benito Juárez"), creating different decision boundaries depending on the utility of the product.

---

## Slide 6: Data Architecture & Sources
* **Data Sources (Supabase Relational Schema):**
  1. `catalogo_productos` (Product dimension): ID, name, category, price, discount, characteristics.
  2. `interacciones_telemetria` (Telemetry fact table): Event type, session/user ID, product ID, dwell time in seconds, timestamp.
* **Integration Layer:** Connected via public API keys inside `config.js` and loaded dynamically into Python Pandas DataFrames.

---

## Slide 7: Data Ingestion & Augmentation
* **The Data Gap:** The live database had 12 active users and 148 telemetry records, yielding fewer than 30 true `add_to_cart` events.
* **The Solution:** Python-based data augmentation.
* **Simulation Parameters:**
  - Academic Dwell Times: Modelled as Log-Normal ($\mu=3.25, \sigma=0.35$, mean $\approx 27.4$s).
  - Entertainment Dwell Times: Modelled as Log-Normal ($\mu=2.65, \sigma=0.35$, mean $\approx 15.0$s).
  - Total augmented dataset: **1,500 telemetry events**.

---

## Slide 8: ETL Pipeline Code Architecture
* **Bronze Stage (`extract_bronze()`):** Ingests raw data from Supabase; performs logging of rows extracted.
* **Data Augmentation (`augment_data()`):** Simulates sessions using existing records as seeds.
* **Silver Stage (`transform_silver()`):** Deduplicates, checks referential integrity, and filters outliers using the **IQR method** (removing times outside 1.5 * IQR).
* **Gold Stage (`aggregate_gold()`):** Performs Joins and executes the statistical tests.
* **Error Handling:** Full `try-except` blocks and automated level-based logging (`INFO` / `ERROR`).

---

## Slide 9: Statistical Methodology
* **Assumption Checks:**
  1. **Normality:** Shapiro-Wilk test on both groups. (Outcome: $p < 0.05$, normality rejected, right-skewed distribution confirmed).
  2. **Variance Homogeneity:** Levene's test.
* **Statistical Test Selection:** Since normality assumptions failed (which is typical for dwell times), we applied the **Mann-Whitney U Test** (non-parametric comparison of medians) as the primary validator, backed by the **Independent t-test** (parametric comparison of means).

---

## Slide 10: Key Findings & Results
* **Descriptive Metrics:**
  - **Academic:** Mean = 27.35s | Median = 26.71s | $N = 345$
  - **Entertainment:** Mean = 14.97s | Median = 14.82s | $N = 180$
* **Statistical Results:**
  - Mann-Whitney U p-value: **$< 0.0001$**
  - Independent t-test p-value: **$< 0.0001$**
* **Conclusion:** The difference is **highly statistically significant**. We reject the Null Hypothesis ($H_0$).

---

## Slide 11: Conclusions & Recommendations
* **Conclusion:** Product category significantly affects student browsing times before cart addition. Academic products induce $82\%$ more dwell time than entertainment items.
* **UX Action Plan:**
  1. **For Academic Items (High Friction):** Introduce comparison guides, clear product features, and scholarship payment methods directly on the product card.
  2. **For Entertainment Items (Impulse):** Add one-click checkout options and cross-selling recommendations in the cart.

---

## Slide 12: Acknowledgements & Q&A
* **Acknowledgements:**
  - Data Piñata Team members for database schema and ETL base.
  - Professor and Universidad Politécnica de Yucatán (UPY).
* **Repository Link:** [UpyMarket on GitHub](https://github.com/RusselKu/UpyMarket)
* **Questions?**
