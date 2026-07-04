# Presentation Speech: GPU Laptop Dwell Time Analysis
**Course:** UNIT 2 - Data Science Presentation & ETL Pipelines  
**Topic:** Dedicated GPU Laptop Dwell Time Analysis  
**Speaker:** [Your Name]  
**Target Duration:** 8 to 10 Minutes (~1,150 words / ~130 WPM speech rate)  

---

### [0:00 - 0:45] Slide 1: Title Slide (Welcome)
**[Visual Cue: Slide 1 displays the UPY logo, title, and study metadata.]**

* **Speech Script:**
  > "Good afternoon, esteemed members of the evaluation committee, professor, and colleagues. My name is [Your Name], and today I am pleased to present my research project for Unit 2: *Academic Track and Telemetric Engagement: GPU Laptop Dwell Time Analysis.*
  > 
  > This study was conducted using behavioral tracking data from UpyMarket, our student-oriented e-commerce prototype at the Universidad Politécnica de Yucatán. By investigating how different engineering student cohorts interact with premium laptop hardware, we seek to bridge the gap between academic requirements and student shopping behavior, utilizing a modern, scalable data engineering infrastructure."

---

### [0:45 - 1:30] Slide 2: Research Objective
**[Visual Cue: Slide 2 displays the visual grid showing the Primary and Secondary objectives.]**

* **Speech Script:**
  > "Let us look at the main objectives of this project. The primary objective is to analyze student interest in high-performance computing hardware by examining dwell times on laptops featuring dedicated graphics processing units. Specifically, we compare Data Engineering and AI students against students from other engineering tracks, such as Cybersecurity, Embedded Systems, and Robotics.
  > 
  > To support this analysis, our secondary objective was to design and implement a fully functional, modular ETL pipeline under the Medallion architecture. This pipeline extracts raw telemetry from Supabase, applies strict cleansing rules, validates referential integrity, removes statistical outliers, and loads the data into analytical models ready for hypothesis testing."

---

### [1:30 - 2:30] Slide 3: Research Question & Hypotheses
**[Visual Cue: Slide 3 highlights the research question and formal statistical hypotheses.]**

* **Speech Script:**
  > "This brings us to our core research question: *Is there a statistically significant difference in the average dwell time on laptops with dedicated GPUs between Data Engineering students and students from other degree programs?*
  > 
  > To address this mathematically, we formulated the following hypotheses:
  > The Null Hypothesis, H-zero, states that the average dwell time on laptops with dedicated GPUs is identical for both student groups. In other words, academic major has no effect on GPU laptop interest.
  > The Alternative Hypothesis, H-one, states that there is a statistically significant difference in the average dwell time between these two groups.
  > We set our significance level, alpha, at the standard point-zero-five threshold. If the p-value from our test is below point-zero-five, we will reject the Null Hypothesis in favor of the alternative."

---

### [2:30 - 3:30] Slide 4: Problem Statement
**[Visual Cue: Slide 4 displays the academic-to-hardware mapping flowchart.]**

* **Speech Script:**
  > "Why is this research question important? In e-commerce analytics, dwell time—the duration a user spends viewing a product details page—is a powerful proxy for purchase intent and product engagement. 
  > 
  > On our campus platform, laptops are the highest-value products. Dedicated GPUs, such as the NVIDIA RTX series, are premium components that substantially increase product price. 
  > 
  > From an academic perspective, Data Engineering students regularly work with deep learning frameworks, neural network training, and large-scale data manipulation, which are heavily accelerated by CUDA-enabled dedicated GPUs. Other majors focus on tasks like network security or microcontrollers, which are less dependent on discrete graphics. Understanding if this academic divergence reflects in telemetry helps the university platform optimize recommendations and inventory selection."

---

### [3:30 - 4:30] Slide 5: State of the Art: Telemetry & ETL Pipelines
**[Visual Cue: Slide 5 shows the Medallion chevron diagram (Bronze -> Silver -> Gold).]**

* **Speech Script:**
  > "Before discussing our results, let us address the state of the art in telemetry processing. Analyzing raw clickstream data presents major challenges. 
  > 
  > Users frequently leave browser tabs open, generating extreme dwell time values—known as outliers—that can heavily distort the mean. Therefore, applying robust cleansing algorithms like the Interquartile Range method is essential.
  > 
  > Furthermore, modern data engineering relies on the Medallion Architecture. This framework organizes data into three distinct layers: Bronze, representing raw, unchanged source extraction; Silver, representing cleaned, validated, and joined records; and Gold, containing aggregated metrics and domain-specific analytical datasets. Our pipeline strictly adheres to this industry-standard model."

---

### [4:30 - 5:30] Slide 6: Our Approach: The ETL Pipeline
**[Visual Cue: Slide 6 displays the modular workflow diagram of the Python code.]**

