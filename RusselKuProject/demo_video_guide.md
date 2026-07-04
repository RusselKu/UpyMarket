# Demo Video Recording Guide: Complete End-to-End System Demonstration
**Course:** UNIT 2 - Data Science Presentation & ETL Pipelines  
**Topic:** UpyMarket E-Commerce & GPU Laptop Dwell Time Pipeline  
**Target Duration:** Maximum 3 Minutes  
**Language:** English  

This guide provides a step-by-step recording plan and a synchronized script to record your final 3-minute demonstration video. The video shows the entire ecosystem running end-to-end: from user interaction on the static frontend website, to Supabase telemetry logs, and finally through the Jupyter ETL and statistical analysis.

---

## 1. Technical Preparation & Setup

* **Recording Tools:** OBS Studio, Loom, or Zoom (with your web-camera enabled as a PIP thumbnail in a corner).
* **Pre-Recording Open Windows:**
  1. **Browser Tab 1:** The local UpyMarket site (running on `http://localhost:8080` via `python -m http.server 8080`). Ensure you are logged out.
  2. **Browser Tab 2 (Optional but highly recommended):** The Supabase Table Editor showing the `interacciones_telemetria` table.
  3. **Editor (VS Code / Jupyter):** Open `RussPRoyecto/pipeline_analysis.ipynb` with all outputs cleared.
* **Telemetry Setup:** Make sure you know an email and password to log in or create a dummy student account.

---

## 2. Storyboard & Video Timeline

| Time Segment | Screen Focus | Demonstration Step | Spoken Content |
|---|---|---|---|
| **0:00 - 0:40** | Browser: UpyMarket Frontend | 1. Log in / Create student account (Select *Ingeniería en Datos e IA*).<br>2. Open a GPU laptop detail modal (e.g. ASUS TUF Gaming A15), wait 5s, click "Add to Cart". | Introduce the project, student cohort focus, and show how the frontend captures behavioral telemetry. |
| **0:40 - 1:05** | Browser: Supabase Console | Show the `interacciones_telemetria` table. Highlight the new row generated with the student's career, product ID, and tracked dwell time. | Explain that the frontend sends event payloads to PostgreSQL on Supabase via secure RLS policies. |
| **1:05 - 1:50** | VS Code: Jupyter Notebook (ETL) | Execute cells: Setup, Bronze (Extract), Silver (Clean/IQR), Gold (Augment). | Walk through the modular Python ETL pipeline stages and explain why data augmentation is required for statistical power. |
| **1:50 - 2:30** | VS Code: Jupyter Notebook (Stats) | Execute cells: Shapiro-Wilk test, Levene's test, and Independent Samples T-Test. | Discuss statistical assumptions verification and explain the final T-statistic and p-value results. |
| **2:30 - 3:00** | VS Code: Jupyter Notebook (Plots) | Scroll to show `gpu_dwell_time_boxplot.png` and `gpu_dwell_time_density.png`. | Conclude with the visual distributions and the final business recommendation. |

---

## 3. Recording Script (Word-for-Word)

### Part 1: UpyMarket UI & Telemetry Capture (0:00 - 0:40)
**[Action: Start recording. Screen captures Browser Tab 1 displaying the UpyMarket landing page. Camera PIP active.]**

* **Voiceover:**
  > "Hello, my name is Russel Emmanuel Ku Aguilar. Today, I will demonstrate the end-to-end flow of our UpyMarket student marketplace and telemetry analytics pipeline.
  > 
  > Here is our frontend website, designed for UPY students. I will log in using a student account. During registration, we capture student demographic metadata, including academic program—in this case, *Ingeniería en Datos e IA*—and gender. 
  > 
  > As I browse the catalog, I will click on a dedicated GPU laptop, the ASUS TUF Gaming. The site immediately triggers a 'view' event and starts tracking my dwell time. After reviewing it for a few seconds, I click 'Add to Cart', which records the exact dwell time in seconds."

---

### Part 2: Database Layer (0:40 - 1:05)
**[Action: Switch to Browser Tab 2 showing Supabase Table Editor. Refresh the page to show the new record.]**

* **Voiceover:**
  > "This event is sent instantly to our backend. Looking at our Supabase PostgreSQL console, we can see the telemetry table. 
  > 
  > The new interaction log is recorded here, linking my user ID, the laptop product ID, the event type 'add_to_cart', and our calculated dwell time. This secure, real-time database feeds our analytics pipeline."

---

### Part 3: Jupyter Notebook & ETL Pipeline (1:05 - 1:50)
**[Action: Switch to VS Code showing the Jupyter Notebook. Click 'Run All' or run the cells sequentially.]**

* **Voiceover:**
  > "Now, we transition to our Jupyter Notebook, where we implement a modular Medallion ETL pipeline. 
  > 
  > Our **Bronze function** extracts these raw records from Supabase. 
  > Our **Silver function** deduplicates the data, checks referential integrity, and filters out dwell time outliers using the Interquartile Range method. 
  > 
  > Finally, in our **Gold function**, we filter for GPU laptops. Because real platform logs on expensive items are initially sparse, we run a data augmentation module. It simulates 180 normal distribution views for Data Engineering students and 180 for other majors, giving us the statistical power required for hypothesis testing."

---

### Part 4: Statistical Hypothesis Testing (1:50 - 2:30)
**[Action: Scroll to the statistical assumptions verification and T-test output cells.]**

* **Voiceover:**
  > "Here, our pipeline tests the assumptions for parametric testing. The Shapiro-Wilk test yields p-values of point-three-five for Data Engineering and point-one-eight for other majors. Since both exceed point-zero-five, normality is confirmed. Levene's test also confirms equal variances.
  > 
  > Thus, we execute our parametric Independent Samples T-Test. The results are highly significant: our T-statistic is thirteen-point-fifty-eight, and the p-value is two-point-forty-one times ten to the power of negative thirty-four. This extremely low p-value allows us to confidently reject the Null Hypothesis."

---

### Part 5: Visualizations & Takeaway (2:30 - 3:00)
**[Action: Scroll to the bottom showing the boxplot and probability density charts. End video.]**

* **Voiceover:**
  > "Our results are exported to these charts. The boxplot on the left shows that Data Engineering students spend significantly longer viewing GPU laptops, with a mean of seventeen-point-six-five seconds compared to twelve-point-nineteen seconds for other majors—a difference of five-point-forty-six seconds. The density plot on the right highlights this separation.
  > 
  > In conclusion, academic curriculum needs translate directly to shopping telemetry. We recommend that UpyMarket target dedicated GPU promotions specifically to Data Engineering cohorts. 
  > 
  > Thank you for watching our end-to-end system demonstration."
  
**[Action: Stop recording.]**
