# Guía de Mantenimiento — Catálogo de Productos UpyMarket

> Este documento es para el equipo técnico. Cualquier cambio en los productos del marketplace **debe hacerse directamente en Supabase**, no en archivos del frontend. `assets/catalog.js` es solo una copia de referencia y ya no se usa en producción.

---

## Regla de oro

```
La fuente de verdad del catálogo es la tabla catalogo_productos en Supabase.
Siempre que agregues, modifiques o elimines productos, corre el SQL correspondiente
en Supabase Dashboard → SQL Editor.
```

---

## Estructura de un producto

Cada producto en `catalogo_productos` tiene estos campos:

| Campo | Tipo | Ejemplo | Obligatorio |
|-------|------|---------|:-----------:|
| `id` | VARCHAR | `'p47'` | ✅ |
| `nombre` | VARCHAR | `'Disco Duro SSD 1 TB'` | ✅ |
| `categoria_general` | VARCHAR | ver categorías válidas | ✅ |
| `carrera_objetivo` | VARCHAR | `'Todas'` o carrera específica | ✅ |
| `tiene_gpu_dedicada` | BOOLEAN | `false` (solo `true` para laptops RTX) | ✅ |
| `precio_original` | DECIMAL | `899.00` | ✅ |
| `porcentaje_descuento` | DECIMAL | `0.10` para 10%, `0.00` si no hay | ✅ |
| `icono` | TEXT | `'💾'` (un solo emoji) | ✅ |
| `descripcion` | TEXT | Descripción de 1-2 oraciones | ✅ |
| `caracteristicas` | TEXT[] | Array con 3-5 puntos clave | ✅ |

### Categorías válidas

```
'Académico'       → cursos, kits, material de estudio
'Entretenimiento' → periféricos, accesorios, suscripciones
'Laptop'          → laptops con o sin GPU
'Books'           → libros y manuales
'Food'            → comida y bebidas en campus
'Services'        → servicios entre estudiantes
'Sports'          → artículos deportivos
'Other'           → todo lo que no encaje arriba
```

### Carreras válidas para `carrera_objetivo`

```
'Todas'
'Ingeniería en Ciberseguridad'
'Ingeniería en Datos e IA'
'Ingeniería en Robótica Computacional'
'Ingeniería en Sistemas Embebidos Computacionales'
```

---

## Agregar un nuevo producto

### Paso 1 — Elige el siguiente ID

El último producto registrado es `p46`. El nuevo debe ser `p47`, `p48`, etc.  
Para verificar cuál es el último ID actual:

```sql
SELECT id FROM public.catalogo_productos ORDER BY id DESC LIMIT 5;
```

### Paso 2 — Corre el INSERT en Supabase SQL Editor

Copia esta plantilla, llena los valores y ejecuta:

```sql
INSERT INTO public.catalogo_productos
  (id, nombre, categoria_general, carrera_objetivo, tiene_gpu_dedicada,
   precio_original, porcentaje_descuento, icono, descripcion, caracteristicas)
VALUES
  ('p47', 'Nombre del Producto',
          'Académico', 'Todas', false,
          999.00, 0.00,
          '📦',
          'Descripción corta del producto en una o dos oraciones.',
          ARRAY['Característica 1', 'Característica 2', 'Característica 3', 'Característica 4']);
```

### Paso 3 — Verifica que se insertó correctamente

```sql
SELECT id, nombre, icono, categoria_general, precio_original
FROM public.catalogo_productos
WHERE id = 'p47';
```

### Paso 4 — Actualiza seed.sql en el repositorio

Agrega el nuevo producto al final de `db/seed.sql` (antes del `ON CONFLICT`) para que el archivo refleje el estado real de la DB.

**¿Por qué actualizar seed.sql si ya está en la DB?**  
Porque si alguien necesita reinicializar la base de datos desde cero (nuevo proyecto Supabase, staging, etc.), seed.sql debe tener todos los productos actualizados.

---

## Modificar un producto existente

Para actualizar el precio, descuento u otro campo de un producto que ya existe:

```sql
UPDATE public.catalogo_productos
SET
  precio_original      = 1299.00,
  porcentaje_descuento = 0.20,
  descripcion          = 'Nueva descripción actualizada.'
WHERE id = 'p13';
```

