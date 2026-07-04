"""
Módulo Analítico Individual - Bianca Acosta
=============================================
Propósito: Responder la Pregunta de Investigación 6 (P6) y validar su hipótesis
mediante una prueba de Chi-cuadrado de Independencia.

Pregunta de Investigación 6 (P6):
    ¿Qué género realiza más compras en la plataforma?

Hipótesis:
    H0: El género del estudiante y la acción de compra son independientes
        (no hay asociación significativa entre género y compra).
    H1: El género del estudiante y la acción de compra están asociados
        (el género influye de forma significativa en la probabilidad de comprar).

Metodología:
    Prueba de Chi-cuadrado de Independencia (scipy.stats.chi2_contingency)
    sobre la tabla de contingencia género x acción (purchase / no_purchase).

IMPORTANTE - Alcance de este módulo:
    Este script es completamente independiente y de solo lectura respecto a la
    base de datos:
      1. SOLO LEE de Supabase (extracción cruda, sin modificar nada).
      2. NO hace drop, delete, update ni upsert de ningún tipo.
      3. La limpieza/"aumentación" (dedupe, validación, enriquecimiento con
         JOINs) se hace en memoria, únicamente para este análisis.
      4. Los resultados (gráfico + reporte) se generan y guardan solo en
         archivos propios de Bianca, sin tocar el pipeline ni el reporte
         compartido del equipo. Esto evita conflictos de Git con los demás
         módulos individuales (rivaldo_analysis.py, etc.).

Autora: Bianca Acosta
Equipo: Analítica y Validación Estadística
"""

from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Backend sin interfaz gráfica, apto para servidores/CI
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

# ============================================
# RUTAS DEL PROYECTO (SOLO SALIDA LOCAL DE BIANCA)
# ============================================
ROOT_DIR = Path(__file__).resolve().parents[3]
CHARTS_DIR = ROOT_DIR / "charts"
REPORT_PATH = ROOT_DIR / "db" / "statistical_report_bianca.md"  # archivo propio, no compartido
CSV_PATH = ROOT_DIR / "db" / "resultados_p6_bianca.csv"  # export local, no se manda a la DB
CHART_FILENAME = "compras_por_genero.png"

ALPHA = 0.05  # Nivel de significancia (95% de confianza)


# ============================================
# 1) EXTRACCIÓN (SOLO LECTURA)
# ============================================
def extraer_datos_crudos() -> dict:
    """
    Extrae los datos crudos necesarios directamente desde Supabase,
    reutilizando el extractor de Bronze del equipo (solo lectura, sin
    modificar nada en la base de datos).

    Returns:
        dict con los DataFrames crudos: usuarios_sesion, interacciones_telemetria
    """
    import sys
    sys.path.append(str(ROOT_DIR))
    from scripts.ETL.Bronze.raw_data import run_bronze_pipeline

    raw_data = run_bronze_pipeline()
    return raw_data


# ============================================
# 2) LIMPIEZA Y AUMENTACIÓN LOCAL (SOLO EN MEMORIA)
# ============================================
def limpiar_y_enriquecer_local(raw_data: dict) -> pd.DataFrame:
    """
    Realiza la limpieza y el enriquecimiento (aumentación) necesarios para
    P6, únicamente en memoria y solo para este análisis.

    No modifica ni elimina nada en la base de datos: no hace drop, delete,
    update ni upsert. Solo transforma copias locales de los DataFrames
    crudos ya extraídos.

    Args:
        raw_data: dict con 'usuarios_sesion' e 'interacciones_telemetria' crudos.

    Returns:
        DataFrame local enriquecido con las columnas 'genero' y 'tipo_evento',
        listo para el análisis de P6.
    """
    usuarios = raw_data["usuarios_sesion"].copy()
    telemetria = raw_data["interacciones_telemetria"].copy()

    # --- Limpieza de usuarios (en memoria) ---
    usuarios = usuarios.drop_duplicates(subset=["id"], keep="first")
    usuarios = usuarios.dropna(subset=["genero"])

    # --- Limpieza de telemetría (en memoria) ---
    telemetria = telemetria.drop_duplicates(subset=["id"], keep="first")
    eventos_validos = ["view", "add_to_cart", "purchase"]
    telemetria = telemetria[telemetria["tipo_evento"].isin(eventos_validos)]

    # --- Integridad referencial: solo eventos de usuarios válidos ---
    telemetria = telemetria[telemetria["usuario_id"].isin(set(usuarios["id"]))]

    # --- Aumentación: enriquecer telemetría con el género del usuario ---
    df_local = telemetria.merge(
        usuarios[["id", "genero"]],
        left_on="usuario_id",
        right_on="id",
        how="inner",
        suffixes=("", "_usuario"),
    ).drop(columns=["id_usuario"], errors="ignore")

    print(f"  ✓ Dataset local de Bianca listo: {len(df_local)} eventos (solo en memoria)")
    return df_local


