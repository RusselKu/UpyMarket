# UpyMarket — Marketplace Estudiantil UPY

Prototipo funcional de e-commerce estático para estudiantes de la **Universidad Politécnica de Yucatán (UPY)**. Diseñado para capturar telemetría de comportamiento de compra y alimentar un pipeline ETL de análisis de datos, todo desplegado como sitio estático en GitHub Pages sin necesidad de backend propio.

---

## Tabla de Contenidos

1. [Descripción general](#descripción-general)
2. [Stack tecnológico](#stack-tecnológico)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Arquitectura del sistema](#arquitectura-del-sistema)
5. [Autenticación con correo institucional](#autenticación-con-correo-institucional)
6. [Base de datos (Supabase)](#base-de-datos-supabase)
7. [Frontend — Componentes y flujo](#frontend--componentes-y-flujo)
8. [Sistema de telemetría](#sistema-de-telemetría)
9. [Preguntas de investigación](#preguntas-de-investigación)
10. [Pipeline ETL (Arquitectura Medallón)](#pipeline-etl-arquitectura-medallón)
11. [Catálogo de productos](#catálogo-de-productos)
12. [Levantar en local](#levantar-en-local)
13. [Despliegue en GitHub Pages](#despliegue-en-github-pages)
14. [Configuración de Supabase (paso a paso)](#configuración-de-supabase-paso-a-paso)

---

## Descripción general

UpyMarket simula una tienda en línea donde estudiantes de Ingeniería de UPY pueden explorar y "comprar" productos académicos, de entretenimiento y laptops. Cada interacción genera un evento de telemetría almacenado en Supabase, vinculado al usuario autenticado, para análisis posterior.

El proyecto tiene **dos audiencias**:

| Audiencia | Qué usan |
|-----------|----------|
| Estudiantes UPY (usuarios finales) | El sitio web en GitHub Pages |
| Equipo de datos (investigadores) | Pipeline ETL en Python + Supabase |

---

## Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Frontend | HTML5, CSS3, JavaScript ES Modules (sin framework, sin build) |
| Base de datos | Supabase (PostgreSQL gestionado) |
| Auth | Supabase Auth — correo institucional `@upy.edu.mx` + confirmación por email |
| Seguridad DB | Row Level Security (RLS) con `auth.uid()` |
| Despliegue | GitHub Pages (sitio 100% estático) |
| Analytics pipeline | Python 3 + pandas + supabase-py |
| Cliente Supabase | `supabase-js@2` auto-hospedado en `assets/supabase.min.js` |

> **Por qué auto-hospedar supabase-js:** Microsoft Edge bloquea requests a `cdn.jsdelivr.net` por Tracking Prevention. Servir el bundle desde el mismo origen elimina ese bloqueo.

---

## Estructura del proyecto

```
UpyMarket/
│
├── index.html                    # Página principal (SPA estática)
├── config.js                     # Credenciales Supabase (URL + anon key)
├── .nojekyll                     # Evita procesamiento Jekyll en GitHub Pages
│
├── assets/
│   ├── style.css                 # Estilos globales (glass morphism, tema UPY)
│   ├── supabase.min.js           # Bundle supabase-js@2 auto-hospedado
│   ├── catalog.js                # Catálogo estático (referencia, ya no usado en prod)
│   ├── upy-logo-full.png
│   ├── upy-emblem.png
│   └── product-images/           # SVGs por categoría
│
├── scripts/
│   ├── supabaseClient.js         # Cliente Supabase + funciones: cargarProductos, insertarPerfil, insertarTelemetria
│   ├── auth.js                   # Modal login/registro @upy.edu.mx, gestión de sesión
│   ├── telemetry.js              # trackView / trackAddToCart / trackPurchase
│   └── ui.js                    # Renderizado del catálogo (carga desde DB), carrito, filtros
│
├── db/
│   ├── schema.sql                # DDL: crea las 3 tablas y políticas RLS
│   ├── migrate_add_product_columns.sql  # Migración: añade icono, descripcion, caracteristicas
│   ├── seed.sql                  # DML: 46 productos completos con todos los campos
│   ├── data_dictionary.md        # Descripción de cada campo de cada tabla
│   └── MANTENIMIENTO.md          # Guía para agregar/modificar productos
│
└── scripts/ETL/
    ├── Bronze/
    │   └── raw_data.py           # Extracción de datos crudos desde Supabase
    ├── Silver/
    │   └── transformed_data.py   # Limpieza, validación y enriquecimiento
    └── Gold/
        └── visualization_data.py  # Agregaciones finales para análisis y visualización
```

---

## Arquitectura del sistema

```
┌─────────────────────────────────────────────┐
│           USUARIO (Estudiante UPY)           │
│           GitHub Pages / localhost           │
└────────────────────┬────────────────────────┘
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────┐
│                 FRONTEND                     │
│  auth.js → login/registro @upy.edu.mx        │
│  ui.js → carga catálogo desde DB             │
│  telemetry.js → eventos con auth.uid()       │
│  supabaseClient.js → cliente supabase-js     │
└────────────────────┬────────────────────────┘
                     │ supabase-js v2 (REST API)
                     ▼
┌─────────────────────────────────────────────┐
│              SUPABASE (PostgreSQL)           │
│  Auth: usuarios @upy.edu.mx                  │
│  usuarios_sesion (perfil: carrera, género)   │
│  catalogo_productos (46 productos)           │
│  interacciones_telemetria (eventos)          │
└────────────────────┬────────────────────────┘
                     │ supabase-py
                     ▼
┌─────────────────────────────────────────────┐
│           PIPELINE ETL (Python)              │
│  Bronze → Silver → Gold                     │
│  (extracción → limpieza → análisis)          │
└─────────────────────────────────────────────┘
```

---

## Autenticación con correo institucional

El acceso a UpyMarket requiere un correo `@upy.edu.mx` válido. El sistema usa **Supabase Auth** con confirmación por email.

### Flujo de registro

```
1. Usuario abre el sitio → aparece modal de Iniciar Sesión / Crear Cuenta
2. En "Crear Cuenta": ingresa correo @upy.edu.mx, contraseña (≥8 chars), carrera y género
3. Supabase envía correo de confirmación al email institucional
4. Usuario hace clic en el enlace del correo → sesión activada
5. onAuthStateChange detecta SIGNED_IN → crea perfil en usuarios_sesion (una sola vez)
6. Modal se cierra, el avatar muestra las iniciales del correo
```

### Flujo de login

```
1. Usuario ingresa correo @upy.edu.mx + contraseña
2. Supabase Auth valida → devuelve sesión con auth.uid()
3. Modal se cierra, usuario accede al marketplace
```

### Restricciones

- Solo se aceptan correos que terminen en `@upy.edu.mx` (validación cliente y Supabase Auth)
- El modal **no se puede cerrar** sin autenticarse — bloquea el acceso a todo el contenido
- El avatar en el header muestra las 2 primeras letras del correo y permite cerrar sesión

### RLS vinculado a auth.uid()

Las políticas de seguridad de la DB exigen que `usuarios_sesion.id = auth.uid()`, es decir, cada usuario solo puede insertar/leer su propio perfil:

```sql
-- Solo el usuario autenticado puede insertar su propio perfil
CREATE POLICY "Insertar perfil propio"
ON public.usuarios_sesion FOR INSERT TO authenticated
WITH CHECK (id = auth.uid());

-- Solo el usuario autenticado puede leer su propio perfil
CREATE POLICY "Leer perfil propio"
ON public.usuarios_sesion FOR SELECT TO authenticated
USING (id = auth.uid());
```

La telemetría también se vincula al `auth.uid()` real de la sesión activa, eliminando los UUIDs anónimos del sistema anterior.

---

## Base de datos (Supabase)

### Tabla `usuarios_sesion`
Perfil del estudiante autenticado. El `id` coincide exactamente con `auth.uid()` de Supabase Auth.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID (PK) | Igual a `auth.uid()` — no se genera automáticamente |
| `carrera` | VARCHAR(100) | Carrera del estudiante |
| `genero` | VARCHAR(50) | Género seleccionado |
| `created_at` | TIMESTAMPTZ | Fecha/hora de primer login |

Carreras válidas: `Ingeniería en Ciberseguridad`, `Ingeniería en Datos e IA`, `Ingeniería en Robótica Computacional`, `Ingeniería en Sistemas Embebidos Computacionales`

Géneros válidos: `Femenino`, `Masculino`, `No binario`, `Prefiero no decir`

---

### Tabla `catalogo_productos`
Catálogo de 46 productos. La fuente de verdad es `db/seed.sql`. El frontend carga los productos **desde esta tabla** al iniciar.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | VARCHAR(100) (PK) | Clave legible (`p1` … `p46`) |
| `nombre` | VARCHAR(255) | Nombre completo del producto |
| `categoria_general` | VARCHAR(50) | `Académico`, `Entretenimiento`, `Laptop`, `Books`, `Food`, `Services`, `Sports`, `Other` |
| `carrera_objetivo` | VARCHAR(100) | `'Todas'` o carrera específica |
| `tiene_gpu_dedicada` | BOOLEAN | `true` solo para laptops con GPU RTX |
| `precio_original` | DECIMAL(10,2) | Precio en MXN |
| `porcentaje_descuento` | DECIMAL(3,2) | Descuento en decimal (0.15 = 15%) |
| `icono` | TEXT | Emoji representativo del producto |
| `descripcion` | TEXT | Descripción corta del producto |
| `caracteristicas` | TEXT[] | Lista de características para el modal de detalle |
| `created_at` | TIMESTAMPTZ | Fecha de alta |

> Para agregar, modificar o eliminar productos, ver `db/MANTENIMIENTO.md`.

---

### Tabla `interacciones_telemetria` *(tabla de hechos)*
Registra cada evento del usuario con su identidad real de Supabase Auth.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID (PK) | Generado automáticamente |
| `usuario_id` | UUID | `auth.uid()` del usuario activo (nullable si no hay sesión) |
| `producto_id` | VARCHAR(100) | ID del producto involucrado |
| `tipo_evento` | VARCHAR(50) | `'view'`, `'add_to_cart'` o `'purchase'` |
| `dwell_time_segundos` | DECIMAL(10,2) | Segundos entre `view` y `add_to_cart` (nullable) |
| `precio_pagado` | DECIMAL(10,2) | Precio final pagado, solo en `purchase` (nullable) |
| `metodo_pago` | VARCHAR(100) | Método de pago, solo en `purchase` (nullable) |
| `es_fin_de_semana` | BOOLEAN | `true` si ocurrió sábado o domingo |
| `created_at` | TIMESTAMPTZ | Marca de tiempo exacta del evento |

---

### Políticas RLS activas

| Tabla | Rol | Operación | Condición |
|-------|-----|-----------|-----------|
| `usuarios_sesion` | `authenticated` | INSERT | `id = auth.uid()` |
| `usuarios_sesion` | `authenticated` | SELECT | `id = auth.uid()` |
| `interacciones_telemetria` | `authenticated` | INSERT | sin restricción adicional |
| `catalogo_productos` | público | SELECT | sin RLS (lectura libre) |

---

## Frontend — Componentes y flujo

### `config.js`
Script cargado antes de los ES modules. Expone credenciales como variables globales:
```javascript
window.UPYSTORE_SUPABASE_URL      = 'https://...supabase.co';
window.UPYSTORE_SUPABASE_ANON_KEY = 'eyJ...';
```
La clave `anon` es segura para exponer públicamente gracias a las políticas RLS.

---

### `assets/supabase.min.js`
Bundle de `@supabase/supabase-js@2` descargado y servido desde el mismo origen para evitar que Microsoft Edge bloquee requests a `cdn.jsdelivr.net` por Tracking Prevention.

---

### `scripts/supabaseClient.js`
Inicializa el cliente y exporta tres funciones:

```javascript
cargarProductos()              // → array de 46 productos desde la DB
insertarPerfil(userId, carrera, genero)  // → crea perfil en usuarios_sesion
insertarTelemetria(payload)    // → inserta evento, fire-and-forget
```

---

### `scripts/auth.js`
Modal de autenticación con dos tabs: **Iniciar Sesión** y **Crear Cuenta**.

- Valida que el correo termine en `@upy.edu.mx` antes de enviar a Supabase
- `signUp` guarda `carrera` y `genero` en `user_metadata`
- `onAuthStateChange(SIGNED_IN)` → crea el perfil en `usuarios_sesion` (solo si no existe)
- El modal bloquea todo el contenido hasta que el usuario esté autenticado
- El avatar en el header muestra iniciales del email y permite cerrar sesión con confirmación

---

### `scripts/ui.js`
Módulo principal de interfaz. Carga productos desde la DB al iniciar, luego renderiza el catálogo.

- **`cargarProductos()`** — fetch async a `catalogo_productos` al cargar la página
- **`renderCatalog()`** — genera tarjetas con `buildCard()`, inserta en `#catalog-grid`
- **Filtros** — chips por categoría y barra de búsqueda por texto
- **Event delegation** — un listener en `#catalog-grid` para "Ver Detalles" y "Agregar al Carrito"
- **Modal de detalle** — muestra `descripcion`, `caracteristicas[]`, precio con/sin descuento
- **Carrito** — estado en `sessionStorage`, con cantidad, total y checkout
- **Toast** — notificación temporal al agregar al carrito

---

### `assets/style.css`
Tema claro con glass morphism y paleta institucional UPY. Variables principales:

| Variable | Uso |
|----------|-----|
| `--purple-main: #5b167d` | Color primario UPY |
| `--purple-dark: #321047` | Textos activos, hover |
| `--gold-accent: #d6a21e` | Acentos, botones primarios |
| `--surface-muted: #f2eef5` | Fondos de secciones secundarias |

---

## Sistema de telemetría

Cada evento registra un payload vinculado al `auth.uid()` real del usuario:

```javascript
{
  usuario_id:          UUID | null,    // auth.uid() de la sesión activa
  producto_id:         'p1' ... 'p46',
  tipo_evento:         'view' | 'add_to_cart' | 'purchase',
  dwell_time_segundos: number | null,  // tiempo entre view y add_to_cart
  precio_pagado:       number | null,  // solo en purchase
  metodo_pago:         string | null,  // solo en purchase
  es_fin_de_semana:    boolean
}
```

### Flujo de eventos

```
Usuario abre detalle del producto
  └─► trackView(productoId)
        → tipo_evento = 'view'
        → inicia temporizador interno

Usuario hace clic en "Agregar al carrito"
  └─► trackAddToCart(productoId, precio)
        → tipo_evento = 'add_to_cart'
        → dwell_time = segundos desde trackView

Usuario hace clic en "Finalizar Compra"
  └─► trackPurchase(cartItems, metodoPago)
        → tipo_evento = 'purchase' (uno por ítem del carrito)
        → precio_pagado = precio final con descuento
        → metodo_pago = método seleccionado
```

---

## Preguntas de investigación

| # | Investigador | Pregunta | Campos usados |
|---|-------------|----------|---------------|
| 1 | Rama | ¿Cuándo compran más: entre semana o fin de semana? | `tipo_evento='purchase'` + `es_fin_de_semana` |
| 2 | Russel | ¿Estudiantes de qué carrera ven laptops GPU por más tiempo? | `dwell_time_segundos` + `carrera` + `tiene_gpu_dedicada` |
| 3 | Edgardo | ¿Se gasta más en Académico o Entretenimiento? | `precio_pagado` agrupado por `categoria_general` |
| 4 | Damian Novelo | ¿Descuentos ≥15% aumentan la tasa de compra? | ratio `purchase/view` por `porcentaje_descuento >= 0.15` |
| 5 | Lukaku Jr | ¿Cuánto dwell time precede un add_to_cart por categoría? | `dwell_time_segundos` en `add_to_cart` por `categoria_general` |
| 6 | Bianca Acosta | ¿Diferencia de compras entre géneros? | `tipo_evento='purchase'` agrupado por `genero` |
| 7 | Jonathan | ¿Productos con descuento se compran más? | `purchase` donde `porcentaje_descuento > 0` vs `= 0` |
| 8 | Isaac | ¿Alumnos con Beca Benito Juárez compran lo de su carrera? | `metodo_pago='Beca Benito Juárez'` + match `carrera` vs `carrera_objetivo` |

---

## Pipeline ETL (Arquitectura Medallón)

### Bronze — Datos crudos
**Archivo:** `scripts/ETL/Bronze/raw_data.py`

Conecta a Supabase con `supabase-py` y extrae las tres tablas completas como DataFrames de pandas sin transformación.

```bash
export SUPABASE_URL="https://...supabase.co"
export SUPABASE_KEY="eyJ..."
python scripts/ETL/Bronze/raw_data.py
```

### Silver — Limpieza y enriquecimiento
**Archivo:** `scripts/ETL/Silver/transformed_data.py`

- Elimina duplicados y registros con campos críticos nulos
- Une `interacciones_telemetria` con `usuarios_sesion` y `catalogo_productos`
- Calcula `precio_final = precio_original * (1 - porcentaje_descuento)`
- Filtra outliers en `dwell_time_segundos`

### Gold — Agregaciones para análisis
**Archivo:** `scripts/ETL/Gold/visualization_data.py`

Produce DataFrames listos para visualización:
- Conversión por categoría y nivel de descuento
- Dwell time promedio por carrera y tipo de producto
- Distribución de métodos de pago
- Volumen de compras por género y día de semana

---

## Catálogo de productos

46 productos en 8 categorías, precios en MXN. La fuente de verdad es `db/seed.sql` en Supabase.

### Académico (14 productos — p1–p12, p31, p32)
| ID | Producto | Carrera objetivo | Precio MXN | Descuento |
|----|----------|-----------------|-----------|-----------|
| p1 | Planner Académico Pro UPY | Todas | $249 | — |
| p2 | Microsoft Office 365 Estudiante | Todas | $1,099 | 15% |
| p3 | Curso Python para Datos e IA | Ing. Datos e IA | $799 | 20% |
| p4 | Cálculo Diferencial e Integral (Pack Digital) | Todas | $399 | — |
| p5 | Curso Machine Learning con TensorFlow | Ing. Datos e IA | $1,199 | 10% |
| p6 | Curso Ethical Hacking & Pentesting | Ing. Ciberseguridad | $999 | 25% |
| p7 | Kit Arduino Uno R4 Starter Pro | Ing. Sistemas Embebidos | $949 | — |
| p8 | Raspberry Pi 5 (8 GB) Kit Completo | Ing. Robótica Computacional | $2,499 | — |
| p9 | Curso Robótica con ROS 2 | Ing. Robótica Computacional | $1,499 | 15% |
| p10 | Álgebra Lineal para IA (eBook + Ejercicios) | Ing. Datos e IA | $349 | — |
| p11 | Certificación CompTIA Security+ (Prep) | Ing. Ciberseguridad | $1,799 | 10% |
| p12 | Kit Sensores IoT Avanzados | Ing. Sistemas Embebidos | $749 | — |
| p31 | Pack de Apuntes UPY: Cálculo y Física | Todas | $189 | — |
| p32 | Servicio de Tutorías Express en Python | Ing. Datos e IA | $250 | 12% |

### Entretenimiento (10 productos — p13–p20, p33, p34)
| ID | Producto | Precio MXN | Descuento |
|----|----------|-----------|-----------|
| p13 | Audífonos JBL Tune 520BT | $899 | — |
| p14 | Bocina JBL Go 4 | $1,099 | 10% |
| p15 | Control Xbox Wireless | $1,399 | — |
| p16 | Spotify Premium Estudiante 3 meses | $177 | 50% |
| p17 | Mochila Antirrobo con Puerto USB | $1,199 | 15% |
| p18 | Silla Ergonómica de Escritorio | $3,999 | 20% |
| p19 | Mouse Logitech MX Anywhere 3S | $1,599 | — |
| p20 | Teclado Mecánico TKL RGB | $1,299 | — |
| p33 | Canva Pro Estudiante (6 meses) | $420 | 18% |
| p34 | Combo Snack de Cafetería UPY | $95 | — |

### Laptop (12 productos — p21–p30, p35, p36)
| ID | Producto | GPU | Precio MXN | Descuento |
|----|----------|-----|-----------|-----------|
| p21 | ASUS VivoBook 15 (i5 13ª gen) | — | $13,499 | — |
| p22 | HP 255 G10 (Ryzen 5 7520U) | — | $11,999 | 10% |
| p23 | Dell Inspiron 15 3530 (i5) | — | $14,999 | 5% |
| p24 | Lenovo IdeaPad Slim 5 (Ryzen 7) | — | $15,499 | — |
| p25 | Acer Aspire 5 (i7 13ª gen) | — | $16,999 | 8% |
| p26 | ASUS TUF Gaming A15 (RTX 4060) | RTX | $22,999 | 15% |
| p27 | Lenovo Legion 5 Gen 9 (RTX 4070) | RTX | $28,999 | — |
| p28 | MSI Thin GF63 (RTX 4050) | RTX | $19,999 | 10% |
| p29 | Acer Nitro 5 (RTX 4060 Ti) | RTX | $24,999 | — |
| p30 | HP Victus 16 (RTX 3050 Ti) | RTX | $21,499 | 10% |
| p35 | MacBook Air M2 (16 GB RAM) | — | $25,999 | 5% |
| p36 | Gigabyte G5 KF (RTX 4060) | RTX | $23,999 | 14% |

### Otras categorías (10 productos)
| ID | Categoría | Producto | Precio MXN | Descuento |
|----|-----------|----------|-----------|-----------|
| p37 | Books | Engineering Formula Handbook | $145 | — |
| p38 | Books | Second-hand Data Structures Textbook | $320 | 10% |
| p39 | Food | UPY Lunch Combo Voucher | $89 | — |
| p40 | Food | Home-baked Brownie Box | $120 | 8% |
| p41 | Services | Resume and Portfolio Review | $180 | 15% |
| p42 | Services | Poster Design for School Projects | $260 | 12% |
| p43 | Sports | UPY Sports Jersey | $390 | 5% |
| p44 | Sports | Resistance Bands Kit | $210 | — |
| p45 | Other | Desk Setup Cable Organizer | $95 | — |
| p46 | Other | Custom UPY Sticker Pack | $70 | — |

---

## Levantar en local

El sitio es 100% estático. No se puede abrir `index.html` directamente desde el sistema de archivos porque los ES modules requieren HTTP.

### Opción 1 — Python (recomendado, sin instalación extra)
```bash
python -m http.server 8080
```
Abre: [http://localhost:8080](http://localhost:8080)

### Opción 2 — Node.js con `serve`
```bash
npx serve .
```

### Opción 3 — Extensión VS Code
Instala **Live Server** (Ritwick Dey) → clic derecho en `index.html` → *Open with Live Server*.

### Nota sobre el flujo de confirmación de email en local

Al registrarse, Supabase envía un correo de confirmación. El enlace de ese correo redirige al **Site URL** configurado en Supabase (producción). Para probar el flujo completo en local:

**Opción A (más rápida para dev):** Desactiva "Confirm email" en Supabase → Authentication → Providers → Email. El registro funciona inmediatamente sin confirmar.

**Opción B:** Agrega `http://localhost:8080/` a Supabase → Authentication → URL Configuration → Redirect URLs.

---

## Despliegue en GitHub Pages

1. Asegúrate de que `.nojekyll` existe en la raíz (ya incluido).
2. En GitHub: **Settings** → **Pages** → **Branch**: `main` → **Folder**: `/ (root)` → **Save**.
3. Espera ~1 min; el sitio quedará en `https://<usuario>.github.io/<repo>/`.

> No se necesita ningún build step. Todo funciona directamente desde los archivos estáticos.

---

## Configuración de Supabase (paso a paso)

### 1. Crear proyecto
Ve a [supabase.com](https://supabase.com) → **New Project** → elige región más cercana.

### 2. Ejecutar el schema
**SQL Editor** → pega el contenido de `db/schema.sql` → **Run**.

Crea las 3 tablas y las políticas RLS base.

### 3. Ejecutar la migración
**SQL Editor** → pega el contenido de `db/migrate_add_product_columns.sql` → **Run**.

Añade las columnas `icono`, `descripcion` y `caracteristicas` a `catalogo_productos`.

### 4. Ejecutar el seed
**SQL Editor** → pega el contenido de `db/seed.sql` → **Run**.

Inserta los 46 productos. Si ya hay datos, el `ON CONFLICT DO UPDATE` los actualiza sin error.

### 5. Configurar Auth
En Supabase → **Authentication → URL Configuration**:
- **Site URL**: `https://RusselKu.github.io/UpyMarket/`
- **Redirect URLs**: agregar `http://localhost:8080/` para pruebas locales

En **Authentication → Providers → Email**:
- Mantén activado "Confirm email" para producción

### 6. Configurar RLS para usuarios autenticados
Aplica las políticas de `db/schema.sql` que usan `auth.uid()`. Verifica en **Authentication → Policies** que existan para `usuarios_sesion` e `interacciones_telemetria`.

### 7. Obtener credenciales
**Settings → API**:
- **Project URL**: `https://xxxxx.supabase.co`
- **anon public**: clave que empieza con `eyJ...`

> Usa la clave `eyJ...` (anon legacy). Las nuevas claves `sb_publishable_` no son compatibles con `supabase-js@2`.

### 8. Editar `config.js`
```javascript
window.UPYSTORE_SUPABASE_URL      = 'https://TU-PROYECTO.supabase.co';
window.UPYSTORE_SUPABASE_ANON_KEY = 'eyJTU-CLAVE-ANON...';
```

### 9. Verificar que funciona
1. Abre el sitio → regístrate con un correo `@upy.edu.mx`
2. Confirma el email → inicia sesión
3. En Supabase → **Table Editor** → `usuarios_sesion` → debe aparecer tu registro con el UUID de Auth
4. Explora un producto → `interacciones_telemetria` → debe aparecer un evento `view` con tu `usuario_id`

---

## Notas técnicas

- **Sin framework ni build**: todo el JavaScript usa ES modules nativos del navegador. No hay npm, webpack ni bundler.
- **Productos desde la DB**: el catálogo se carga desde `catalogo_productos` en Supabase al iniciar. `assets/catalog.js` queda como referencia pero ya no se usa en producción.
- **Carrito en sessionStorage**: el estado del carrito se pierde al cerrar la pestaña (comportamiento esperado para un prototipo de investigación).
- **Telemetría fire-and-forget**: los errores de Supabase en telemetría no interrumpen la experiencia del usuario. Los fallos aparecen en la consola del navegador con el prefijo `[UpyMarket]`.
- **Compatibilidad GitHub Pages**: el archivo `.nojekyll` en la raíz es obligatorio para que GitHub Pages no procese los módulos ES con Jekyll.

---

*Proyecto académico — Universidad Politécnica de Yucatán · Ingeniería en Datos e IA*
