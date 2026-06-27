-- Migración: agregar columnas de detalle a catalogo_productos
-- Ejecutar en Supabase Dashboard → SQL Editor ANTES de correr seed.sql actualizado
ALTER TABLE public.catalogo_productos
  ADD COLUMN IF NOT EXISTS icono          TEXT     DEFAULT '📦',
  ADD COLUMN IF NOT EXISTS descripcion    TEXT     DEFAULT '',
  ADD COLUMN IF NOT EXISTS caracteristicas TEXT[]  DEFAULT '{}';
