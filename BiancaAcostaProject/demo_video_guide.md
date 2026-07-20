# Demo Video Recording Guide: Complete End-to-End System Demonstration

**Course:** UNIT 2 - Data Science Presentation & ETL Pipelines  
**Topic:** UpyMarket P6 – Purchases by Gender Analysis  
**Presenter:** Bianca Acosta  
**Target Duration:** Maximum 3 Minutes  
**Language:** English

---

# Open Before Recording

- UpyMarket website
- Supabase Dashboard
- VS Code (`scripts/ETL/Gold/bianca_analysis.py`)
- Terminal at the project root
- BiancaAcostaProject folder (chart, CSV, and report)

---

# Video Timeline

| Time | Screen | Demonstration |
|-------|--------|---------------|
| 0:00–0:20 | UpyMarket | Introduce the project |
| 0:20–0:40 | UpyMarket | Show where telemetry data comes from |
| 0:40–1:00 | Supabase | Show the database tables |
| 1:00–1:20 | VS Code | Present the ETL pipeline |
| 1:20–2:20 | Terminal | Run the complete ETL pipeline |
| 2:20–2:50 | Output Files | Show the generated results |
| 2:50–3:00 | Terminal | Closing statement |

---

# Recording Script

---

## Part 1 – Introduction (0:00–0:20)

**Screen**

UpyMarket homepage.

### Voice

> "Hello, I'm Bianca Acosta.
>
> This video demonstrates my analytical module for Project 06 of UpyMarket.
>
> My research question is: Which gender makes more purchases on the platform?
>
> I'll show the complete process from the platform, to the database, the ETL pipeline, and finally the generated results."

---

## Part 2 – UpyMarket Platform (0:20–0:40)

**Screen**

Navigate through the platform.

Show:

- Home page
- Product catalog
- Product details
- User interactions

### Voice

> "This is the UpyMarket platform.
>
> Students can browse products, view product details, add items to the cart, and make purchases.
>
> Every interaction generates telemetry data, which is later analyzed by my ETL pipeline."

---

## Part 3 – Supabase Database (0:40–1:00)

**Screen**

Supabase Dashboard.

Show:

- usuarios_sesion
- interacciones_telemetria

### Voice

> "All telemetry is stored in Supabase.
>
> My analysis reads information from the **usuarios_sesion** and **interacciones_telemetria** tables.
>
> The connection is completely read-only, so the pipeline never modifies the shared database."

---

## Part 4 – ETL Pipeline (1:00–1:20)

**Screen**

VS Code.

Show the four main functions.

### Voice

> "This is my ETL pipeline.
>
> It is divided into four stages.
>
> First, it extracts the data from Supabase.
>
> Then, it cleans and enriches the information in memory.
>
> Next, it performs the Chi-Square Test of Independence.
>
> Finally, it generates the output files.
>
> Each stage records its execution using logging."

---

## Part 5 – Running the Pipeline (1:20–2:20)

**Screen**

Terminal.

Run:

```bash
python scripts/ETL/Gold/bianca_analysis.py
```

### Voice

> "Now I'll execute the pipeline.
>
> First, it connects to Supabase and extracts the raw data.
>
> Next, it removes duplicates, validates the records, filters invalid data, and joins each event with the user's gender.
>
> Then, it performs the Chi-Square Test of Independence.
>
> Finally, it generates the chart, the CSV file, and the statistical report locally."

---

## Part 6 – Generated Results (2:20–2:50)

**Screen**

Open:

- purchases_by_gender.png
- resultados_p6_bianca.csv
- statistical_report_bianca.md

### Voice

> "These are the generated results.
>
> The chart shows the purchase distribution by gender.
>
> The CSV contains the descriptive statistics and contingency table.
>
> Finally, the markdown report summarizes the methodology, the statistical test, and the final conclusion."

---

## Part 7 – Closing (2:50–3:00)

**Screen**

Terminal.

### Voice

> "The entire pipeline runs successfully without modifying the shared database.
>
> All generated files are stored only inside my local project folder.
>
> Thank you."

---

# Final Checklist

- [ ] Show the UpyMarket platform.
- [ ] Show the Supabase database.
- [ ] Show the ETL pipeline.
- [ ] Execute the pipeline without cuts.
- [ ] Show the generated chart.
- [ ] Show the generated CSV.
- [ ] Show the generated report.
- [ ] Total duration under 3 minutes.