# ============================================
# 3) PREPARACIÓN PARA LA PRUEBA ESTADÍSTICA
# ============================================
def construir_tabla_contingencia(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construye la tabla de contingencia género x acción (purchase / no_purchase)
    requerida por la prueba de Chi-cuadrado de Independencia.

    Args:
        df: DataFrame local enriquecido, con columnas 'genero' y 'tipo_evento'.

    Returns:
        DataFrame (tabla de contingencia) con géneros como filas y
        columnas ['purchase', 'no_purchase'].
    """
    datos = df.copy()
    datos["accion"] = np.where(datos["tipo_evento"] == "purchase", "purchase", "no_purchase")

    tabla = pd.crosstab(datos["genero"], datos["accion"])

    for columna in ["purchase", "no_purchase"]:
        if columna not in tabla.columns:
            tabla[columna] = 0

    return tabla[["purchase", "no_purchase"]]


# ============================================
# 4) PREGUNTA DE INVESTIGACIÓN 6
# ============================================
def pregunta_6_compras_genero(df: pd.DataFrame) -> dict:
    """
    P6 (Bianca Acosta): ¿Qué género realiza más compras en la plataforma?

    Hipótesis: No existe una diferencia estadísticamente significativa en el
    volumen de compras en función del género (H0 de independencia).

    Args:
        df: DataFrame local enriquecido (salida de limpiar_y_enriquecer_local).

    Returns:
        Diccionario con resumen, tabla de contingencia, estadísticos y conclusión.
    """
    compras = df[df["tipo_evento"] == "purchase"].copy()
    resumen = compras.groupby("genero").size().reset_index(name="total_compras")
    resumen["porcentaje"] = (
        resumen["total_compras"] / resumen["total_compras"].sum() * 100
    ).round(2)
    resumen = resumen.sort_values("total_compras", ascending=False).reset_index(drop=True)

    tabla_contingencia = construir_tabla_contingencia(df)
    chi2_stat, p_value, dof, expected = chi2_contingency(tabla_contingencia)

    rechaza_h0 = p_value < ALPHA

    if rechaza_h0:
        conclusion = (
            "Se rechaza H0: existe una asociación estadísticamente significativa "
            "entre el género del estudiante y la probabilidad de compra "
            f"(p-value = {p_value:.6f} < alpha = {ALPHA})."
        )
    else:
        conclusion = (
            "No se rechaza H0: no hay evidencia estadística suficiente para afirmar "
            "que el género esté asociado a la probabilidad de compra "
            f"(p-value = {p_value:.6f} >= alpha = {ALPHA})."
        )

    resultado = {
        "resumen": resumen,
        "tabla_contingencia": tabla_contingencia,
        "expected_frequencies": pd.DataFrame(
            expected,
            index=tabla_contingencia.index,
            columns=tabla_contingencia.columns,
        ).round(2),
        "chi2_statistic": round(float(chi2_stat), 4),
        "p_value": float(p_value),
        "grados_libertad": int(dof),
        "alpha": ALPHA,
        "rechaza_h0": bool(rechaza_h0),
        "conclusion": conclusion,
    }

    print(f"  ✓ P6 completada: {len(resumen)} géneros analizados")
    print(f"  ✓ Chi2 = {resultado['chi2_statistic']} | p-value = {p_value:.6f} | gl = {dof}")
    print(f"  {'✓ Se rechaza H0' if rechaza_h0 else '✗ No se rechaza H0'} (alpha = {ALPHA})")

    return resultado


# ============================================
# 5) VISUALIZACIÓN (SALIDA LOCAL, SOLO ARCHIVO)
# ============================================
def generar_grafico_compras_genero(resumen: pd.DataFrame, output_path: Path = None) -> Path:
    """
    Genera un gráfico con el total y la proporción de compras por género y lo
    guarda como archivo local en charts/compras_por_genero.png. No se envía
    ni se guarda nada a la base de datos.

    Args:
        resumen: DataFrame [genero, total_compras, porcentaje].
        output_path: Ruta opcional donde guardar el gráfico.

    Returns:
        Path del archivo de imagen generado.
    """
    if output_path is None:
        CHARTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = CHARTS_DIR / CHART_FILENAME

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    colores = plt.cm.Set2(np.linspace(0, 1, len(resumen)))
    axes[0].bar(resumen["genero"], resumen["total_compras"], color=colores)
    axes[0].set_title("Total de compras por género")
    axes[0].set_xlabel("Género")
    axes[0].set_ylabel("Número de compras")
    axes[0].tick_params(axis="x", rotation=20)
    for i, valor in enumerate(resumen["total_compras"]):
        axes[0].text(i, valor, str(int(valor)), ha="center", va="bottom")

    axes[1].pie(
        resumen["total_compras"],
        labels=resumen["genero"],
        autopct="%1.1f%%",
        colors=colores,
        startangle=90,
    )
    axes[1].set_title("Proporción de compras por género")

    fig.suptitle("P6: Compras por Género", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"  ✓ Gráfico guardado en: {output_path}")
    return output_path


# ============================================
# 6) EXPORT A CSV (SOLO DISCO LOCAL, NO DB)
# ============================================
def exportar_csv_local(resultado: dict, csv_path: Path = CSV_PATH) -> Path:
    """
    Exporta los resultados de P6 a un archivo CSV en disco local. Esto es
    solo un archivo de texto en tu computadora/repositorio: no involucra
    ninguna conexión ni escritura a Supabase ni a ninguna base de datos.

    Guarda dos bloques en el mismo CSV:
        1. El resumen de compras por género (con porcentaje).
        2. La tabla de contingencia usada en la prueba de Chi-cuadrado.

    Args:
        resultado: Diccionario retornado por pregunta_6_compras_genero.
        csv_path: Ruta local donde guardar el CSV.

    Returns:
        Path del archivo CSV generado.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    resumen = resultado["resumen"].copy()
    tabla = resultado["tabla_contingencia"].reset_index()

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        f.write("# Resumen: compras por genero\n")
        resumen.to_csv(f, index=False)
        f.write("\n# Tabla de contingencia (purchase vs no_purchase)\n")
        tabla.to_csv(f, index=False)
        f.write("\n# Prueba estadistica\n")
        f.write(f"chi2_statistic,{resultado['chi2_statistic']}\n")
        f.write(f"p_value,{resultado['p_value']}\n")
        f.write(f"grados_libertad,{resultado['grados_libertad']}\n")
        f.write(f"alpha,{resultado['alpha']}\n")

    print(f"  ✓ CSV local guardado en: {csv_path}")
    return csv_path


# ============================================
# 7) REPORTE ESTADÍSTICO PROPIO (ARCHIVO INDIVIDUAL)
# ============================================
def generar_reporte_bianca(resultado: dict, report_path: Path = REPORT_PATH) -> Path:
    """
    Genera el reporte estadístico de P6 en un archivo propio de Bianca
    (db/statistical_report_bianca.md), separado del de otros integrantes
    para evitar conflictos de Git al trabajar cada quien en su módulo.

    Args:
        resultado: Diccionario retornado por pregunta_6_compras_genero.
        report_path: Ruta del reporte individual.

    Returns:
        Path del reporte generado.
    """
    resumen = resultado["resumen"]
    tabla = resultado["tabla_contingencia"]

    filas_resumen = "\n".join(
        f"| {row.genero} | {row.total_compras} | {row.porcentaje}% |"
        for row in resumen.itertuples()
    )

    filas_tabla = "\n".join(
        f"| {genero} | {fila['purchase']} | {fila['no_purchase']} |"
        for genero, fila in tabla.iterrows()
    )

    contenido = f"""# Reporte Estadístico Individual - Bianca Acosta

## P6: ¿Qué género realiza más compras en la plataforma?

**Autora:** Bianca Acosta
**Fecha de ejecución:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Hipótesis
- **H0:** El género del estudiante y la acción de compra son independientes.
- **H1:** El género del estudiante y la acción de compra están asociados.
- **Nivel de significancia (α):** {resultado['alpha']}

### Metodología
Prueba de Chi-cuadrado de Independencia (`scipy.stats.chi2_contingency`) sobre
la tabla de contingencia género x acción (purchase / no_purchase). Los datos
crudos se extrajeron de Supabase (solo lectura) y la limpieza/aumentación se
realizó localmente, en memoria, sin escribir nada en la base de datos.

### Resumen descriptivo

| Género | Total de compras | Porcentaje |
|---|---|---|
{filas_resumen}

### Tabla de contingencia (observada)

| Género | Purchase | No Purchase |
|---|---|---|
{filas_tabla}

### Resultado de la prueba estadística

| Estadístico | Valor |
|---|---|
| Chi-cuadrado (χ²) | {resultado['chi2_statistic']} |
| Grados de libertad | {resultado['grados_libertad']} |
| p-value | {resultado['p_value']:.6f} |

### Conclusión
{resultado['conclusion']}

![Compras por género](../charts/{CHART_FILENAME})
"""

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(contenido, encoding="utf-8")
    print(f"  ✓ Reporte individual guardado en: {report_path}")
    return report_path


# ============================================
# PIPELINE PRINCIPAL DEL MÓDULO (INDEPENDIENTE)
# ============================================
def run_bianca_analysis() -> dict:
    """
    Ejecuta el módulo analítico completo de Bianca Acosta (P6), de forma
    totalmente independiente:
        1. Extrae datos crudos (solo lectura de Supabase).
        2. Limpia y enriquece localmente, en memoria (sin tocar la DB).
        3. Corre la prueba de Chi-cuadrado.
        4. Genera el gráfico y el reporte, ambos guardados solo en archivos
           propios de Bianca.

    Returns:
        Diccionario con los resultados de la prueba y las rutas generadas.
    """
    print("\n" + "=" * 50)
    print("MÓDULO ANALÍTICO - BIANCA ACOSTA (P6)")
    print("=" * 50)

    print("\n[1/4] Extrayendo datos crudos (solo lectura)...")
    raw_data = extraer_datos_crudos()

    print("\n[2/4] Limpiando y enriqueciendo localmente (en memoria)...")
    df_local = limpiar_y_enriquecer_local(raw_data)

    print("\n[3/4] Calculando P6: Compras por género...")
    resultado = pregunta_6_compras_genero(df_local)

    print("\n[4/4] Generando gráfico, CSV y reporte individual (todo local)...")
    chart_path = generar_grafico_compras_genero(resultado["resumen"])
    csv_path = exportar_csv_local(resultado)
    report_path = generar_reporte_bianca(resultado)

    print("\n" + "=" * 50)
    print("RESUMEN P6")
    print("=" * 50)
    print(resultado["resumen"].to_string(index=False))
    print(f"\nChi2 = {resultado['chi2_statistic']} | p-value = {resultado['p_value']:.6f}")
    print(resultado["conclusion"])

    resultado["chart_path"] = chart_path
    resultado["csv_path"] = csv_path
    resultado["report_path"] = report_path
    return resultado


# ============================================
# EJECUCIÓN
# ============================================
if __name__ == "__main__":
    resultado_p6 = run_bianca_analysis()