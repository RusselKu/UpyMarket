-- ─────────────────────────────────────────────────────────────────────────────
-- Seed del catálogo de productos — UpyMarket v2
-- Ejecutar en Supabase Dashboard → SQL Editor DESPUÉS de correr schema.sql
--
-- Mapeo categoria_frontend → categoria_general en DB:
--   Académico       → 'Académico',       tiene_gpu_dedicada = false
--   Entretenimiento → 'Entretenimiento', tiene_gpu_dedicada = false
--   Laptop sin GPU  → 'Laptop',          tiene_gpu_dedicada = false
--   Laptop con GPU  → 'Laptop',          tiene_gpu_dedicada = true
--
-- Carreras UPY disponibles:
--   'Todas' | 'Ingeniería en Ciberseguridad' | 'Ingeniería en Datos e IA'
--   'Ingeniería en Robótica Computacional'   | 'Ingeniería en Sistemas Embebidos Computacionales'
--
-- Precios en MXN
-- ─────────────────────────────────────────────────────────────────────────────

INSERT INTO public.catalogo_productos
  (id, nombre, categoria_general, carrera_objetivo, tiene_gpu_dedicada, precio_original, porcentaje_descuento)
VALUES

  -- ── Académico (12 productos) ──────────────────────────────────────────────
  ('p1',  'Planner Académico Pro UPY',
          'Académico', 'Todas',                                          false,  249.00, 0.00),
  ('p2',  'Microsoft Office 365 Estudiante',
          'Académico', 'Todas',                                          false, 1099.00, 0.15),
  ('p3',  'Curso Python para Datos e IA',
          'Académico', 'Ingeniería en Datos e IA',                       false,  799.00, 0.20),
  ('p4',  'Cálculo Diferencial e Integral (Pack Digital)',
          'Académico', 'Todas',                                          false,  399.00, 0.00),
  ('p5',  'Curso Machine Learning con TensorFlow',
          'Académico', 'Ingeniería en Datos e IA',                       false, 1199.00, 0.10),
  ('p6',  'Curso Ethical Hacking & Pentesting',
          'Académico', 'Ingeniería en Ciberseguridad',                   false,  999.00, 0.25),
  ('p7',  'Kit Arduino Uno R4 Starter Pro',
          'Académico', 'Ingeniería en Sistemas Embebidos Computacionales',false,  949.00, 0.00),
  ('p8',  'Raspberry Pi 5 (8 GB) Kit Completo',
          'Académico', 'Ingeniería en Robótica Computacional',           false, 2499.00, 0.00),
  ('p9',  'Curso Robótica con ROS 2',
          'Académico', 'Ingeniería en Robótica Computacional',           false, 1499.00, 0.15),
  ('p10', 'Álgebra Lineal para IA (eBook + Ejercicios)',
          'Académico', 'Ingeniería en Datos e IA',                       false,  349.00, 0.00),
  ('p11', 'Certificación CompTIA Security+ (Prep)',
          'Académico', 'Ingeniería en Ciberseguridad',                   false, 1799.00, 0.10),
  ('p12', 'Kit Electrónica: Sensores IoT Avanzados',
          'Académico', 'Ingeniería en Sistemas Embebidos Computacionales',false,  749.00, 0.00),

  -- ── Entretenimiento (8 productos) ─────────────────────────────────────────
  ('p13', 'Audífonos Inalámbricos JBL Tune 520BT',
          'Entretenimiento', 'Todas',                                    false,  899.00, 0.00),
  ('p14', 'Bocina Portátil JBL Go 4',
          'Entretenimiento', 'Todas',                                    false, 1099.00, 0.10),
  ('p15', 'Control Xbox Wireless (Carbon Black)',
          'Entretenimiento', 'Todas',                                    false, 1399.00, 0.00),
  ('p16', 'Spotify Premium Estudiante (3 meses)',
          'Entretenimiento', 'Todas',                                    false,  177.00, 0.50),
  ('p17', 'Mochila Antirrobo con Puerto USB',
          'Entretenimiento', 'Todas',                                    false, 1199.00, 0.15),
  ('p18', 'Silla Ergonómica de Escritorio',
          'Entretenimiento', 'Todas',                                    false, 3999.00, 0.20),
  ('p19', 'Mouse Inalámbrico Logitech MX Anywhere 3S',
          'Entretenimiento', 'Todas',                                    false, 1599.00, 0.00),
  ('p20', 'Teclado Mecánico Compacto TKL RGB',
          'Entretenimiento', 'Todas',                                    false, 1299.00, 0.00),

  -- ── Laptop sin GPU (5 productos) ──────────────────────────────────────────
  ('p21', 'ASUS VivoBook 15 (Intel Core i5 13ª gen)',
          'Laptop', 'Todas',                                             false, 13499.00, 0.00),
  ('p22', 'HP 255 G10 (AMD Ryzen 5 7520U)',
          'Laptop', 'Todas',                                             false, 11999.00, 0.10),
  ('p23', 'Dell Inspiron 15 3530 (Intel i5)',
          'Laptop', 'Ingeniería en Ciberseguridad',                      false, 14999.00, 0.05),
  ('p24', 'Lenovo IdeaPad Slim 5 (AMD Ryzen 7)',
          'Laptop', 'Ingeniería en Sistemas Embebidos Computacionales',  false, 15499.00, 0.00),
  ('p25', 'Acer Aspire 5 (Intel Core i7 13ª gen)',
          'Laptop', 'Ingeniería en Robótica Computacional',              false, 16999.00, 0.08),

  -- ── Laptop con GPU (5 productos) ──────────────────────────────────────────
  ('p26', 'ASUS TUF Gaming A15 (RTX 4060)',
          'Laptop', 'Ingeniería en Datos e IA',                          true,  22999.00, 0.15),
  ('p27', 'Lenovo Legion 5 Gen 9 (RTX 4070)',
          'Laptop', 'Ingeniería en Robótica Computacional',              true,  28999.00, 0.00),
  ('p28', 'MSI Thin GF63 (RTX 4050)',
          'Laptop', 'Todas',                                             true,  19999.00, 0.10),
  ('p29', 'Acer Nitro 5 (RTX 4060 Ti)',
          'Laptop', 'Ingeniería en Datos e IA',                         true,  24999.00, 0.00),
  ('p30', 'HP Victus 16 (RTX 3050 Ti)',
          'Laptop', 'Todas',                                             true,  21499.00, 0.10)

ON CONFLICT (id) DO UPDATE SET
  nombre               = EXCLUDED.nombre,
  categoria_general    = EXCLUDED.categoria_general,
  carrera_objetivo     = EXCLUDED.carrera_objetivo,
  tiene_gpu_dedicada   = EXCLUDED.tiene_gpu_dedicada,
  precio_original      = EXCLUDED.precio_original,
  porcentaje_descuento = EXCLUDED.porcentaje_descuento;