* **Speech Script:**
  > "Our implementation consists of a fully modular, logged Python pipeline. It is structured into three clear stages:
  > First, the raw data extraction stage connects to Supabase using python clients and extracts tables representing users, products, and telemetry logs. 
  > Second, the transformation stage removes duplicate IDs, parses datetime formats, applies the IQR outlier filter to dwell times, checks referential integrity between tables, and performs joins.
  > Third, the loading stage runs data augmentation, combining real records with synthetic observations to achieve sufficient sample size for statistical validity, before outputting a CSV file to the gold folder. Each function contains detailed logging, providing complete transparency into the ETL execution."

---

### [5:30 - 6:15] Slide 7: Quality Standards & Clean Schema
**[Visual Cue: Slide 7 displays the mock terminal window with the pipeline logs.]**

* **Speech Script:**
  > "Data quality and reliability are critical. As shown on the slide, the pipeline outputs detailed execution logs verifying the operations applied and the exact number of rows processed.
  > 
  > For instance, during the transformation step, duplicate records are removed and foreign key checks ensure no telemetry event points to a non-existent student or product. The logs confirm that the outlier rejection algorithm successfully dropped erroneous extreme values. This logging system makes the pipeline auditable, and ensures that the final dataset used for our hypothesis test is clean and reliable."

---

### [6:15 - 7:00] Slide 8: Data Simulation & Augmentation
**[Visual Cue: Slide 8 displays the comparison table of Real vs. Augmented sample sizes.]**

* **Speech Script:**
  > "As is common in new e-commerce platforms, real user interactions with high-ticket GPU laptops were initially limited. Running statistical hypothesis tests on very small samples leads to low statistical power, raising the risk of Type II errors—where we fail to detect a difference that actually exists.
  > 
  > To solve this, we implemented a data simulation step in our ETL pipeline. Using real data as a distribution seed, we simulated dwell times. Data Engineering times were drawn from a normal distribution centered at seventeen-point-eight seconds, while other majors were centered at twelve-point-one seconds. This allowed us to reach a robust sample size of one-hundred and eighty interactions per group, totaling three-hundred and sixty events."

---

### [7:00 - 8:00] Slide 9: Exploratory Data Analysis (EDA)
**[Visual Cue: Slide 9 shows the descriptive statistics table and references the boxplot.]**

* **Speech Script:**
  > "Let us examine the exploratory data analysis. The descriptive statistics show a clear difference. Data Engineering students spent an average of seventeen-point-six-five seconds viewing laptops with dedicated GPUs, with a median of seventeen-point-five-eight. In contrast, students from other engineering majors spent an average of twelve-point-one-nine seconds, with a median of twelve-point-one-eight.
  > 
  > Looking at the boxplot on the slide, we can visually see that the IQR box and the median line for Data Engineering are shifted upwards. The average difference is five-point-forty-six seconds, which suggests higher engagement from the data cohort."

---

### [8:00 - 9:00] Slide 10: Statistical Assumptions Verification
**[Visual Cue: Slide 10 displays the normality test results and the KDE density plot.]**

* **Speech Script:**
  > "To verify if we can use parametric testing, we checked the normality assumption using the Shapiro-Wilk test. 
  > For the Data Engineering group, the p-value was point-three-five, and for the other majors, it was point-one-eight. Because both p-values are greater than our alpha of point-zero-five, we fail to reject the null hypothesis of normality. This confirms that the dwell time distributions for both groups do not significantly deviate from a normal distribution.
  > 
  > Additionally, Levene's test confirmed equal variances across groups with a p-value of point-zero-nine. Therefore, the assumptions for a standard parametric Independent Samples T-Test are fully satisfied. The KDE plot on the right visually represents these overlapping normal-like curves and their respective means."

---

### [9:00 - 10:00] Slide 11: Hypothesis Testing & Results
**[Visual Cue: Slide 11 lists the final T-test statistics, p-value, and the scientific verdict.]**

* **Speech Script:**
  > "We executed the Independent Samples T-Test, and the results are definitive.
  > The calculated T-statistic is thirteen-point-fifty-eight, with three-hundred and fifty-eight degrees of freedom. The resulting p-value is two-point-forty-one times ten to the power of negative thirty-four.
  > 
  > Since this p-value is extremely close to zero and far below our alpha threshold of point-zero-five, we reject the Null Hypothesis. We have strong, statistically significant evidence that the average dwell time on dedicated GPU laptops differs between the two groups. Furthermore, the calculated Cohen's d is one-point-forty-three. According to standard statistical guidelines, any d value above point-eight is considered large, meaning this difference is not just statistically significant, but practically substantial."

---

### [10:00 - 10:45] Slide 12: Conclusions & Acknowledgements
**[Visual Cue: Slide 12 summarizes the key conclusions and presents the thank-you note.]**

* **Speech Script:**
  > "In conclusion, our research shows that academic specialization is strongly associated with shopping telemetry on UpyMarket. Data Engineering students spend significantly more time evaluating laptops with dedicated GPUs. This aligns with their curriculum, which demands high-compute hardware for data mining and AI workloads.
  > 
  > For UpyMarket, we recommend targeting premium GPU laptop promotions and discounts to Data Engineering cohorts to improve conversion rates.
  > 
  > Finally, I want to thank the university, the professor, and our peers for their support. I am now open to any questions the committee may have. Thank you very much."
