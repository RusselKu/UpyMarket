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

import os
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from supabase import Client, create_client

try:
    import psycopg
except ImportError:  # pragma: no cover - optional dependency until installed
    psycopg = None


ROOT_DIR = Path(__file__).resolve().parents[3]
LOCAL_ENV_FILE = ROOT_DIR / '.env'


def load_local_env(env_path: Path = LOCAL_ENV_FILE) -> None:
    """Carga variables de entorno desde un archivo .env local si existe."""
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def get_clean_supabase_client() -> Client:
    """Inicializa el cliente de Supabase para escribir en el esquema limpio."""
    load_local_env()

    url = os.environ.get('SUPABASE_URL') or os.environ.get('UPYSTORE_SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY') or os.environ.get('UPYSTORE_SUPABASE_ANON_KEY')

    if not url or not key:
        raise ValueError(
            'Faltan credenciales de Supabase. Define SUPABASE_URL y SUPABASE_KEY en .env o en el entorno.'
        )

    return create_client(url, key)


def get_clean_database_url() -> str | None:
    """Obtiene la URL de conexión directa a PostgreSQL para el esquema limpio."""
    return (
        os.environ.get('SUPABASE_CLEAN_DB_URL')
        or os.environ.get('DATABASE_URL')
        or os.environ.get('SUPABASE_DB_URL')
    )


def dataframe_to_records(df: pd.DataFrame) -> list[dict]:
    """Convierte un DataFrame a registros JSON serializables para Supabase."""
    if df.empty:
        return []

    prepared = df.copy()

    for column in prepared.columns:
        if pd.api.types.is_datetime64_any_dtype(prepared[column]):
            prepared[column] = prepared[column].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    prepared = prepared.replace({np.nan: None, pd.NaT: None})

    records: list[dict] = []
    for record in prepared.to_dict(orient='records'):
        cleaned_record = {}
        for key, value in record.items():
            if value is None:
                cleaned_record[key] = None
            elif isinstance(value, float) and np.isnan(value):
                cleaned_record[key] = None
            else:
                cleaned_record[key] = value
        records.append(cleaned_record)

    return records


def ensure_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Garantiza que el DataFrame tenga las columnas esperadas aunque venga vacío."""
    result = df.copy()
    for column in columns:
        if column not in result.columns:
            result[column] = pd.Series(dtype='object')
    return result


def upsert_clean_table(schema_client, table_name: str, df: pd.DataFrame, conflict_key: str = 'id') -> None:
    """Inserta o actualiza los registros limpios en una tabla del esquema analítico."""
    records = dataframe_to_records(df)
    if not records:
        print(f"  • {table_name}: sin registros para guardar")
        return

    if psycopg is not None and isinstance(schema_client, str):
        columns = list(records[0].keys())
        schema_name = os.environ.get('SUPABASE_CLEAN_SCHEMA', 'upy_analytics_clean')
        insert_columns = ', '.join(f'"{column}"' for column in columns)
        conflict_columns = conflict_key
        update_columns = ', '.join(
            f'"{column}" = EXCLUDED."{column}"'
            for column in columns
            if column != conflict_key
        )
        values_placeholders = ', '.join(['%s'] * len(columns))
        query = (
            f'INSERT INTO "{schema_name}"."{table_name}" ({insert_columns}) '
            f'VALUES ({values_placeholders}) '
            f'ON CONFLICT ("{conflict_columns}") DO UPDATE SET {update_columns}'
        )
        if not update_columns:
            query = (
                f'INSERT INTO "{schema_name}"."{table_name}" ({insert_columns}) '
                f'VALUES ({values_placeholders}) '
                f'ON CONFLICT ("{conflict_columns}") DO NOTHING'
            )

        db_url = schema_client
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.executemany(query, [tuple(record[column] for column in columns) for record in records])
            conn.commit()

        print(f"  ✓ {table_name}: {len(records)} registros guardados/actualizados en PostgreSQL")
        return

    response = schema_client.table(table_name).upsert(records, on_conflict=conflict_key).execute()
    error = getattr(response, 'error', None)
    if error:
        raise RuntimeError(f'Error guardando {table_name}: {error}')

    print(f"  ✓ {table_name}: {len(records)} registros guardados/actualizados")


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
    df = ensure_columns(df, ['id', 'carrera', 'genero', 'created_at'])
    
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
        - Normalizar columnas nuevas del catálogo: icono, descripcion, caracteristicas
        - Calcular precio_final para uso analítico posterior
    """
    df = df_productos.copy()
    df = ensure_columns(df, [
        'id', 'nombre', 'categoria_general', 'carrera_objetivo', 'tiene_gpu_dedicada',
        'precio_original', 'porcentaje_descuento', 'icono', 'descripcion', 'caracteristicas', 'created_at'
    ])
    
    # Eliminar duplicados
    initial_count = len(df)
    df = df.drop_duplicates(subset=['id'], keep='first')
    print(f"  • Duplicados eliminados: {initial_count - len(df)}")
    
    # Validar precios y tipos numéricos
    df['precio_original'] = pd.to_numeric(df['precio_original'], errors='coerce')
    if 'porcentaje_descuento' in df.columns:
        df['porcentaje_descuento'] = pd.to_numeric(df['porcentaje_descuento'], errors='coerce').fillna(0)

    # Validar precios positivos
    df = df[df['precio_original'] > 0]
    
    # Validar rango de descuentos
    if 'porcentaje_descuento' in df.columns:
        df = df[(df['porcentaje_descuento'] >= 0) & (df['porcentaje_descuento'] <= 1)]

    # Normalizar columnas de enriquecimiento del nuevo esquema
    if 'icono' in df.columns:
        df['icono'] = df['icono'].fillna('📦')
    else:
        df['icono'] = '📦'

    if 'descripcion' in df.columns:
        df['descripcion'] = df['descripcion'].fillna('')
    else:
        df['descripcion'] = ''

    if 'caracteristicas' in df.columns:
        df['caracteristicas'] = df['caracteristicas'].apply(
            lambda value: value if isinstance(value, list) else []
        )
    else:
        df['caracteristicas'] = [[] for _ in range(len(df))]

    df['precio_final'] = (df['precio_original'] * (1 - df['porcentaje_descuento'])).round(2)
    
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
    df = ensure_columns(df, [
        'id', 'usuario_id', 'producto_id', 'tipo_evento', 'dwell_time_segundos',
        'precio_pagado', 'metodo_pago', 'es_fin_de_semana', 'created_at'
    ])
    
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


