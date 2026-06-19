"""
ETL Pipeline - Bronze Layer (Raw Data)
========================================
Propósito: Extraer datos crudos desde Supabase sin transformaciones.
Responsabilidades:
    - Conectar a la base de datos PostgreSQL en Supabase
    - Extraer tablas completas: usuarios_sesion, catalogo_productos, interacciones_telemetria
    - Guardar datos crudos para procesamiento posterior
    
Equipo: Arquitectura de Base de Datos y Seguridad
"""

import os
from supabase import create_client, Client
import pandas as pd
from datetime import datetime


# ============================================
# CONFIGURACIÓN DE SUPABASE
# ============================================
def get_supabase_client() -> Client:
    """
    Inicializa y retorna el cliente de Supabase.
    
    Returns:
        Client: Cliente autenticado de Supabase
    
    Nota: Las credenciales deben estar en variables de entorno:
        - SUPABASE_URL: URL del proyecto
        - SUPABASE_KEY: API Key (anon/public)
    """
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("Faltan credenciales de Supabase en variables de entorno")
    
    supabase: Client = create_client(url, key)
    return supabase


# ============================================
# EXTRACCIÓN DE DATOS CRUDOS
# ============================================
def extract_usuarios_sesion(supabase: Client) -> pd.DataFrame:
    """
    Extrae todos los registros de la tabla usuarios_sesion.
    
    Args:
        supabase: Cliente de Supabase autenticado
        
    Returns:
        DataFrame con columnas: id, carrera, genero, created_at
    """
    try:
        response = supabase.table("usuarios_sesion").select("*").execute()
        df = pd.DataFrame(response.data)
        print(f"✓ Usuarios extraídos: {len(df)} registros")
        return df
    except Exception as e:
        print(f"✗ Error extrayendo usuarios: {e}")
        return pd.DataFrame()


def extract_catalogo_productos(supabase: Client) -> pd.DataFrame:
    """
    Extrae todos los productos del catálogo.
    
    Args:
        supabase: Cliente de Supabase autenticado
        
    Returns:
        DataFrame con el catálogo completo de productos
    """
    try:
        response = supabase.table("catalogo_productos").select("*").execute()
        df = pd.DataFrame(response.data)
        print(f"✓ Productos extraídos: {len(df)} registros")
        return df
    except Exception as e:
        print(f"✗ Error extrayendo catálogo: {e}")
        return pd.DataFrame()


def extract_interacciones_telemetria(supabase: Client) -> pd.DataFrame:
    """
    Extrae todos los eventos de telemetría registrados.
    
    Args:
        supabase: Cliente de Supabase autenticado
        
    Returns:
        DataFrame con todos los eventos de interacción
    """
    try:
        response = supabase.table("interacciones_telemetria").select("*").execute()
        df = pd.DataFrame(response.data)
        print(f"✓ Eventos de telemetría extraídos: {len(df)} registros")
        return df
    except Exception as e:
        print(f"✗ Error extrayendo telemetría: {e}")
        return pd.DataFrame()


# ============================================
# PIPELINE PRINCIPAL - BRONZE
# ============================================
def run_bronze_pipeline():
    """
    Ejecuta el pipeline completo de la capa Bronze.
    
    Pasos:
        1. Conectar a Supabase
        2. Extraer todas las tablas
        3. Retornar DataFrames crudos
        
    Returns:
        dict: Diccionario con las tres tablas como DataFrames
    """
    print("="*50)
    print("INICIANDO PIPELINE BRONZE (RAW DATA)")
    print("="*50)
    
    # Conectar a Supabase
    supabase = get_supabase_client()
    print("✓ Conexión a Supabase establecida\n")
    
    # Extraer datos crudos
    usuarios = extract_usuarios_sesion(supabase)
    productos = extract_catalogo_productos(supabase)
    telemetria = extract_interacciones_telemetria(supabase)
    
    # Resumen de extracción
    print("\n" + "="*50)
    print("RESUMEN DE EXTRACCIÓN")
    print("="*50)
    print(f"Usuarios:    {len(usuarios):,} registros")
    print(f"Productos:   {len(productos):,} registros")
    print(f"Telemetría:  {len(telemetria):,} eventos")
    print(f"Timestamp:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return {
        "usuarios_sesion": usuarios,
        "catalogo_productos": productos,
        "interacciones_telemetria": telemetria
    }


# ============================================
# EJECUCIÓN
# ============================================
if __name__ == "__main__":
    raw_data = run_bronze_pipeline()
    
    # Opcional: Guardar los datos crudos para análisis posterior
    # raw_data["usuarios_sesion"].to_csv("bronze_usuarios.csv", index=False)
    # raw_data["catalogo_productos"].to_csv("bronze_productos.csv", index=False)
    # raw_data["interacciones_telemetria"].to_csv("bronze_telemetria.csv", index=False)