Luego actualiza también el registro correspondiente en `db/seed.sql`.

---

## Eliminar un producto

> **Precaución:** Si hay registros en `interacciones_telemetria` que referencian este producto, la eliminación fallará por la FK constraint. Primero verifica si hay telemetría.

```sql
-- 1. Verifica si hay telemetría asociada
SELECT COUNT(*) FROM public.interacciones_telemetria WHERE producto_id = 'p46';

-- 2. Si no hay registros (COUNT = 0), procede a eliminar
DELETE FROM public.catalogo_productos WHERE id = 'p46';
```

Si hay telemetría y aún quieres eliminar el producto, considera desactivarlo en vez de borrarlo — por ejemplo agregando un campo `activo BOOLEAN DEFAULT true` y filtrando en el frontend.

---

## Correr seed.sql completo (reinicialización)

Si necesitas reinicializar el catálogo desde cero (por ejemplo en un proyecto Supabase nuevo):

1. **Ejecuta la migración primero** (si es una DB nueva sin columnas `icono`/`descripcion`/`caracteristicas`):
   ```
   Supabase SQL Editor → pega db/migrate_add_product_columns.sql → Run
   ```

2. **Ejecuta el seed completo:**
   ```
   Supabase SQL Editor → pega db/seed.sql → Run
   ```

El seed usa `ON CONFLICT (id) DO UPDATE`, así que si los productos ya existen los actualiza sin duplicar.

---

## Validar el estado del catálogo

Después de cualquier cambio, corre estas queries para verificar que todo está bien:

```sql
-- ¿Cuántos productos hay en total?
SELECT COUNT(*) AS total FROM public.catalogo_productos;

-- ¿Cuántos hay por categoría?
SELECT categoria_general, COUNT(*) AS cantidad
FROM public.catalogo_productos
GROUP BY categoria_general
ORDER BY cantidad DESC;

-- ¿Algún producto con descripción o icono vacío?
SELECT id, nombre
FROM public.catalogo_productos
WHERE descripcion = '' OR icono = '📦' OR caracteristicas = '{}';

-- ¿Rango de precios por categoría?
SELECT categoria_general,
       MIN(precio_original) AS precio_min,
       MAX(precio_original) AS precio_max,
       ROUND(AVG(precio_original), 2) AS precio_promedio
FROM public.catalogo_productos
GROUP BY categoria_general
ORDER BY precio_promedio DESC;
```

---

## Impacto en la telemetría al agregar productos

Cuando se agrega un nuevo producto a la DB:

- El frontend lo mostrará automáticamente la próxima vez que se cargue la página (sin necesidad de redespliegue)
- Los eventos de telemetría (`view`, `add_to_cart`, `purchase`) podrán registrarse con el nuevo `producto_id`
- El pipeline ETL en Python lo incluirá automáticamente en los análisis

---

## Sincronización con assets/catalog.js

`assets/catalog.js` es una copia estática del catálogo que **ya no se usa en producción**. El frontend carga productos desde la DB. Sin embargo, se mantiene en el repositorio como:

- Referencia para saber qué productos existen si no hay acceso a Supabase
- Fuente de datos para pruebas locales sin conexión a internet (si en el futuro se necesita un fallback)

Si quieres mantener `catalog.js` sincronizado con la DB, exporta los datos desde Supabase y actualiza el archivo manualmente. **No es obligatorio** hacerlo en cada cambio.

---

## Checklist de mantenimiento

Al agregar un nuevo producto:

- [ ] Elegí un ID consecutivo (p47, p48, ...)
- [ ] Verifiqué que la categoría es una de las 8 válidas
- [ ] Verifiqué que la carrera es una de las 5 válidas (o `'Todas'`)
- [ ] El precio está en MXN con dos decimales
- [ ] El descuento está en decimal (0.15 para 15%), no en porcentaje
- [ ] El icono es un emoji único y representativo
- [ ] La descripción tiene entre 1 y 3 oraciones
- [ ] Las características son 3-5 puntos concretos
- [ ] Corrí la query de validación y el conteo aumentó
- [ ] Actualicé `db/seed.sql` en el repositorio con el nuevo producto

---

*Última actualización: junio 2026 — UpyMarket v3 (46 productos)*
