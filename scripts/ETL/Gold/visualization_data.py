"""
ETL Pipeline - Gold Layer (Aggregated & Business Metrics)
==========================================================
Propósito: Generar métricas de negocio y responder preguntas de investigación.
Responsabilidades:
    - Agregar datos por dimensiones clave (carrera, género, categoría)
    - Calcular KPIs y métricas estadísticas
    - Responder a las 8 preguntas del proyecto
    - Generar tablas listas para dashboard y reportes
    
Equipo: Analítica y Validación Estadística
"""

import pandas as pd
import numpy as np
from datetime import datetime


# ============================================
# PREGUNTAS DE INVESTIGACIÓN
# ============================================

def pregunta_1_dias_compra(df: pd.DataFrame) -> pd.DataFrame:
    """
    P1 (Rama): ¿En qué días de la semana se hacen más compras?
    
    Hipótesis: Los estudiantes compran más en fines de semana.
    
    Args:
        df: DataFrame enriquecido (Silver)
        
    Returns:
        DataFrame con conteo de compras por tipo de día
        Columnas: es_fin_de_semana, total_compras
    """
    compras = df[df['tipo_evento'] == 'purchase'].copy()
    
    resultado = compras.groupby('es_fin_de_semana').size().reset_index(name='total_compras')
    resultado['es_fin_de_semana'] = resultado['es_fin_de_semana'].map({
        True: 'Fin de semana',
        False: 'Entre semana'
    })
    
    print(f"  ✓ P1 completada: {len(resultado)} categorías de días")
    return resultado


def pregunta_2_gpu_carrera(df: pd.DataFrame) -> pd.DataFrame:
    """
    P2 (Russel): ¿Qué carreras pasan más tiempo viendo equipos con GPU?
    
    Hipótesis: Sistemas Embebidos y Game Development tienen mayor dwell time.
    
    Args:
        df: DataFrame enriquecido (Silver)
        
    Returns:
        DataFrame con promedio de dwell_time por carrera y GPU
        Columnas: carrera, tiene_gpu_dedicada, promedio_dwell_time_segundos
    """
    views_gpu = df[
        (df['tipo_evento'] == 'view') & 
        (df['dwell_time_segundos'].notna())
    ].copy()
    
    resultado = views_gpu.groupby(['carrera', 'tiene_gpu_dedicada']).agg({
        'dwell_time_segundos': 'mean'
    }).reset_index()
    
    resultado = resultado.rename(columns={'dwell_time_segundos': 'promedio_dwell_time_segundos'})
    resultado['promedio_dwell_time_segundos'] = resultado['promedio_dwell_time_segundos'].round(2)
    
    print(f"  ✓ P2 completada: {len(resultado)} combinaciones carrera-GPU")
    return resultado


def pregunta_3_gasto_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """
    P3 (Edgardo): ¿En qué categoría gastan más: Académico o Entretenimiento?
    
    Hipótesis: Mayor gasto en categoría Académico.
    
    Args:
        df: DataFrame enriquecido (Silver)
        
    Returns:
        DataFrame con suma de gasto por categoría
        Columnas: categoria_general, total_gastado, numero_compras
    """
    compras = df[df['tipo_evento'] == 'purchase'].copy()
    
    resultado = compras.groupby('categoria_general').agg({
        'precio_pagado': ['sum', 'count']
    }).reset_index()
    
    resultado.columns = ['categoria_general', 'total_gastado', 'numero_compras']
    resultado['total_gastado'] = resultado['total_gastado'].round(2)
    
    print(f"  ✓ P3 completada: {len(resultado)} categorías")
    return resultado


def pregunta_4_descuentos_conversion(df: pd.DataFrame) -> pd.DataFrame:
    """
    P4 (Damian Novelo): ¿Los descuentos >= 15% aumentan la conversión?
    
    Hipótesis: Productos con descuento >= 15% tienen mayor tasa de conversión.
    
    Args:
        df: DataFrame enriquecido (Silver)
        
    Returns:
        DataFrame con tasa de conversión por nivel de descuento
        Columnas: tiene_descuento_alto, total_views, total_purchases, tasa_conversion
    """
    # Crear columna de descuento alto (>= 15%)
    df['tiene_descuento_alto'] = df['porcentaje_descuento'] >= 0.15
    
    # Contar views y purchases por nivel de descuento
    views = df[df['tipo_evento'] == 'view'].groupby('tiene_descuento_alto').size().reset_index(name='total_views')
    purchases = df[df['tipo_evento'] == 'purchase'].groupby('tiene_descuento_alto').size().reset_index(name='total_purchases')
    
    resultado = views.merge(purchases, on='tiene_descuento_alto', how='left')
    resultado['total_purchases'] = resultado['total_purchases'].fillna(0)
    resultado['tasa_conversion'] = (resultado['total_purchases'] / resultado['total_views'] * 100).round(2)
    
    resultado['tiene_descuento_alto'] = resultado['tiene_descuento_alto'].map({
        True: 'Descuento >= 15%',
        False: 'Descuento < 15%'
    })
    
    print(f"  ✓ P4 completada: {len(resultado)} niveles de descuento")
    return resultado


