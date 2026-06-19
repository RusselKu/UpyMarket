"""
ETL Pipeline - Silver Layer (Cleaned & Enriched Data)
======================================================
Propósito: Limpiar, validar y enriquecer los datos crudos de Bronze.
Responsabilidades:
    - Eliminar valores atípicos (outliers)
    - Validar integridad referencial
    - Enriquecer con joins entre tablas
    - Preparar datos para visualización y análisis
    
Equipo: Ingeniería de Datos y Procesamiento ELT
"""

import pandas as pd
import numpy as np
from datetime import datetime


# ============================================
# LIMPIEZA Y VALIDACIÓN
# ============================================
def clean_usuarios(df_usuarios: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y valida la tabla de usuarios.
    
    Args:
        df_usuarios: DataFrame crudo de usuarios_sesion
        
    Returns:
        DataFrame limpio con validaciones aplicadas
        
    Validaciones:
        - Eliminar duplicados por id
        - Validar que carrera y género no sean nulos
        - Convertir created_at a datetime
    """
    df = df_usuarios.copy()
    
    # Eliminar duplicados
    initial_count = len(df)
    df = df.drop_duplicates(subset=['id'], keep='first')
    print(f"  • Duplicados eliminados: {initial_count - len(df)}")
    
    # Validar campos obligatorios
    df = df.dropna(subset=['carrera', 'genero'])
    
    # Convertir timestamp
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'])
    
    print(f"  ✓ Usuarios limpios: {len(df)} registros")
    return df


def clean_productos(df_productos: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y valida el catálogo de productos.
    
    Args:
        df_productos: DataFrame crudo de catalogo_productos
        
    Returns:
        DataFrame limpio con validaciones aplicadas
        
    Validaciones:
        - Eliminar duplicados por id
        - Validar precios positivos
        - Validar descuentos en rango [0, 1]
    """
    df = df_productos.copy()
    
    # Eliminar duplicados
    initial_count = len(df)
    df = df.drop_duplicates(subset=['id'], keep='first')
    print(f"  • Duplicados eliminados: {initial_count - len(df)}")
    
    # Validar precios positivos
    df = df[df['precio_original'] > 0]
    
    # Validar rango de descuentos
    if 'porcentaje_descuento' in df.columns:
        df = df[(df['porcentaje_descuento'] >= 0) & (df['porcentaje_descuento'] <= 1)]
    
    print(f"  ✓ Productos limpios: {len(df)} registros")
    return df


def remove_outliers_dwell_time(df_telemetria: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina valores atípicos en dwell_time usando el método IQR.
    
    Args:
        df_telemetria: DataFrame de telemetría
        
    Returns:
        DataFrame sin outliers en dwell_time
        
    Método:
        - Calcula Q1, Q3 e IQR (Rango Intercuartílico)
        - Elimina valores fuera de [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
    """
    df = df_telemetria.copy()
    
    # Filtrar solo eventos con dwell_time válido
    df_with_dwell = df[df['dwell_time_segundos'].notna()].copy()
    
    if len(df_with_dwell) > 0:
        Q1 = df_with_dwell['dwell_time_segundos'].quantile(0.25)
        Q3 = df_with_dwell['dwell_time_segundos'].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Contar outliers
        outliers = df_with_dwell[
            (df_with_dwell['dwell_time_segundos'] < lower_bound) | 
            (df_with_dwell['dwell_time_segundos'] > upper_bound)
        ]
        print(f"  • Outliers de dwell_time eliminados: {len(outliers)}")
        
        # Filtrar outliers
        df_with_dwell = df_with_dwell[
            (df_with_dwell['dwell_time_segundos'] >= lower_bound) & 
            (df_with_dwell['dwell_time_segundos'] <= upper_bound)
        ]
        
        # Recombinar con eventos que no tienen dwell_time
        df_without_dwell = df[df['dwell_time_segundos'].isna()]
        df = pd.concat([df_with_dwell, df_without_dwell], ignore_index=True)
    
    return df


def clean_telemetria(df_telemetria: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y valida eventos de telemetría.
    
    Args:
        df_telemetria: DataFrame crudo de interacciones_telemetria
        
    Returns:
        DataFrame limpio sin outliers
        
    Validaciones:
        - Eliminar duplicados por id
        - Validar tipo_evento permitido
        - Eliminar outliers de dwell_time
        - Convertir timestamps
    """
    df = df_telemetria.copy()
    
    # Eliminar duplicados
    initial_count = len(df)
    df = df.drop_duplicates(subset=['id'], keep='first')
    print(f"  • Duplicados eliminados: {initial_count - len(df)}")
    
    # Validar tipos de evento permitidos
    eventos_validos = ['view', 'add_to_cart', 'purchase']
    df = df[df['tipo_evento'].isin(eventos_validos)]
    
    # Eliminar outliers de dwell_time
    df = remove_outliers_dwell_time(df)
    
    # Convertir timestamp
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'])
    
    print(f"  ✓ Eventos de telemetría limpios: {len(df)} registros")
    return df


# ============================================
# ENRIQUECIMIENTO DE DATOS
# ============================================
def enrich_telemetria(
    df_telemetria: pd.DataFrame,
    df_usuarios: pd.DataFrame,
    df_productos: pd.DataFrame
) -> pd.DataFrame:
    """
    Enriquece la telemetría haciendo JOIN con usuarios y productos.
    
    Args:
        df_telemetria: DataFrame de telemetría limpia
        df_usuarios: DataFrame de usuarios limpio
        df_productos: DataFrame de productos limpio
        
    Returns:
        DataFrame enriquecido con información de carrera, género, categoría, etc.
        
    Columnas añadidas:
        - carrera (del usuario)
        - genero (del usuario)
        - categoria_general (del producto)
        - carrera_objetivo (del producto)
        - tiene_gpu_dedicada (del producto)
        - precio_original (del producto)
        - porcentaje_descuento (del producto)
    """
    # JOIN con usuarios
    df_enriched = df_telemetria.merge(
        df_usuarios[['id', 'carrera', 'genero']],
        left_on='usuario_id',
        right_on='id',
        how='left',
        suffixes=('', '_usuario')
    )
    
    # JOIN con productos
    df_enriched = df_enriched.merge(
        df_productos[[
            'id', 'nombre', 'categoria_general', 'carrera_objetivo',
            'tiene_gpu_dedicada', 'precio_original', 'porcentaje_descuento'
        ]],
        left_on='producto_id',
        right_on='id',
        how='left',
        suffixes=('', '_producto')
    )
    
    # Limpiar columnas duplicadas de id
    df_enriched = df_enriched.drop(columns=['id_usuario', 'id_producto'], errors='ignore')
    
    print(f"  ✓ Telemetría enriquecida: {len(df_enriched)} eventos con {len(df_enriched.columns)} columnas")
    return df_enriched


# ============================================
# PIPELINE PRINCIPAL - SILVER
# ============================================
def run_silver_pipeline(raw_data: dict) -> pd.DataFrame:
    """
    Ejecuta el pipeline completo de la capa Silver.
    
    Args:
        raw_data: Diccionario con DataFrames de Bronze:
            - usuarios_sesion
            - catalogo_productos
            - interacciones_telemetria
            
    Returns:
        DataFrame enriquecido y limpio listo para análisis
        
    Pasos:
        1. Limpiar cada tabla individualmente
        2. Eliminar valores atípicos
        3. Enriquecer telemetría con JOINs
        4. Retornar dataset unificado
    """
    print("\n" + "="*50)
    print("INICIANDO PIPELINE SILVER (CLEANED DATA)")
    print("="*50)
    
    # Limpiar cada tabla
    print("\n[1/3] Limpiando usuarios...")
    usuarios_clean = clean_usuarios(raw_data['usuarios_sesion'])
    
    print("\n[2/3] Limpiando productos...")
    productos_clean = clean_productos(raw_data['catalogo_productos'])
    
    print("\n[3/3] Limpiando telemetría...")
    telemetria_clean = clean_telemetria(raw_data['interacciones_telemetria'])
    
    # Enriquecer telemetría
    print("\n[Enriquecimiento] Uniendo tablas...")
    telemetria_enriched = enrich_telemetria(
        telemetria_clean,
        usuarios_clean,
        productos_clean
    )
    
    # Resumen final
    print("\n" + "="*50)
    print("RESUMEN DE LIMPIEZA")
    print("="*50)
    print(f"Eventos finales:     {len(telemetria_enriched):,}")
    print(f"Columnas totales:    {len(telemetria_enriched.columns)}")
    print(f"Timestamp:           {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return telemetria_enriched


# ============================================
# EJECUCIÓN
# ============================================
if __name__ == "__main__":
    # Este archivo requiere los datos de Bronze como input
    # Ejemplo de uso:
    # from scripts.ETL.Bronze.raw_data import run_bronze_pipeline
    # raw_data = run_bronze_pipeline()
    # silver_data = run_silver_pipeline(raw_data)
    
    print("Nota: Este script requiere datos de la capa Bronze.")
    print("Ejecuta primero: raw_data.py")
