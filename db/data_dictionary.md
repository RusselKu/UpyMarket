# Diccionario de Datos: E-commerce Platform

Este es el diseño relacional de la base de datos. Consta de 3 tablas principales (2 de dimensiones y 1 de hechos para la telemetría).

## 1. Tabla: `usuarios_sesion` (Dimensión de Usuario)
Almacena el perfil demográfico anónimo de cada estudiante que ingresa a la tienda.

* **id (UUID):** Llave primaria generada automáticamente. Identificador único de la sesión del alumno.
* **carrera (VARCHAR):** Carrera del estudiante (Ej. "Ingeniería de Datos", "Sistemas Embebidos").
* **genero (VARCHAR):** Género del estudiante (Ej. "Masculino", "Femenino").
* **created_at (TIMESTAMP):** Fecha y hora exacta de su registro.

## 2. Tabla: `catalogo_productos` (Dimensión de Producto)
Contiene la información estática de los artículos que se venden. Debe ser pre-llenada por el equipo.

* **id (VARCHAR):** Llave primaria. Un ID legible que también se usará en la URL (Ej. "macbook-pro-m3").
* **nombre (VARCHAR):** Nombre completo del producto.
* **categoria_general (VARCHAR):** Clasificación principal ("Académico" o "Entretenimiento").
* **carrera_objetivo (VARCHAR):** Carrera a la que va dirigida el producto (Ej. "Todas", "Sistemas Embebidos").
* **tiene_gpu_dedicada (BOOLEAN):** `true` si es un equipo con gráficos dedicados (RTX), `false` si no lo es.
* **precio_original (DECIMAL):** Precio base del producto.
* **porcentaje_descuento (DECIMAL):** Descuento aplicable en formato decimal (Ej. 0.15 = 15%).
* **created_at (TIMESTAMP):** Fecha en la que se dio de alta el producto.

## 3. Tabla: `interacciones_telemetria` (Tabla de Hechos)
El corazón del proyecto. Registra cada acción (clic, tiempo, compra) que los usuarios hacen con los productos.

* **id (UUID):** Llave primaria del evento.
* **usuario_id (UUID):** Llave foránea (Foreign Key) vinculada a `usuarios_sesion.id`.
* **producto_id (VARCHAR):** Llave foránea vinculada a `catalogo_productos.id`.
* **tipo_evento (VARCHAR):** Acción específica. Puede ser: 'view' (ver), 'add_to_cart' (añadir al carrito) o 'purchase' (comprar).
* **dwell_time_segundos (DECIMAL, Nullable):** Segundos que pasó viendo el producto. Se llena solo si el evento es 'view' o antes de un 'add_to_cart'.
* **precio_pagado (DECIMAL, Nullable):** Precio final. Se llena solo si el evento es 'purchase'.
* **metodo_pago (VARCHAR, Nullable):** Cómo pagó. Se llena solo si el evento es 'purchase' (Ej. "Tarjeta", "Beca Benito Juárez").
* **es_fin_de_semana (BOOLEAN):** `true` si la acción ocurrió en sábado o domingo.
* **created_at (TIMESTAMP):** Marca de tiempo exacta del evento.

---

## Matriz de Validación: ¿Cómo resolvemos las 8 preguntas?

1. **Rama (Días de compra):** Se cruza `tipo_evento = 'purchase'` con la columna `es_fin_de_semana`.
2. **Russel (GPUs y Carrera):** Se cruza `dwell_time_segundos` con `carrera` (de usuarios) y `tiene_gpu_dedicada` (de productos).
3. **Edgardo (Gasto Académico vs Ocio):** Se suma `precio_pagado` (cuando `tipo_evento='purchase'`) agrupado por `categoria_general` (Académico/Entretenimiento).
4. **Damian Novelo (Descuentos >= 15%):** Se calcula la tasa de conversión (purchase / view) agrupando por `porcentaje_descuento >= 0.15`.
5. **Rivaldo Canché (Dwell time previo al carrito):** Se mide el `dwell_time_segundos` enviado en el momento exacto en que `tipo_evento = 'add_to_cart'`, agrupado por `categoria_general`.
6. **Bianca Acosta (Compras por Género):** Se cuenta el total de `tipo_evento = 'purchase'` agrupado por `genero` de la tabla usuarios.
7. **Jonathan (Impacto general de descuentos):** Se compara el volumen de `purchase` en productos donde `porcentaje_descuento > 0` vs `porcentaje_descuento = 0`.
8. **Isaac (Beca Benito Juárez y carrera):** Se filtran las compras con `metodo_pago = 'Beca Benito Juárez'` y se revisa si la `carrera` del usuario coincide con la `carrera_objetivo` del producto.