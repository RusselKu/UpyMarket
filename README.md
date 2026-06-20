# UpyMarket — Marketplace Estudiantil UPY

Prototipo funcional de e-commerce estático para estudiantes de la **Universidad Politécnica de Yucatán (UPY)**. Diseñado para capturar telemetría de comportamiento de compra y alimentar un pipeline ETL de análisis de datos, todo desplegado como sitio estático en GitHub Pages sin necesidad de backend propio.

---

## Tabla de Contenidos

1. [Descripción general](#descripción-general)
2. [Stack tecnológico](#stack-tecnológico)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Arquitectura del sistema](#arquitectura-del-sistema)
5. [Base de datos (Supabase)](#base-de-datos-supabase)
6. [Frontend — Componentes y flujo](#frontend--componentes-y-flujo)
7. [Sistema de telemetría](#sistema-de-telemetría)
8. [Preguntas de investigación](#preguntas-de-investigación)
9. [Pipeline ETL (Arquitectura Medallón)](#pipeline-etl-arquitectura-medallón)
10. [Catálogo de productos](#catálogo-de-productos)
11. [Levantar en local](#levantar-en-local)
12. [Despliegue en GitHub Pages](#despliegue-en-github-pages)
13. [Configuración de Supabase (paso a paso)](#configuración-de-supabase-paso-a-paso)

---

## Descripción general

UpyMarket simula una tienda en línea donde estudiantes de Ingeniería de UPY pueden explorar y "comprar" productos académicos, de entretenimiento y laptops. Cada interacción del usuario genera un evento de telemetría que se almacena en Supabase para análisis posterior.

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
| Auth/seguridad | Row Level Security (RLS) con clave anon pública |
| Despliegue | GitHub Pages (sitio 100% estático) |
| Analytics pipeline | Python 3 + pandas + supabase-py |
| Librerías CDN | `@supabase/supabase-js@2` |

---

## Estructura del proyecto

```
UpyMarket/
│
├── index.html                   # Página principal (SPA estática)
├── config.js                    # Credenciales Supabase (URL + anon key)
├── .nojekyll                    # Evita procesamiento Jekyll en GitHub Pages
│
├── assets/
│   ├── style.css                # Estilos globales (glass morphism, dark theme)
│   └── catalog.js               # Catálogo de 30 productos como ES module
│
├── scripts/
│   ├── supabaseClient.js        # Inicialización del cliente y funciones de inserción
│   ├── onboarding.js            # Modal de bienvenida; captura carrera y género
│   ├── telemetry.js             # Funciones trackView / trackAddToCart / trackPurchase
│   └── ui.js                   # Renderizado dinámico del catálogo, carrito, filtros
│
├── db/
│   ├── schema.sql               # DDL: crea las 3 tablas y políticas RLS
│   ├── seed.sql                 # DML: inserta los 30 productos del catálogo
│   └── data_dictionary.md       # Descripción de cada campo de cada tabla
│
└── scripts/ETL/
    ├── Bronze/
    │   └── raw_data.py          # Extracción de datos crudos desde Supabase
    ├── Silver/
    │   └── transformed_data.py  # Limpieza, validación y enriquecimiento
    └── Gold/
        └── visualization_data.py # Agregaciones finales para análisis y visualización
```

---

## Arquitectura del sistema

```
┌─────────────────────────────────────────────┐
│           USUARIO (Estudiante UPY)           │
│              GitHub Pages (browser)          │
└────────────────────┬────────────────────────┘
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────┐
│                 FRONTEND                     │
│  index.html → ui.js → telemetry.js          │
│  onboarding.js → supabaseClient.js          │
└────────────────────┬────────────────────────┘
                     │ supabase-js v2 (REST API)
                     ▼
┌─────────────────────────────────────────────┐
│              SUPABASE (PostgreSQL)           │
│  usuarios_sesion                             │
│  catalogo_productos                          │
│  interacciones_telemetria                    │
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

## Base de datos (Supabase)

### Tabla `usuarios_sesion`
Perfil demográfico anónimo de cada estudiante al entrar a la tienda.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID (PK) | Generado automáticamente |
| `carrera` | VARCHAR(100) | Carrera del estudiante |
| `genero` | VARCHAR(50) | Género seleccionado |
| `created_at` | TIMESTAMPTZ | Fecha/hora de registro |

Carreras válidas: `Ingeniería en Ciberseguridad`, `Ingeniería en Datos e IA`, `Ingeniería en Robótica Computacional`, `Ingeniería en Sistemas Embebidos Computacionales`

Géneros válidos: `Femenino`, `Masculino`, `No binario`, `Prefiero no decir`

---

### Tabla `catalogo_productos`
Catálogo estático de productos. Pre-llenado con `seed.sql`.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | VARCHAR(100) (PK) | Clave legible (p1, p2, ... p30) |
| `nombre` | VARCHAR(255) | Nombre completo del producto |
| `categoria_general` | VARCHAR(50) | `'Académico'`, `'Entretenimiento'` o `'Laptop'` |
| `carrera_objetivo` | VARCHAR(100) | Carrera a la que va dirigido (`'Todas'` o carrera específica) |
| `tiene_gpu_dedicada` | BOOLEAN | `true` solo para laptops con GPU RTX |
| `precio_original` | DECIMAL(10,2) | Precio en MXN |
| `porcentaje_descuento` | DECIMAL(3,2) | Descuento en decimal (0.15 = 15%) |
| `created_at` | TIMESTAMPTZ | Fecha de alta |

---

### Tabla `interacciones_telemetria` *(tabla de hechos)*
El núcleo del proyecto. Registra cada evento del usuario.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID (PK) | Generado automáticamente |
| `usuario_id` | UUID (FK) | Referencia a `usuarios_sesion.id` |
| `producto_id` | VARCHAR(100) | ID del producto involucrado |
| `tipo_evento` | VARCHAR(50) | `'view'`, `'add_to_cart'` o `'purchase'` |
| `dwell_time_segundos` | DECIMAL(10,2) | Segundos entre `view` y `add_to_cart` (nullable) |
| `precio_pagado` | DECIMAL(10,2) | Precio final pagado, solo en `purchase` (nullable) |
| `metodo_pago` | VARCHAR(100) | Método de pago, solo en `purchase` (nullable) |
| `es_fin_de_semana` | BOOLEAN | `true` si ocurrió sábado o domingo |
| `created_at` | TIMESTAMPTZ | Marca de tiempo exacta del evento |

> **Nota:** La FK `producto_id → catalogo_productos.id` fue eliminada con `ALTER TABLE ... DROP CONSTRAINT` para permitir tracking de todos los productos aunque no existan en la tabla de catálogo. Los datos de telemetría siguen siendo válidos para análisis.

Métodos de pago válidos: `Beca Benito Juárez`, `Efectivo`, `Tarjeta Bancaria`, `Transferencia SPEI`

---

### Políticas RLS

Supabase tiene Row Level Security activo. Las políticas permiten que usuarios anónimos (`anon`) puedan **solo insertar** registros en `usuarios_sesion` e `interacciones_telemetria`. No pueden leer ni modificar registros de otros usuarios.

```sql
-- Permite que cualquier visitante registre su sesión
CREATE POLICY "Permitir registro de usuarios anonimos"
ON public.usuarios_sesion FOR INSERT TO anon WITH CHECK (true);

-- Permite tracking de eventos sin autenticación
CREATE POLICY "Permitir tracking anonimo"
ON public.interacciones_telemetria FOR INSERT TO anon WITH CHECK (true);
```

---

## Frontend — Componentes y flujo

### `config.js`
Script cargado **antes** de los ES modules. Expone las credenciales de Supabase como variables globales:
```javascript
window.UPYSTORE_SUPABASE_URL  = 'https://...supabase.co';
window.UPYSTORE_SUPABASE_ANON_KEY = 'eyJ...';
```
La clave `anon` es segura para exponer públicamente gracias a las políticas RLS.

---

### `scripts/supabaseClient.js`
Inicializa el cliente `supabase-js@2` y exporta dos funciones:

```javascript
insertarUsuario(carrera, genero)   // → UUID del nuevo usuario
insertarTelemetria(payload)        // → void, fire-and-forget
```

---

### `scripts/onboarding.js`
Gestiona el modal de bienvenida:
1. Al cargar, revisa `localStorage`/`sessionStorage` si ya hay perfil guardado.
2. Si no hay perfil → muestra el modal.
3. Al enviar el formulario → llama `insertarUsuario()` → guarda `{ carrera, genero, userId }` en storage codificado en Base64.
4. Actualiza las iniciales del avatar en el header con la carrera seleccionada.

Exporta `getUserProfile()` y `saveUserProfile()` para que `telemetry.js` pueda leer el `userId`.

---

### `assets/catalog.js`
Módulo ES que exporta el array `productos` con los 30 artículos del catálogo. Cada objeto tiene:

```javascript
{
  id, nombre, categoria, categoria_general,
  carrera_objetivo, tiene_gpu_dedicada,
  precio_original, porcentaje_descuento,
  icono, descripcion, caracteristicas[]
}
```

---

### `scripts/ui.js`
Módulo principal de interfaz. Importa `catalog.js` y `telemetry.js`. Responsabilidades:

- **`renderCatalog()`** — Genera las tarjetas de producto dinámicamente con `buildCard()`. Las inserta en `#catalog-grid`.
- **Filtros** — Chips de categoría (`Todos`, `Académico`, `Entretenimiento`, `Laptop`) y barra de búsqueda por texto.
- **"Ver Ofertas"** — Filtra el catálogo mostrando solo productos con `porcentaje_descuento > 0`.
- **Event delegation** — Un solo listener en `#catalog-grid` maneja clics en "Ver Producto" y "Agregar al Carrito" mediante `data-action`.
- **Carrito** — Estado en `sessionStorage`. Soporte para agregar, quitar y ver total. Renderizado reactivo.
- **Checkout** — Lee el método de pago seleccionado, llama `trackPurchase()`, vacía el carrito.
- **Modal de detalle** — Muestra descripción, características, precio con/sin descuento y botón de compra.
- **Toast** — Notificación temporal de 2.4 segundos al agregar al carrito.

---

### `assets/style.css`
Tema oscuro con glass morphism. Variables CSS principales:

| Variable | Valor | Uso |
|----------|-------|-----|
| `--bg-dark` | `#12061c` | Fondo principal |
| `--primary` | `#caa54b` | Dorado — acentos, logos, botones primarios |
| `--secondary` | `#7c3aed` | Morado — badges GPU, botones secundarios |
| `--glass` | `rgba(255,255,255,0.09)` | Fondo de tarjetas glass |
| `--muted` | `#d7cbe7` | Texto secundario |

Badges visuales en tarjetas:
- **`.discount-badge`** — Esquina superior derecha, rojo, muestra `−X%`
- **`.gpu-badge`** — Esquina superior izquierda, morado, solo en laptops con GPU
- **`.career-tag`** — Bajo el título, dorado, muestra carrera objetivo

---

## Sistema de telemetría

Cada evento registra un payload con este esquema:

```javascript
{
  usuario_id:          UUID | null,       // del perfil en storage
  producto_id:         'p1' ... 'p30',
  tipo_evento:         'view' | 'add_to_cart' | 'purchase',
  dwell_time_segundos: number | null,     // view → add_to_cart
  precio_pagado:       number | null,     // solo en purchase
  metodo_pago:         string | null,     // solo en purchase
  es_fin_de_semana:    boolean
}
```

### Flujo de eventos por acción del usuario

```
Usuario abre detalle del producto
  └─► trackView(productoId)
        → tipo_evento = 'view'
        → dwell_time = null
        → inicia temporizador interno

Usuario hace clic en "Agregar al carrito"
  └─► trackAddToCart(productoId, precio)
        → tipo_evento = 'add_to_cart'
        → dwell_time = tiempo desde trackView (segundos)
        → precio_pagado = precio con descuento

Usuario hace clic en "Finalizar Compra"
  └─► trackPurchase(cartItems, metodoPago)
        → tipo_evento = 'purchase' (uno por ítem)
        → precio_pagado = precio final del ítem
        → metodo_pago = método seleccionado
```

---

## Preguntas de investigación

El sistema de telemetría está diseñado para responder 8 preguntas de investigación del equipo:

| # | Investigador | Pregunta | Campos usados |
|---|-------------|----------|---------------|
| 1 | Rama | ¿Cuándo compran más: entre semana o fin de semana? | `tipo_evento='purchase'` + `es_fin_de_semana` |
| 2 | Russel | ¿Estudiantes de qué carrera ven laptops GPU por más tiempo? | `dwell_time_segundos` + `carrera` + `tiene_gpu_dedicada` |
| 3 | Edgardo | ¿Se gasta más en Académico o Entretenimiento? | `precio_pagado` agrupado por `categoria_general` |
| 4 | Damian Novelo | ¿Descuentos ≥15% aumentan la tasa de compra? | `purchase/view` ratio agrupado por `porcentaje_descuento >= 0.15` |
| 5 | Lukaku Jr | ¿Cuánto tiempo de dwell precede un add_to_cart por categoría? | `dwell_time_segundos` en `add_to_cart` por `categoria_general` |
| 6 | Bianca Acosta | ¿Diferencia de compras entre géneros? | `tipo_evento='purchase'` agrupado por `genero` |
| 7 | Jonathan | ¿Productos con descuento se compran más? | `purchase` donde `porcentaje_descuento > 0` vs `= 0` |
| 8 | Isaac | ¿Alumnos con Beca Benito Juárez compran lo de su carrera? | `metodo_pago='Beca Benito Juárez'` + match `carrera` vs `carrera_objetivo` |

---

## Pipeline ETL (Arquitectura Medallón)

Los scripts de Python en `scripts/ETL/` implementan la arquitectura de tres capas:

### Bronze — Datos crudos
**Archivo:** `scripts/ETL/Bronze/raw_data.py`

Conecta a Supabase con `supabase-py` y extrae las tres tablas completas como DataFrames de pandas sin transformación alguna.

```bash
# Variables de entorno requeridas
export SUPABASE_URL="https://...supabase.co"
export SUPABASE_KEY="eyJ..."

python scripts/ETL/Bronze/raw_data.py
```

---

### Silver — Limpieza y enriquecimiento
**Archivo:** `scripts/ETL/Silver/transformed_data.py`

- Elimina duplicados y registros con campos críticos nulos
- Convierte timestamps a `datetime`
- Une `interacciones_telemetria` con `usuarios_sesion` y `catalogo_productos` mediante joins
- Calcula columna `precio_final` = `precio_original * (1 - porcentaje_descuento)`
- Filtra outliers en `dwell_time_segundos`

---

### Gold — Agregaciones para análisis
**Archivo:** `scripts/ETL/Gold/visualization_data.py`

Produce los DataFrames finales listos para visualización:
- Conversión por categoría y descuento
- Dwell time promedio por carrera y tipo de producto
- Distribución de métodos de pago
- Volumen de compras por género y día de semana

---

## Catálogo de productos

30 productos en tres categorías, precios en MXN:

### Académico (12 productos)
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
| p10 | Álgebra Lineal para IA (eBook) | Ing. Datos e IA | $349 | — |
| p11 | Certificación CompTIA Security+ (Prep) | Ing. Ciberseguridad | $1,799 | 10% |
| p12 | Kit Sensores IoT Avanzados | Ing. Sistemas Embebidos | $749 | — |

### Entretenimiento (8 productos)
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

### Laptop — Sin GPU (5 productos)
| ID | Producto | Carrera objetivo | Precio MXN | Descuento |
|----|----------|-----------------|-----------|-----------|
| p21 | ASUS VivoBook 15 (i5 13ª gen) | Todas | $13,499 | — |
| p22 | HP 255 G10 (Ryzen 5 7520U) | Todas | $11,999 | 10% |
| p23 | Dell Inspiron 15 3530 (i5) | Ing. Ciberseguridad | $14,999 | 5% |
| p24 | Lenovo IdeaPad Slim 5 (Ryzen 7) | Ing. Sistemas Embebidos | $15,499 | — |
| p25 | Acer Aspire 5 (i7 13ª gen) | Ing. Robótica Computacional | $16,999 | 8% |

### Laptop — Con GPU dedicada (5 productos)
| ID | Producto | Carrera objetivo | Precio MXN | Descuento |
|----|----------|-----------------|-----------|-----------|
| p26 | ASUS TUF Gaming A15 (RTX 4060) | Ing. Datos e IA | $22,999 | 15% |
| p27 | Lenovo Legion 5 Gen 9 (RTX 4070) | Ing. Robótica Computacional | $28,999 | — |
| p28 | MSI Thin GF63 (RTX 4050) | Todas | $19,999 | 10% |
| p29 | Acer Nitro 5 (RTX 4060 Ti) | Ing. Datos e IA | $24,999 | — |
| p30 | HP Victus 16 (RTX 3050 Ti) | Todas | $21,499 | 10% |

---

## Levantar en local

El sitio es 100% estático. Solo necesitas un servidor de archivos; **no** se puede abrir `index.html` directamente desde el sistema de archivos porque los ES modules requieren HTTP.

### Opción 1 — Python (recomendado, sin instalación extra)
```bash
# Desde la raíz del proyecto
python -m http.server 8080
```
Abre: [http://localhost:8080](http://localhost:8080)

### Opción 2 — Node.js con `serve`
```bash
npx serve .
```

### Opción 3 — Extensión VS Code
Instala **Live Server** (Ritwick Dey) → clic derecho en `index.html` → *Open with Live Server*.

---

## Despliegue en GitHub Pages

1. Asegúrate de que `.nojekyll` existe en la raíz (ya incluido en el repo).
2. En GitHub: **Settings** → **Pages** → **Branch**: `main` → **Folder**: `/ (root)` → **Save**.
3. Espera ~1 min; el sitio quedará en `https://<usuario>.github.io/<repo>/`.

> No se necesita ningún build step. Todo funciona directamente desde los archivos estáticos.

---

## Configuración de Supabase (paso a paso)

### 1. Crear proyecto
Ve a [supabase.com](https://supabase.com) → **New Project** → elige región más cercana (US East o South America).

### 2. Ejecutar el schema
**SQL Editor** → pega el contenido de `db/schema.sql` → **Run**.

Esto crea las 3 tablas y las políticas RLS.

### 3. Ejecutar el seed
**SQL Editor** → pega el contenido de `db/seed.sql` → **Run**.

Inserta los 30 productos. Si ya hay datos previos, el `ON CONFLICT DO UPDATE` los actualiza sin error.

### 4. Eliminar FK de telemetría (ya aplicado)
```sql
ALTER TABLE public.interacciones_telemetria
  DROP CONSTRAINT interacciones_telemetria_producto_id_fkey;
```
Esto permite que la telemetría funcione para todos los productos del frontend aunque no estén en la tabla de catálogo de Supabase.

### 5. Obtener credenciales
**Settings** → **API**:
- **Project URL**: `https://xxxxx.supabase.co` (sin `/rest/v1/`)
- **anon public**: la clave que empieza con `eyJ...`

> Usa la clave `eyJ...` (legacy/anon). No uses las nuevas claves `sb_publishable_` ya que `supabase-js@2` no las soporta.

### 6. Editar `config.js`
```javascript
window.UPYSTORE_SUPABASE_URL      = 'https://TU-PROYECTO.supabase.co';
window.UPYSTORE_SUPABASE_ANON_KEY = 'eyJTU-CLAVE-ANON...';
```

### 7. Verificar que funciona
1. Abre el sitio → completa el modal de onboarding.
2. En Supabase → **Table Editor** → `usuarios_sesion` → debe aparecer un registro nuevo.
3. Haz clic en un producto → **Table Editor** → `interacciones_telemetria` → debe aparecer un evento `view`.

---

## Notas técnicas adicionales

- **Sin framework ni build**: todo el JavaScript usa ES modules nativos del navegador. No hay npm, webpack ni bundler.
- **Carrito en sessionStorage**: el estado del carrito se pierde al cerrar la pestaña (comportamiento esperado para un prototipo de investigación).
- **Perfil en localStorage**: el perfil del estudiante persiste entre sesiones para no mostrar el modal de onboarding repetidamente.
- **Telemetría fire-and-forget**: los errores de Supabase en la telemetría no interrumpen la experiencia del usuario. Los fallos se pueden ver en la consola del navegador.
- **Compatibilidad GitHub Pages**: el archivo `.nojekyll` en la raíz es obligatorio para que GitHub Pages no procese los archivos con Jekyll, lo que rompería las rutas de los módulos ES.

---

*Proyecto académico — Universidad Politécnica de Yucatán · Ingeniería en Datos e IA*