def pregunta_5_dwell_carrito(df: pd.DataFrame) -> pd.DataFrame:
    """
    P5 (Lukaku Jr): ¿Cuál es el dwell time promedio antes de añadir al carrito?
    
    Hipótesis: Los productos académicos requieren más tiempo de evaluación.
    
    Args:
        df: DataFrame enriquecido (Silver)
        
    Returns:
        DataFrame con dwell_time promedio por categoría al añadir al carrito
        Columnas: categoria_general, promedio_dwell_time_segundos, numero_eventos
    """
    add_to_cart = df[
        (df['tipo_evento'] == 'add_to_cart') & 
        (df['dwell_time_segundos'].notna())
    ].copy()
    
    resultado = add_to_cart.groupby('categoria_general').agg({
        'dwell_time_segundos': ['mean', 'count']
    }).reset_index()
    
    resultado.columns = ['categoria_general', 'promedio_dwell_time_segundos', 'numero_eventos']
    resultado['promedio_dwell_time_segundos'] = resultado['promedio_dwell_time_segundos'].round(2)
    
    print(f"  ✓ P5 completada: {len(resultado)} categorías")
    return resultado


def pregunta_6_compras_genero(df: pd.DataFrame) -> pd.DataFrame:
    """
    P6 (Bianca Acosta): ¿Qué género realiza más compras?
    
    Hipótesis: No hay diferencia significativa entre géneros.
    
    Args:
        df: DataFrame enriquecido (Silver)
        
    Returns:
        DataFrame con conteo de compras por género
        Columnas: genero, total_compras, porcentaje
    """
    compras = df[df['tipo_evento'] == 'purchase'].copy()
    
    resultado = compras.groupby('genero').size().reset_index(name='total_compras')
    resultado['porcentaje'] = (resultado['total_compras'] / resultado['total_compras'].sum() * 100).round(2)
    
    print(f"  ✓ P6 completada: {len(resultado)} géneros")
    return resultado


def pregunta_7_impacto_descuentos(df: pd.DataFrame) -> pd.DataFrame:
    """
    P7 (Jonathan): ¿Los descuentos (cualquiera) aumentan las ventas?
    
    Hipótesis: Productos con descuento tienen más compras.
    
    Args:
        df: DataFrame enriquecido (Silver)
        
    Returns:
        DataFrame con volumen de compras según presencia de descuento
        Columnas: tiene_descuento, total_compras, porcentaje
    """
    compras = df[df['tipo_evento'] == 'purchase'].copy()
    compras['tiene_descuento'] = compras['porcentaje_descuento'] > 0
    
    resultado = compras.groupby('tiene_descuento').size().reset_index(name='total_compras')
    resultado['porcentaje'] = (resultado['total_compras'] / resultado['total_compras'].sum() * 100).round(2)
    
    resultado['tiene_descuento'] = resultado['tiene_descuento'].map({
        True: 'Con descuento',
        False: 'Sin descuento'
    })
    
    print(f"  ✓ P7 completada: {len(resultado)} niveles de descuento")
    return resultado


def pregunta_8_beca_benito_juarez(df: pd.DataFrame) -> pd.DataFrame:
    """
    P8 (Isaac): ¿La Beca Benito Juárez se usa en productos alineados a la carrera?
    
    Hipótesis: Los estudiantes con beca compran productos relevantes a su carrera.
    
    Args:
        df: DataFrame enriquecido (Silver)
        
    Returns:
        DataFrame con compras con beca y si coincide la carrera objetivo
        Columnas: carrera_coincide, total_compras_con_beca, porcentaje
    """
    compras_beca = df[
        (df['tipo_evento'] == 'purchase') & 
        (df['metodo_pago'] == 'Beca Benito Juárez')
    ].copy()
    
    # Verificar si la carrera del usuario coincide con la carrera objetivo del producto
    compras_beca['carrera_coincide'] = (
        (compras_beca['carrera'] == compras_beca['carrera_objetivo']) |
        (compras_beca['carrera_objetivo'] == 'Todas')
    )
    
    resultado = compras_beca.groupby('carrera_coincide').size().reset_index(name='total_compras_con_beca')
    resultado['porcentaje'] = (resultado['total_compras_con_beca'] / resultado['total_compras_con_beca'].sum() * 100).round(2)
    
    resultado['carrera_coincide'] = resultado['carrera_coincide'].map({
        True: 'Carrera coincide',
        False: 'Carrera no coincide'
    })
    
    print(f"  ✓ P8 completada: {len(resultado)} categorías de coincidencia")
    return resultado


# ============================================
# MÉTRICAS GENERALES DEL NEGOCIO
# ============================================

