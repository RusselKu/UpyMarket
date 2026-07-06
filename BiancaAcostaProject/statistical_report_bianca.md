# Individual Statistical Report - Bianca Acosta

## P6: Which gender makes more purchases on the platform?

**Author:** Bianca Acosta
**Run timestamp:** 2026-07-05 21:47:42

### Hypotheses
- **H0:** Student gender and purchase action are independent.
- **H1:** Student gender and purchase action are associated.
- **Significance level (α):** 0.05

### Methodology
Chi-Square Test of Independence (`scipy.stats.chi2_contingency`) over the
gender x action (purchase / no_purchase) contingency table. Raw data was
extracted from Supabase (read-only) and cleaning/augmentation was performed
locally, in memory, without writing anything to the database.

### Descriptive summary

| Gender | Total purchases | Percentage |
|---|---|---|
| Masculino | 37 | 94.87% |
| Femenino | 2 | 5.13% |

### Contingency table (observed)

| Gender | Purchase | No Purchase |
|---|---|---|
| Femenino | 2 | 5 |
| Masculino | 37 | 66 |

### Statistical test result

| Statistic | Value |
|---|---|
| Chi-Square (χ²) | 0.0 |
| Degrees of freedom | 1 |
| p-value | 1.000000 |

### Conclusion
H0 is not rejected: there is not enough statistical evidence to state that gender is associated with the probability of purchase (p-value = 1.000000 >= alpha = 0.05).

![Purchases by gender](charts/purchases_by_gender.png)