def filter_telemetria_referencial(df_telemetria: pd.DataFrame, df_usuarios: pd.DataFrame, df_productos: pd.DataFrame) -> pd.DataFrame:
    """Elimina eventos cuya referencia a usuario o producto no exista en las tablas limpias."""
    valid_usuarios = set(df_usuarios['id'])
    valid_productos = set(df_productos['id'])

    initial_count = len(df_telemetria)
    df = df_telemetria[
        df_telemetria['usuario_id'].isin(valid_usuarios) &
        df_telemetria['producto_id'].isin(valid_productos)
    ].copy()

    print(f"  • Eventos eliminados por integridad referencial: {initial_count - len(df)}")
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
        how='inner',
        suffixes=('', '_usuario')
    )
    
    # JOIN con productos
    df_enriched = df_enriched.merge(
        df_productos[[
            'id', 'nombre', 'categoria_general', 'carrera_objetivo',
            'tiene_gpu_dedicada', 'precio_original', 'porcentaje_descuento',
            'precio_final', 'icono', 'descripcion', 'caracteristicas'
        ]],
        left_on='producto_id',
        right_on='id',
        how='inner',
        suffixes=('', '_producto')
    )
    
    # Limpiar columnas duplicadas de id
    df_enriched = df_enriched.drop(columns=['id_usuario', 'id_producto'], errors='ignore')
    
    print(f"  ✓ Telemetría enriquecida: {len(df_enriched)} eventos con {len(df_enriched.columns)} columnas")
    return df_enriched


# ============================================
# PIPELINE PRINCIPAL - SILVER
# ============================================
def run_silver_pipeline(raw_data: dict, persist_to_clean_db: bool = True) -> pd.DataFrame:
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

    print("\n[Validación] Filtrando eventos con llaves foráneas válidas...")
    telemetria_clean = filter_telemetria_referencial(telemetria_clean, usuarios_clean, productos_clean)
    
    # Enriquecer telemetría
    print("\n[Enriquecimiento] Uniendo tablas...")
    telemetria_enriched = enrich_telemetria(
        telemetria_clean,
        usuarios_clean,
        productos_clean
    )

    if persist_to_clean_db:
        print("\n[Persistencia] Guardando capa limpia en upy_analytics_clean...")
        clean_db_url = get_clean_database_url()
        if clean_db_url and psycopg is not None:
            upsert_clean_table(clean_db_url, 'usuarios_sesion_clean', usuarios_clean)
            upsert_clean_table(clean_db_url, 'catalogo_productos_clean', productos_clean)
            upsert_clean_table(clean_db_url, 'interacciones_telemetria_clean', telemetria_clean)
        else:
            supabase = get_clean_supabase_client()
            try:
                clean_schema_client = supabase.schema(os.environ.get('SUPABASE_CLEAN_SCHEMA', 'upy_analytics_clean'))
                upsert_clean_table(clean_schema_client, 'usuarios_sesion_clean', usuarios_clean)
                upsert_clean_table(clean_schema_client, 'catalogo_productos_clean', productos_clean)
                upsert_clean_table(clean_schema_client, 'interacciones_telemetria_clean', telemetria_clean)
            except Exception as exc:
                print(f"  ! Persistencia omitida: {exc}")
    
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
