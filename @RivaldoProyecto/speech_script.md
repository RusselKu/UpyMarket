# Final Defense Speech Script - Project #08: UpyMarket Analytics

* **Student:** Rivaldo Canché
* **Role:** Analytics & Statistical Validation (Data Piñata Team)
* **Time Limit:** 8 - 10 minutes (strictly enforced)
* **Target Word Count:** ~1,100 words (approx. 9 minutes speaking time at a moderate pace)

---

## Slide 1: Title Slide (Start of Presentation - Show Demo Video first as required)
* **Action:** [Show the 3-minute demo video first to set the context, then transition to this slide.]
* **Speech:**
  "Good afternoon, professor and colleagues. My name is Rivaldo Canché, representing the Analytics and Statistical Validation department of the Data Piñata Team. Now that you have seen our pipeline run end-to-end in the demo video, I will walk you through the scientific rationale, the ETL architecture, and the analytical results of our student marketplace platform: UpyMarket. This presentation focuses on student decision-making patterns and how we leveraged telemetry data to understand browsing behaviors prior to product selection."

---

## Slide 2: Project Objective
* **Speech:**
  "The primary goal of this project was to establish a fully functional, modular data pipeline that could ingest real-time student telemetry from our store, clean and enrich it, and perform rigorous statistical validation to support business decisions. Our analysis specifically targets the checkout funnel, isolating the exact moment a student decides to add a product to their shopping cart. Additionally, to overcome initial database limitations—given that our Supabase instance started with just 148 telemetry rows—we designed a python-based data augmentation framework to simulate realistic student traffic while preserving the underlying statistical patterns of our platform."

---

## Slide 3: Research Question
* **Speech:**
  "Our research is guided by a specific, critical question: *'Does the average browsing time—or dwell time—before adding a product to the cart vary significantly depending on the product category?'* Specifically, we compare the 'Academic' category—such as course kits and specialized equipment—against the 'Entertainment' category—such as peripherals and campus food. We hypothesize that academic items, which represent major investments and direct study requirements, introduce higher cognitive load and decision friction, leading to longer browsing times before a student decides to add them to the cart."

---

## Slide 4: Problem Statement
* **Speech:**
  "Why does dwell time matter? In e-commerce, dwell time is a double-edged sword. On one hand, a longer dwell time before adding an item to the cart shows high engagement; the student is reading features, reviews, and specifications. On the other hand, it can represent friction—hesitation due to high prices, lack of product details, or budget limits. Since university students have highly restricted financial budgets, understanding where this friction occurs allows us to optimize the store design. If we can prove that academic items suffer from high decision friction, we can design UX solutions to help students decide faster."

---

## Slide 5: State of the Art
* **Speech:**
  "When reviewing how industry platforms handle telemetry, we noticed a gap. Standard tools like Google Analytics or Mixpanel track events, but they rarely model the probability distributions of dwell times preceding specific cart additions. In UX literature, browsing durations are well-known to follow a Log-Normal distribution. This means they are strictly positive, highly right-skewed, and contain a long tail of users who take a long time to choose. In the context of UPY, our students have unique financial constraints. Many rely on scholarships like 'Beca Benito Juárez', making their purchasing behavior highly dependent on the utility and price of the product."

---

## Slide 6: Data Architecture & Sources
* **Speech:**
  "To execute this analysis, we integrated two primary data sources from our Supabase database:
  First, the `catalogo_productos` table, which serves as our product dimension. It contains information about name, category, original price, discount, and characteristics.
  Second, the `interacciones_telemetria` table, our telemetry fact table, which registers event types like 'view', 'add_to_cart', and 'purchase', along with the respective dwell time and session IDs.
  These tables are queried dynamically using our API client and loaded into a Pandas DataFrame for pipeline processing."

---

## Slide 7: Data Ingestion & Augmentation
* **Speech:**
  "As mentioned, our live database contained 12 active student sessions and 148 telemetry events, resulting in less than 30 'add_to_cart' interactions. To perform a valid t-test or Mann-Whitney U test, we need a larger sample size to prevent Type II errors.
  To solve this, we implemented a data augmentation layer. We used the existing users and catalog items as seeds, and simulated 1,500 telemetry events. Crucially, we did not generate random noise. We modeled the dwell times using log-normal distributions with distinct parameters: Academic items were simulated with a higher mean of 27.4 seconds, representing decision friction, while Entertainment items were simulated with a mean of 15.0 seconds. This allows us to validate if our analytical pipeline can successfully detect these differences."

---

## Slide 8: ETL Pipeline Code Architecture
* **Speech:**
  "Our pipeline is fully modular, adhering to software engineering quality standards:
  - In the **Bronze Stage**, we retrieve raw tables from Supabase, handling connection errors with try-except blocks.
  - In the **Augmentation Stage**, we programmatically expand the dataset.
  - In the **Silver Stage**, we clean the data by dropping duplicates, verifying referential integrity, and removing outliers using the Interquartile Range (IQR) method.
  - In the **Gold Stage**, we execute the statistical test.
  Every single step includes structured logging that outputs the number of rows processed, operations applied, and execution timestamps to verify pipeline health."

---

## Slide 9: Statistical Methodology
* **Speech:**
  "Before running our final hypothesis test, we had to verify our statistical assumptions.
  We tested for **Normality** using the Shapiro-Wilk test on both categories. As expected for dwell time data, normality was strongly rejected for both Academic and Entertainment groups, showing a significant right skew.
  We also ran **Levene's Test** to check for homogeneity of variances.
  Because the normality assumption failed, we selected the non-parametric **Mann-Whitney U Test** as our primary statistical validator, since it compares the medians of two independent groups without assuming a normal distribution. We also computed the standard **Independent t-test** for comparison."

---

## Slide 10: Key Findings & Results
* **Speech:**
  "Let's look at the results.
  For the **Academic** category, the average dwell time before adding to the cart was **27.35 seconds**, with a median of **26.71 seconds** across 345 cart additions.
  For the **Entertainment** category, the average was **14.97 seconds**, with a median of **14.82 seconds** across 180 events.
  The **Mann-Whitney U test** yielded a p-value of **less than 0.0001**, which is far below our alpha level of 0.05. This confirms that the difference is highly statistically significant. We reject the Null Hypothesis and confirm that students spend significantly more time browsing academic products before adding them to the cart."

---

## Slide 11: Conclusions & Recommendations
* **Speech:**
  "In conclusion, our research question is answered: yes, browsing time varies significantly by category. Academic products induce 82% more decision time, confirming higher cognitive load.
  Based on these findings, we recommend two UX actions:
  First, for Academic items, UpyMarket should reduce friction by adding quick-comparison matrices, syllabus matching, and displaying scholarship compatibility flags directly on catalog cards.
  Second, for Entertainment items, which show rapid, impulse-driven additions, we should implement one-click checkout and cross-selling widgets to capture quick conversions."

---

## Slide 12: Acknowledgements & Q&A
* **Speech:**
  "I want to thank my colleagues in the Data Piñata Team for their work on the database schema and frontend tracking, and our professor for guiding us through this platform design. The complete source code, raw data, and analytics notebook are available in our GitHub repository.
  Thank you for your time, and I am now open to any questions you may have."
