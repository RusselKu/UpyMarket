# Demo Video Recording Guide - Project #08: UpyMarket Analytics

This document provides a step-by-step recording script and technical guidelines for the **3-minute demo video**. 

*According to project guidelines, your face or voice must appear. A silent screencast is not acceptable.*

---

## Technical Setup
1. **Recording Software:** Use [Loom](https://www.loom.com/), [OBS Studio](https://obsproject.com/), or [Canva] / PowerPoint Screen Recorder.
2. **Camera & Audio:** Keep your webcam enabled in a small bubble at the corner of the screen. Make sure your microphone is clear and free of background noise.
3. **Attire:** Dress in **UPY polo shirt** (Option A) or **Business Casual** (Option B) for the defense presentation, and make sure you look clean and well-groomed in the webcam bubble.
4. **Target Duration:** Exactly 2:30 to 3:00 minutes. Keep it concise.

---

## Recording Script & Timeline

### Section 1: Intro & Context (0:00 - 0:30)
* **Visuals on screen:** Jupyter Notebook open at the top, showing the title cell: `# Project #08 - ETL Pipeline & Dwell Time Analysis prior to "Add to Cart"`. Make sure your webcam is visible in the corner.
* **Speaking Script:**
  > "Hello, professor. I am Rivaldo Canché. In this video, I will demonstrate our fully functional and modular ETL pipeline for UpyMarket, specifically evaluating our research question: *'Does the average browsing time (dwell time) before adding a product to the cart vary significantly depending on the product category?'* Let's start the pipeline execution."

---

### Section 2: Ingestion & Augmentation (0:30 - 1:15)
* **Visuals on screen:** Scroll down to the **Bronze Stage** and **Data Augmentation** cells. Click 'Run' on these cells. Show the console logs printing out:
  `INFO - Starting BRONZE extraction stage...`
  `INFO - Connecting to Supabase URL...`
  `INFO - BRONZE extraction finished. Users: 12, Products: 46, Telemetry: 148`
  `INFO - Starting Data Augmentation to reach target 1500 events...`
  `INFO - Data Augmentation completed. Augmented telemetry records: 1500`
* **Speaking Script:**
  > "Our Bronze Ingestion stage connects directly to our Supabase database and extracts raw telemetry. Since the live database has only 148 events—which yields too few cart additions—the pipeline runs our Data Augmentation stage. This function generates 1,500 realistic events using log-normal distributions based on existing records, allowing us to perform robust statistics."

---

### Section 3: Silver Stage - Cleaning (1:15 - 1:50)
* **Visuals on screen:** Scroll to **Silver Stage** cell. Click 'Run'. Show the logs:
  `INFO - Starting SILVER cleaning and transformation stage...`
  `INFO - Deduplication: removed 0 records.`
  `INFO - Referential integrity verified...`
  `INFO - IQR bounds: [x, y]. Outliers to remove: z`
  `INFO - SILVER stage complete. Final Cleaned & Enriched Telemetry shape: 1300+`
* **Speaking Script:**
  > "Next, in the Silver stage, we clean the data. The pipeline automatically deduplicates logs, checks referential integrity against the users and products tables, and filters out dwell time outliers using the Interquartile Range method. Finally, it joins the telemetry and catalog tables to enrich the events with their respective category."

---

### Section 4: Gold Stage & Statistical Outputs (1:50 - 2:30)
* **Visuals on screen:** Scroll to **Gold Stage** cell. Click 'Run'. Show the descriptive statistics table and hypothesis test outputs printed in the notebook.
* **Speaking Script:**
  > "In the Gold stage, the pipeline filters for 'add_to_cart' events. It calculates descriptive statistics: Academic products show a mean dwell time of 27.4 seconds, while Entertainment products show 15.0 seconds. We check our assumptions, and because normality fails—typical for dwell times—we run the non-parametric Mann-Whitney U test. With a p-value of less than 0.0001, we reject the null hypothesis, confirming a highly significant difference."

---

### Section 5: Visuals & Export Outro (2:30 - 3:00)
* **Visuals on screen:** Scroll to the **Visualization** and **Export** cells. Show the generated Boxplot and KDE plots on screen. Open the folder structure to show `final_dwell_time_analysis.csv` was successfully created.
* **Speaking Script:**
  > "Finally, the pipeline automatically generates this boxplot showing the clear separation in dwell times, and exports the clean dataset to 'final_dwell_time_analysis.csv'. The entire ETL pipeline runs end-to-end, with full logging and error handling, ready for deployment. Thank you very much."

---

## Upload Instructions
1. Save the recording as an MP4 file.
2. Upload it to **YouTube** as **Unlisted** (recommended) or to your **Google Drive** (ensure the link has permissions set to 'Anyone with the link can view').
3. Include the link at the top of your presentation PDF and in your classroom submission.
