-- 1. Crear tabla de Perfiles de Estudiantes (Usuarios)
CREATE TABLE public.usuarios_sesion (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    carrera VARCHAR(100) NOT NULL,
    genero VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Crear tabla de Catálogo de Productos
CREATE TABLE public.catalogo_productos (
    id VARCHAR(100) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    categoria_general VARCHAR(50) NOT NULL,
    carrera_objetivo VARCHAR(100) DEFAULT 'Todas',
    tiene_gpu_dedicada BOOLEAN DEFAULT false,
    precio_original DECIMAL(10, 2) NOT NULL,
    porcentaje_descuento DECIMAL(3, 2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Crear tabla de Telemetría (Eventos)
CREATE TABLE public.interacciones_telemetria (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    usuario_id UUID REFERENCES public.usuarios_sesion (id) ON DELETE CASCADE,
    producto_id VARCHAR(100) REFERENCES public.catalogo_productos (id) ON DELETE CASCADE,
    tipo_evento VARCHAR(50) NOT NULL,
    dwell_time_segundos DECIMAL(10, 2),
    precio_pagado DECIMAL(10, 2),
    metodo_pago VARCHAR(100),
    es_fin_de_semana BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Índices para optimizar velocidad de consultas analíticas
CREATE INDEX idx_telemetria_usuario ON public.interacciones_telemetria(usuario_id);
CREATE INDEX idx_telemetria_producto ON public.interacciones_telemetria(producto_id);
CREATE INDEX idx_telemetria_evento ON public.interacciones_telemetria(tipo_evento);

-- 5. Configuración de Seguridad RLS
ALTER TABLE public.usuarios_sesion ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.interacciones_telemetria ENABLE ROW LEVEL SECURITY;

-- Permitir que CUALQUIERA (anon) pueda INSERTAR un nuevo perfil al entrar a la tienda
CREATE POLICY "Permitir registro de usuarios anonimos" 
ON public.usuarios_sesion FOR INSERT TO anon WITH CHECK (true);

-- Permitir que CUALQUIERA (anon) pueda INSERTAR un evento de telemetría
CREATE POLICY "Permitir tracking anonimo" 
ON public.interacciones_telemetria FOR INSERT TO anon WITH CHECK (true);