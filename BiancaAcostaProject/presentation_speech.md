# Presentation Speech: Purchases by Gender Analysis

**Course:** UNIT 2 - Data Science Presentation & ETL Pipelines  
**Topic:** Purchases by Gender on UpyMarket  
**Speaker:** Bianca Acosta  
**Target Duration:** **3-minute demo video + 6–7 minute presentation + 1–2 minute Q&A**

---

# [0:00 - 3:00] Demo Video

*(The demo video is played before the presentation, as required by the rubric.)*

### Speech Script

> "Good afternoon, professor and classmates. Before I begin my presentation, I'd like to show a short demonstration of my ETL pipeline running from data extraction to the statistical analysis."

*(Play the demo video.)*

---

# [3:00 - 3:25] Slide 1: Title

**[Visual Cue: Slide 1 displays the title, subtitle, and UPY logo.]**

### Speech Script

> "Good afternoon. My name is Bianca Acosta, and today I will present my analytical module for Project 06 of UpyMarket.
>
> My research focuses on one question: **Which gender makes more purchases on the platform?**
>
> To answer this question, I developed a modular ETL pipeline and analyzed the data using the Chi-Square Test of Independence."

---

# [3:25 - 4:00] Slide 2: Research Objectives

**[Visual Cue: Slide 2 displays the research objectives.]**

### Speech Script

> "This project has two main objectives.
>
> First, to determine whether student gender influences purchasing behavior on the UpyMarket platform.
>
> Second, to build a clean and reproducible ETL pipeline that extracts, cleans, and analyzes the data without modifying the shared database.
>
> The analysis uses four main variables: gender, event type, total purchases, and purchase percentage."

---

# [4:00 - 4:35] Slide 3: Research Question & Hypotheses

**[Visual Cue: Slide 3 highlights the research question and hypotheses.]**

### Speech Script

> "The research question is:
>
> **Which gender makes more purchases on the UpyMarket platform?**
>
> To answer it, I defined two hypotheses.
>
> The null hypothesis states that gender and purchasing behavior are independent.
>
> The alternative hypothesis states that they are associated.
>
> The significance level for this test is 0.05."

---

# [4:35 - 5:15] Slide 4: Problem Statement

**[Visual Cue: Slide 4 presents the problem and business context.]**

### Speech Script

> "UpyMarket records user interactions such as product views, add-to-cart actions, and purchases.
>
> Companies often use customer information to create marketing strategies.
>
> However, making decisions based on gender without statistical evidence can lead to incorrect conclusions.
>
> This analysis helps determine whether gender should actually be considered when making business decisions."

---

# [5:15 - 5:50] Slide 5: State of the Art

**[Visual Cue: Slide 5 displays the three main concepts.]**

### Speech Script

> "Previous studies show that gender usually affects the type of products people buy more than the total number of purchases.
>
> Small datasets can also produce misleading results.
>
> For this reason, the Chi-Square Test of Independence is commonly used to evaluate whether two categorical variables are truly related."

---

# [5:50 - 6:45] Slide 6: ETL Pipeline

**[Visual Cue: Slide 6 displays the ETL workflow.]**

### Speech Script

> "My ETL pipeline has four stages.
>
> First, it extracts data from the Supabase database in read-only mode.
>
> Second, it cleans the data by removing duplicates, validating the records, and joining each event with the user's gender.
>
> Third, it creates the contingency table and performs the Chi-Square Test.
>
> Finally, it generates charts, reports, and CSV files locally without modifying the shared database."

---

# [6:45 - 7:25] Slide 7: Exploratory Data Analysis

**[Visual Cue: Slide 7 displays the pie chart and descriptive statistics.]**

### Speech Script

> "After cleaning the data, I obtained 110 telemetry events from 15 users.
>
> There were 39 purchases in total.
>
> Male students made 37 purchases, which represents 94.87%.
>
> Female students made only 2 purchases, representing 5.13%.
>
> Although this looks like a large difference, descriptive statistics alone are not enough to reach a conclusion."

---

# [7:25 - 8:05] Slide 8: Statistical Test Results

**[Visual Cue: Slide 8 displays the Chi-Square results.]**

### Speech Script

> "Next, I performed the Chi-Square Test of Independence.
>
> The Chi-Square statistic was 0.0, and the p-value was 1.0.
>
> Since the p-value is greater than 0.05, I cannot reject the null hypothesis.
>
> Therefore, the available data does not show a statistically significant association between gender and purchasing behavior."

---

# [8:05 - 8:45] Slide 9: Interpretation & Limitations

**[Visual Cue: Slide 9 explains the sample size limitation.]**

### Speech Script

> "This does not mean that gender has no effect.
>
> It only means that the current dataset does not provide enough statistical evidence.
>
> The main limitation is the sample size.
>
> The analysis includes only 15 users, so a larger and more balanced dataset would produce more reliable results."

---

# [8:45 - 9:20] Slide 10: Conclusions

**[Visual Cue: Slide 10 summarizes the conclusions.]**

### Speech Script

> "In conclusion, I successfully developed a modular and read-only ETL pipeline.
>
> The descriptive analysis shows that most purchases were made by male students.
>
> However, the Chi-Square Test found no statistically significant relationship between gender and purchasing behavior.
>
> Future analyses should be repeated when more users and purchase data become available."

---

# [9:20 - 9:40] Slide 11: Acknowledgements

**[Visual Cue: Slide 11 displays the acknowledgements.]**

### Speech Script

> "Finally, I would like to thank my teammates for their collaboration, Rivaldo Canché for coordinating the analytical modules, and our professor for the guidance throughout this project.
>
> Thank you very much for your attention.
>
> I will be happy to answer your questions."

---

# Timing Summary

| Section | Duration |
|----------|---------:|
| Demo Video | 3:00 |
| Slide 1 | 0:25 |
| Slide 2 | 0:35 |
| Slide 3 | 0:35 |
| Slide 4 | 0:40 |
| Slide 5 | 0:35 |
| Slide 6 | 0:55 |
| Slide 7 | 0:40 |
| Slide 8 | 0:40 |
| Slide 9 | 0:40 |
| Slide 10 | 0:35 |
| Slide 11 | 0:20 |
| **Presentation** | **≈ 6:40** |
| **Questions** | **≈ 1–2 min** |

**Total defense time:** **Approximately 10–11 minutes (including the demo video and Q&A).**
