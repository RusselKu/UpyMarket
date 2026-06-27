-- ─────────────────────────────────────────────────────────────────────────────
-- Seed completo — UpyMarket v3 (46 productos)
-- Requiere haber ejecutado migrate_add_product_columns.sql primero
-- Ejecutar en Supabase Dashboard → SQL Editor
-- ─────────────────────────────────────────────────────────────────────────────

INSERT INTO public.catalogo_productos
  (id, nombre, categoria_general, carrera_objetivo, tiene_gpu_dedicada,
   precio_original, porcentaje_descuento, icono, descripcion, caracteristicas)
VALUES

  -- ── Académico ────────────────────────────────────────────────────────────

  ('p1',  'Planner Académico Pro UPY',
          'Académico', 'Todas', false, 249.00, 0.00,
          '📘',
          'Organiza tareas, proyectos y semanas de examen en una sola herramienta pensada para el ritmo universitario UPY.',
          ARRAY['Planeación semanal y mensual', 'Seguimiento de exámenes parciales', 'Registro de proyectos por materia', 'Formato digital editable PDF']),

  ('p2',  'Microsoft Office 365 Estudiante',
          'Académico', 'Todas', false, 1099.00, 0.15,
          '📊',
          'Suite completa con Word, Excel, PowerPoint y Teams. Incluye 1 TB en OneDrive y licencia para hasta 5 dispositivos.',
          ARRAY['Word, Excel, PowerPoint', 'Microsoft Teams incluido', '1 TB en OneDrive', 'Licencia anual renovable']),

  ('p3',  'Curso Python para Datos e IA',
          'Académico', 'Ingeniería en Datos e IA', false, 799.00, 0.20,
          '🐍',
          'Aprende Python desde cero: pandas, NumPy, scikit-learn y visualización con matplotlib. Certificado al terminar.',
          ARRAY['25 horas de contenido en video', 'Proyectos con datasets reales', 'Certificado digital incluido', 'Acceso de por vida']),

  ('p4',  'Cálculo Diferencial e Integral (Pack Digital)',
          'Académico', 'Todas', false, 399.00, 0.00,
          '📐',
          'Pack digital de los dos libros más usados en Cálculo en UPY. Ejercicios resueltos paso a paso con enfoque en Ingeniería.',
          ARRAY['Cálculo I y II en PDF', 'Ejercicios resueltos', 'Adaptado al plan de estudios UPY', 'Descarga inmediata']),

  ('p5',  'Curso Machine Learning con TensorFlow',
          'Académico', 'Ingeniería en Datos e IA', false, 1199.00, 0.10,
          '🤖',
          'Redes neuronales, CNN, RNN y modelos de lenguaje con TensorFlow y Keras. Incluye laboratorio en Google Colab.',
          ARRAY['40 horas de contenido', 'Laboratorios en Google Colab', 'Proyecto final de portafolio', 'Certificado reconocido']),

  ('p6',  'Curso Ethical Hacking & Pentesting',
          'Académico', 'Ingeniería en Ciberseguridad', false, 999.00, 0.25,
          '🔐',
          'Fundamentos de hacking ético: reconocimiento, explotación, post-explotación y reporte. Labs en Kali Linux y Metasploit.',
          ARRAY['Kali Linux y Metasploit', 'Laboratorios en entorno aislado', 'Técnicas OWASP Top 10', 'Certificado de Ethical Hacking']),

  ('p7',  'Kit Arduino Uno R4 Starter Pro',
          'Académico', 'Ingeniería en Sistemas Embebidos Computacionales', false, 949.00, 0.00,
          '⚙️',
          'Kit completo con Arduino Uno R4, 37 sensores, protoboard, jumpers, motores y guía de proyectos paso a paso.',
          ARRAY['Arduino Uno R4 WiFi', '37 módulos y sensores', 'Guía de 15 proyectos', 'Ideal para materias de sistemas embebidos']),

  ('p8',  'Raspberry Pi 5 (8 GB) Kit Completo',
          'Académico', 'Ingeniería en Robótica Computacional', false, 2499.00, 0.00,
          '🍓',
          'Raspberry Pi 5 con 8 GB RAM, case oficial, fuente de alimentación, tarjeta MicroSD 64 GB y disipador térmico.',
          ARRAY['Raspberry Pi 5 - 8 GB RAM', 'MicroSD 64 GB con Raspberry OS', 'Case oficial con ventilador', 'Fuente 5V/5A incluida']),

  ('p9',  'Curso Robótica con ROS 2 (Robot Operating System)',
          'Académico', 'Ingeniería en Robótica Computacional', false, 1499.00, 0.15,
          '🦾',
          'Diseño y programación de robots con ROS 2, Gazebo y Python. Simulaciones de brazos robóticos y navegación autónoma.',
          ARRAY['ROS 2 Humble Hawksbill', 'Simulaciones en Gazebo', 'Python para robótica', 'Proyecto: robot móvil autónomo']),

  ('p10', 'Álgebra Lineal para IA (eBook + Ejercicios)',
          'Académico', 'Ingeniería en Datos e IA', false, 349.00, 0.00,
          '🔢',
          'Vectores, matrices, valores propios y transformaciones lineales con enfoque en redes neuronales y machine learning.',
          ARRAY['Enfoque en IA y ML', '200+ ejercicios resueltos', 'Ejemplos en Python/NumPy', 'PDF interactivo']),

  ('p11', 'Certificación CompTIA Security+ (Prep)',
          'Académico', 'Ingeniería en Ciberseguridad', false, 1799.00, 0.10,
          '🛡️',
          'Curso preparatorio para CompTIA Security+ SY0-701. 500 preguntas de práctica, simulacros de examen y laboratorios.',
          ARRAY['Alineado a SY0-701', '500+ preguntas de práctica', '6 simulacros de examen completos', 'Válido 12 meses']),

  ('p12', 'Kit Electrónica: Sensores IoT Avanzados',
          'Académico', 'Ingeniería en Sistemas Embebidos Computacionales', false, 749.00, 0.00,
          '📡',
          'Pack de sensores IoT: temperatura, humedad, presión, ultrasonido, RFID y acelerómetro para proyectos embebidos.',
          ARRAY['15 sensores diferentes', 'Compatible con Arduino y ESP32', 'Cables y conectores incluidos', 'Guía de integración']),

  -- ── Entretenimiento ──────────────────────────────────────────────────────

  ('p13', 'Audífonos Inalámbricos JBL Tune 520BT',
          'Entretenimiento', 'Todas', false, 899.00, 0.00,
          '🎧',
          'Audífonos Bluetooth on-ear con 57 horas de batería, conexión multipunto y sonido potenciado por JBL Pure Bass.',
          ARRAY['57 horas de batería', 'Bluetooth 5.3 multipunto', 'JBL Pure Bass Sound', 'Plegables y portátiles']),

  ('p14', 'Bocina Portátil JBL Go 4',
          'Entretenimiento', 'Todas', false, 1099.00, 0.10,
          '🔊',
          'Bocina Bluetooth IP67 resistente al agua y al polvo. Sonido potente en formato ultra-compacto para el campus.',
          ARRAY['IP67 agua y polvo', 'Bluetooth 5.3', 'Batería 7 horas', 'Gancho de mosquetón incluido']),

  ('p15', 'Control Xbox Wireless (Carbon Black)',
          'Entretenimiento', 'Todas', false, 1399.00, 0.00,
          '🎮',
          'Control inalámbrico Xbox compatible con PC Windows, Android, iOS y cloud gaming. USB-C y triggers mejorados.',
          ARRAY['PC/Android/iOS/Cloud', 'Carga USB-C', 'Triggers con hápticos', 'Botón dedicado Share']),

  ('p16', 'Spotify Premium Estudiante (3 meses)',
          'Entretenimiento', 'Todas', false, 177.00, 0.50,
          '🎵',
          'Spotify Premium sin anuncios, modo offline y calidad de audio máxima. Descuento exclusivo para estudiantes UPY.',
          ARRAY['Sin anuncios', 'Modo sin conexión', 'Audio alta calidad 320 kbps', 'Precio exclusivo estudiantes']),

  ('p17', 'Mochila Antirrobo con Puerto USB',
          'Entretenimiento', 'Todas', false, 1199.00, 0.15,
          '🎒',
          'Mochila 30 L con cierre antirrobo oculto, compartimento acolchado para laptop 15.6" y puerto USB de carga externa.',
          ARRAY['30 L de capacidad', 'Puerto USB de carga externa', 'Compartimento laptop 15.6"', 'Material impermeable reforzado']),

  ('p18', 'Silla Ergonómica de Escritorio',
          'Entretenimiento', 'Todas', false, 3999.00, 0.20,
          '🪑',
          'Silla de escritorio ergonómica con soporte lumbar ajustable, reposapiés retráctil y reposabrazos 4D. Hasta 150 kg.',
          ARRAY['Soporte lumbar ajustable', 'Reposabrazos 4D', 'Reposapiés retráctil', 'Capacidad hasta 150 kg']),

  ('p19', 'Mouse Inalámbrico Logitech MX Anywhere 3S',
          'Entretenimiento', 'Todas', false, 1599.00, 0.00,
          '🖱️',
          'Mouse compacto con scroll electromagnético MagSpeed, DPI hasta 8000 y hasta 70 días de batería. Bluetooth + USB.',
          ARRAY['Scroll MagSpeed electromagnético', 'DPI 200–8000', 'Bluetooth + USB-C Unifying', '70 días de batería']),

  ('p20', 'Teclado Mecánico Compacto TKL RGB',
          'Entretenimiento', 'Todas', false, 1299.00, 0.00,
          '⌨️',
          'Teclado mecánico tenkeyless RGB con switches Gateron Red silenciosos, cable USB-C desmontable y cuerpo de aluminio.',
          ARRAY['Switches Gateron Red silenciosos', 'RGB por tecla programable', 'Cable USB-C desmontable', 'Marco de aluminio anodizado']),

  -- ── Laptop ───────────────────────────────────────────────────────────────

  ('p21', 'ASUS VivoBook 15 (Intel Core i5 13ª gen)',
          'Laptop', 'Todas', false, 13499.00, 0.00,
          '💻',
          'Laptop ultradelgada y ligera (1.7 kg) para clases, tareas y presentaciones. Pantalla FullHD 15.6" con batería de 12 horas.',
          ARRAY['Intel Core i5-1335U (13ª gen)', 'Pantalla 15.6" FHD IPS', '8 GB RAM DDR4', 'SSD 512 GB NVMe']),

  ('p22', 'HP 255 G10 (AMD Ryzen 5 7520U)',
          'Laptop', 'Todas', false, 11999.00, 0.10,
          '💻',
          'Laptop accesible y eficiente con Ryzen 5 y gráficos AMD Radeon integrados. Ideal para el día a día universitario.',
          ARRAY['AMD Ryzen 5 7520U', 'Gráficos AMD Radeon integrados', '8 GB RAM DDR5', 'SSD 256 GB + ranura amp.']),

  ('p23', 'Dell Inspiron 15 3530 (Intel i5)',
          'Laptop', 'Ingeniería en Ciberseguridad', false, 14999.00, 0.05,
          '💻',
          'Confiabilidad Dell con Core i5 de 13ª gen y SSD de 512 GB. Perfecta para laboratorios de seguridad y VMs ligeras.',
          ARRAY['Intel Core i5-1334U', 'RAM 16 GB DDR4 (amp. a 32)', 'SSD 512 GB NVMe', 'Windows 11 Pro incluido']),

  ('p24', 'Lenovo IdeaPad Slim 5 (AMD Ryzen 7)',
          'Laptop', 'Ingeniería en Sistemas Embebidos Computacionales', false, 15499.00, 0.00,
          '💻',
          'Diseño premium con Ryzen 7, pantalla 2.8K OLED 90 Hz y 16 GB de RAM. Múltiples puertos para conexión de hardware.',
          ARRAY['AMD Ryzen 7 7730U', 'Pantalla 14" 2.8K OLED 90 Hz', '16 GB RAM LPDDR4X', 'USB-A x3 + USB-C + HDMI']),

  ('p25', 'Acer Aspire 5 (Intel Core i7 13ª gen)',
          'Laptop', 'Ingeniería en Robótica Computacional', false, 16999.00, 0.08,
          '💻',
          'Core i7 de alto rendimiento con 16 GB RAM para simulaciones de robótica, compilación de código y entornos virtuales.',
          ARRAY['Intel Core i7-1355U', '16 GB RAM DDR5', 'SSD 512 GB PCIe 4.0', 'Pantalla 15.6" FHD IPS 100% sRGB']),

  ('p26', 'ASUS TUF Gaming A15 (RTX 4060)',
          'Laptop', 'Ingeniería en Datos e IA', true, 22999.00, 0.15,
          '🖥️',
          'GPU RTX 4060 con 8 GB VRAM ideal para entrenar modelos de IA, procesamiento de datos masivos y CUDA computing.',
          ARRAY['RTX 4060 8 GB VRAM + CUDA', 'AMD Ryzen 7 7745HX', '16 GB RAM DDR5', 'SSD 512 GB PCIe 4.0']),

  ('p27', 'Lenovo Legion 5 Gen 9 (RTX 4070)',
          'Laptop', 'Ingeniería en Robótica Computacional', true, 28999.00, 0.00,
          '🖥️',
          'Pantalla QHD 165 Hz con cobertura sRGB 100%, RTX 4070 y Ryzen 9 para simulaciones robóticas intensivas en Gazebo.',
          ARRAY['RTX 4070 8 GB VRAM', 'Pantalla 2K QHD 165 Hz 100% sRGB', 'AMD Ryzen 9 7945HX', '32 GB RAM DDR5']),

  ('p28', 'MSI Thin GF63 (RTX 4050)',
          'Laptop', 'Todas', true, 19999.00, 0.10,
          '🖥️',
          'Laptop delgada y ligera (1.86 kg) con RTX 4050. Potencia GPU sin el volumen de un equipo gaming tradicional.',
          ARRAY['RTX 4050 6 GB VRAM', 'Intel Core i5-13420H', '8 GB RAM (amp. a 32 GB)', 'Peso 1.86 kg']),

  ('p29', 'Acer Nitro 5 (RTX 4060 Ti)',
          'Laptop', 'Ingeniería en Datos e IA', true, 24999.00, 0.00,
          '🖥️',
          'RTX 4060 Ti con 8 GB VRAM, pantalla 144 Hz y enfriamiento dual. Máximo rendimiento para deep learning y renderizado.',
          ARRAY['RTX 4060 Ti 8 GB VRAM', 'Intel Core i7-13650HX', 'Pantalla 15.6" 144 Hz IPS', 'SSD 1 TB NVMe']),

  ('p30', 'HP Victus 16 (RTX 3050 Ti)',
          'Laptop', 'Todas', true, 21499.00, 0.10,
          '🖥️',
          'Precio accesible con GPU dedicada. RTX 3050 Ti para cómputo paralelo, visión por computadora y proyectos de IA ligeros.',
          ARRAY['RTX 3050 Ti 4 GB VRAM', 'AMD Ryzen 5 7535HS', 'Pantalla 16.1" FHD antirreflejo', '8 GB RAM (amp. a 16 GB)']),

  -- ── Extras Académico ─────────────────────────────────────────────────────

  ('p31', 'Pack de Apuntes UPY: Cálculo y Física',
          'Académico', 'Todas', false, 189.00, 0.00,
          '📚',
          'Compilado digital con resúmenes, formularios y ejercicios frecuentes de primer año para estudiantes UPY.',
          ARRAY['Formato PDF y Notion', 'Incluye simulador de exámenes', 'Actualizado al semestre actual', 'Descarga inmediata']),

  ('p32', 'Servicio de Tutorías Express en Python',
          'Académico', 'Ingeniería en Datos e IA', false, 250.00, 0.12,
          '👨‍💻',
          'Sesiones cortas de acompañamiento para tareas, depuración y preparación de exámenes de programación.',
          ARRAY['Sesiones de 45 minutos', 'Modalidad presencial o virtual', 'Enfoque en Python y pandas', 'Agenda flexible']),

  -- ── Extras Entretenimiento ───────────────────────────────────────────────

  ('p33', 'Canva Pro Estudiante (6 meses)',
          'Entretenimiento', 'Todas', false, 420.00, 0.18,
          '🎨',
          'Acceso compartido para diseño de presentaciones, CVs, posts y materiales visuales para proyectos estudiantiles.',
          ARRAY['Plantillas premium', 'Recursos gráficos incluidos', 'Ideal para presentaciones', 'Activación el mismo día']),

  ('p34', 'Combo Snack de Cafetería UPY',
          'Entretenimiento', 'Todas', false, 95.00, 0.00,
          '🍱',
          'Combo estudiantil con bebida, snack y descuento en recarga para jornadas largas de clase o laboratorio.',
          ARRAY['Disponible en horario matutino', 'Canje en campus', 'Presenta tu credencial', 'Ideal para entre clases']),

  -- ── Extras Laptop ────────────────────────────────────────────────────────

  ('p35', 'MacBook Air M2 (16 GB RAM)',
          'Laptop', 'Todas', false, 25999.00, 0.05,
          '💻',
          'Equipo ligero y silencioso para productividad, investigación, desarrollo web y trabajo académico diario.',
          ARRAY['Chip Apple M2', '16 GB de memoria unificada', 'SSD 512 GB', 'Batería de hasta 18 horas']),

  ('p36', 'Gigabyte G5 KF (RTX 4060)',
          'Laptop', 'Ingeniería en Datos e IA', true, 23999.00, 0.14,
          '🖥️',
          'Laptop de alto rendimiento con GPU dedicada para simulaciones, entrenamiento de modelos y trabajo intensivo.',
          ARRAY['RTX 4060 8 GB VRAM', 'Intel Core i7 de 13a generación', '16 GB RAM DDR5', 'Pantalla 15.6" 144 Hz']),

  -- ── Books ────────────────────────────────────────────────────────────────

  ('p37', 'Engineering Formula Handbook',
          'Books', 'Todas', false, 145.00, 0.00,
          '📚',
          'Compact guide with calculus, physics and electronics formulas commonly used during the first semesters at UPY.',
          ARRAY['Pocket-size format', 'Quick reference tabs', 'Includes unit conversions', 'Ideal for study sessions']),

  ('p38', 'Second-hand Data Structures Textbook',
          'Books', 'Ingeniería en Datos e IA', false, 320.00, 0.10,
          '📖',
          'Used textbook in very good condition with highlighted examples and extra notes for programming classes.',
          ARRAY['English edition', 'Clean pages', 'Good for algorithms courses', 'Ready for immediate pickup']),

  -- ── Food ─────────────────────────────────────────────────────────────────

  ('p39', 'UPY Lunch Combo Voucher',
          'Food', 'Todas', false, 89.00, 0.00,
          '🍔',
          'Student combo with main dish, drink and snack for busy class days or long lab sessions.',
          ARRAY['Redeemable on campus', 'Morning and afternoon schedule', 'Valid with student ID', 'Fresh menu rotation']),

  ('p40', 'Home-baked Brownie Box',
          'Food', 'Todas', false, 120.00, 0.08,
          '🍫',
          'Box of 6 brownies prepared by students, perfect for team meetings, presentations or gifting on campus.',
          ARRAY['6 assorted brownies', 'Same-day delivery inside campus', 'Student-made product', 'Custom note included']),

  -- ── Services ─────────────────────────────────────────────────────────────

  ('p41', 'Resume and Portfolio Review',
          'Services', 'Todas', false, 180.00, 0.15,
          '🧾',
          'One-on-one review session to improve your CV, LinkedIn profile and project portfolio before internships.',
          ARRAY['45-minute session', 'Feedback in English or Spanish', 'Portfolio checklist included', 'Ideal for internship season']),

  ('p42', 'Poster Design for School Projects',
          'Services', 'Todas', false, 260.00, 0.12,
          '🎨',
          'Custom visual design service for academic posters, expo stands and class presentations with UPY style.',
          ARRAY['Editable Canva file', 'Fast turnaround', 'Includes 2 revisions', 'Prepared for printing or digital display']),

  -- ── Sports ───────────────────────────────────────────────────────────────

  ('p43', 'UPY Sports Jersey',
          'Sports', 'Todas', false, 390.00, 0.05,
          '⚽',
          'Breathable student jersey for football, volleyball and campus tournaments with a modern athletic fit.',
          ARRAY['Lightweight fabric', 'Available in multiple sizes', 'UPY-inspired color palette', 'Good for team events']),

  ('p44', 'Resistance Bands Kit',
          'Sports', 'Todas', false, 210.00, 0.00,
          '💪',
          'Portable resistance bands for quick workouts between classes or for training at home without bulky equipment.',
          ARRAY['5 resistance levels', 'Includes carrying bag', 'Beginner friendly', 'Works for stretching and strength']),

  -- ── Other ────────────────────────────────────────────────────────────────

  ('p45', 'Desk Setup Cable Organizer',
          'Other', 'Todas', false, 95.00, 0.00,
          '🔌',
          'Simple accessory set to keep your desk cleaner during study sessions, streaming or hybrid classes.',
          ARRAY['Adhesive clips included', 'USB cable sleeves', 'Minimal design', 'Easy to install']),

  ('p46', 'Custom UPY Sticker Pack',
          'Other', 'Todas', false, 70.00, 0.00,
          '✨',
          'Set of vinyl stickers for laptops, tablets and bottles featuring tech, campus and student-life themes.',
          ARRAY['Water-resistant vinyl', '10 unique designs', 'Student-created illustrations', 'Good gift option'])

ON CONFLICT (id) DO UPDATE SET
  nombre               = EXCLUDED.nombre,
  categoria_general    = EXCLUDED.categoria_general,
  carrera_objetivo     = EXCLUDED.carrera_objetivo,
  tiene_gpu_dedicada   = EXCLUDED.tiene_gpu_dedicada,
  precio_original      = EXCLUDED.precio_original,
  porcentaje_descuento = EXCLUDED.porcentaje_descuento,
  icono                = EXCLUDED.icono,
  descripcion          = EXCLUDED.descripcion,
  caracteristicas      = EXCLUDED.caracteristicas;
