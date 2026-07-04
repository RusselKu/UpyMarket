# Reporte Estadístico Individual - Bianca Acosta

## P6: ¿Qué género realiza más compras en la plataforma?

**Autora:** Bianca Acosta
**Fecha de ejecución:** 2026-07-03 19:18:17

### Hipótesis
- **H0:** El género del estudiante y la acción de compra son independientes.
- **H1:** El género del estudiante y la acción de compra están asociados.
- **Nivel de significancia (α):** 0.05

### Metodología
Prueba de Chi-cuadrado de Independencia (`scipy.stats.chi2_contingency`) sobre
la tabla de contingencia género x acción (purchase / no_purchase). Los datos
crudos se extrajeron de Supabase (solo lectura) y la limpieza/aumentación se
realizó localmente, en memoria, sin escribir nada en la base de datos.

### Resumen descriptivo

| Género | Total de compras | Porcentaje |
|---|---|---|
| Masculino | 34 | 94.44% |
| Femenino | 2 | 5.56% |

### Tabla de contingencia (observada)

| Género | Purchase | No Purchase |
|---|---|---|
| Femenino | 2 | 5 |
| Masculino | 34 | 51 |

### Resultado de la prueba estadística

| Estadístico | Valor |
|---|---|
| Chi-cuadrado (χ²) | 0.0371 |
| Grados de libertad | 1 |
| p-value | 0.847218 |

### Conclusión
No se rechaza H0: no hay evidencia estadística suficiente para afirmar que el género esté asociado a la probabilidad de compra (p-value = 0.847218 >= alpha = 0.05).

![Compras por género](../charts/compras_por_genero.png)