def calcular_metricas_generales(df: pd.DataFrame) -> dict:
    """
    Calcula KPIs generales del marketplace.
    
    Args:
        df: DataFrame enriquecido (Silver)
        
    Returns:
        Diccionario con métricas clave del negocio
    """
    total_usuarios = df['usuario_id'].nunique()
    total_productos = df['producto_id'].nunique()
    total_eventos = len(df)
    
    views = len(df[df['tipo_evento'] == 'view'])
    add_to_cart = len(df[df['tipo_evento'] == 'add_to_cart'])
    purchases = len(df[df['tipo_evento'] == 'purchase'])
    
    tasa_conversion_global = (purchases / views * 100) if views > 0 else 0
    
    compras = df[df['tipo_evento'] == 'purchase']
    revenue_total = compras['precio_pagado'].sum() if len(compras) > 0 else 0
    ticket_promedio = compras['precio_pagado'].mean() if len(compras) > 0 else 0
    
    metricas = {
        'total_usuarios': total_usuarios,
        'total_productos': total_productos,
        'total_eventos': total_eventos,
        'total_views': views,
        'total_add_to_cart': add_to_cart,
        'total_purchases': purchases,
        'tasa_conversion_global': round(tasa_conversion_global, 2),
        'revenue_total': round(revenue_total, 2),
        'ticket_promedio': round(ticket_promedio, 2)
    }
    
    return metricas


# ============================================
# PIPELINE PRINCIPAL - GOLD
# ============================================
def run_gold_pipeline(silver_data: pd.DataFrame) -> dict:
    """
    Ejecuta el pipeline completo de la capa Gold.
    
    Args:
        silver_data: DataFrame limpio y enriquecido de Silver
        
    Returns:
        Diccionario con todas las tablas Gold y métricas:
            - pregunta_1 a pregunta_8: DataFrames con respuestas
            - metricas_generales: KPIs del negocio
            
    Pasos:
        1. Calcular respuestas a las 8 preguntas de investigación
        2. Calcular métricas generales del negocio
        3. Retornar diccionario con todos los resultados
    """
    print("\n" + "="*50)
    print("INICIANDO PIPELINE GOLD (BUSINESS METRICS)")
    print("="*50)
    
    resultados = {}
    
    # Responder cada pregunta de investigación
    print("\n[1/8] Calculando P1: Días de compra...")
    resultados['pregunta_1_dias_compra'] = pregunta_1_dias_compra(silver_data)
    
    print("\n[2/8] Calculando P2: GPU por carrera...")
    resultados['pregunta_2_gpu_carrera'] = pregunta_2_gpu_carrera(silver_data)
    
    print("\n[3/8] Calculando P3: Gasto por categoría...")
    resultados['pregunta_3_gasto_categoria'] = pregunta_3_gasto_categoria(silver_data)
    
    print("\n[4/8] Calculando P4: Descuentos y conversión...")
    resultados['pregunta_4_descuentos_conversion'] = pregunta_4_descuentos_conversion(silver_data)
    
    print("\n[5/8] Calculando P5: Dwell time antes del carrito...")
    resultados['pregunta_5_dwell_carrito'] = pregunta_5_dwell_carrito(silver_data)
    
    print("\n[6/8] Calculando P6: Compras por género...")
    resultados['pregunta_6_compras_genero'] = pregunta_6_compras_genero(silver_data)
    
    print("\n[7/8] Calculando P7: Impacto general de descuentos...")
    resultados['pregunta_7_impacto_descuentos'] = pregunta_7_impacto_descuentos(silver_data)
    
    print("\n[8/8] Calculando P8: Beca Benito Juárez...")
    resultados['pregunta_8_beca_benito_juarez'] = pregunta_8_beca_benito_juarez(silver_data)
    
    # Calcular métricas generales
    print("\n[Métricas] Calculando KPIs generales del negocio...")
    resultados['metricas_generales'] = calcular_metricas_generales(silver_data)
    
    # Resumen final
    print("\n" + "="*50)
    print("RESUMEN DE MÉTRICAS GOLD")
    print("="*50)
    print(f"Total preguntas respondidas: 8")
    print(f"Total usuarios únicos:       {resultados['metricas_generales']['total_usuarios']:,}")
    print(f"Total compras:               {resultados['metricas_generales']['total_purchases']:,}")
    print(f"Revenue total:               ${resultados['metricas_generales']['revenue_total']:,.2f}")
    print(f"Tasa conversión global:      {resultados['metricas_generales']['tasa_conversion_global']}%")
    print(f"Timestamp:                   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return resultados


# ============================================
# EJECUCIÓN
# ============================================
if __name__ == "__main__":
    # Este archivo requiere los datos de Silver como input
    # Ejemplo de uso completo:
    # from scripts.ETL.Bronze.raw_data import run_bronze_pipeline
    # from scripts.ETL.Silver.transformed_data import run_silver_pipeline
    # 
    # raw_data = run_bronze_pipeline()
    # silver_data = run_silver_pipeline(raw_data)
    # gold_results = run_gold_pipeline(silver_data)
    
    print("Nota: Este script requiere datos de la capa Silver.")
    print("Ejecuta primero: raw_data.py -> transformed_data.py")
