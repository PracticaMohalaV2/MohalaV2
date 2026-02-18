-- =========================
-- Poblamiento de tabla Escala
-- =========================
INSERT INTO ESCALA 
    (ID_ESCALA, DESCRIPCION) 
VALUES 
(1, 'NO LOGRA LO ESPERADO'),
(2, 'LOGRA PARCIALMENTE LO ESPERADO'),
(3, 'LOGRA LO ESPERADO'),
(4, 'SUPERA LO ESPERADO');

-- =========================
-- Poblamiento de tabla Dimension
-- =========================
INSERT INTO DIMENSION 
    (ID_DIMENSION, NOMBRE_DIMENSION) 
VALUES 
    (1, 'Organizacionales'),
    (2, 'Funcionales');

-- =========================
-- Poblamiento de tabla Departamento
-- =========================
INSERT INTO DEPARTAMENTO 
    (ID_DEPARTAMENTO, NOMBRE_DEPARTAMENTO)
VALUES 
    (1, 'Gerencia General'),
    (2, 'Recursos Humanos'),
    (3, 'Tecnología de la Información'),
    (4, 'Operaciones y Logística'),
    (5, 'Comercial y Ventas'),
    (6, 'Finanzas y Contabilidad'),
    (7, 'Marketing y Comunicaciones'),
    (8, 'Servicio al Cliente'),
    (9, 'Producción'),
    (10, 'Calidad y Medio Ambiente');

-- =========================
-- Poblamiento de tabla Nivel Jerárquico
-- =========================
INSERT INTO NIVEL_JERARQUICO 
    (ID_NIVEL_JERARQUICO, NOMBRE_NIVEL_JERARQUICO) 
VALUES 
    (1, 'Operativo'),
    (2, 'Táctico'),
    (3, 'Estratégico');

-- =========================
-- Poblamiento de tabla Cargo
-- =========================

-- Cargos Operativos (Nivel 1)
INSERT INTO CARGO 
    (ID_CARGO, NOMBRE_CARGO, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES
    (1, 'Analista', 1),
    (2, 'Técnico en Informática', 1),
    (3, 'Asistente Administrativo', 1),
    (4, 'Cajero', 1),
    (5, 'Operario de Producción', 1),
    (6, 'Guardia de Seguridad', 1),
    (7, 'Chofer', 1),
    (8, 'Secretaria', 1),
    (9, 'Paramédico', 1),
    (10, 'Auxiliar de Enfermería', 1),
    (11, 'Vendedor', 1),
    (12, 'Contador Junior', 1),
    (13, 'Recepcionista', 1),
    (14, 'Auxiliar de Aseo', 1),
    (15, 'Digitador', 1);

-- Cargos Tácticos (Nivel 2)
INSERT INTO CARGO 
    (ID_CARGO, NOMBRE_CARGO, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES
    (16, 'Supervisor de Ventas', 2),
    (17, 'Jefe de Área', 2),
    (18, 'Coordinador de Proyectos', 2),
    (19, 'Ingeniero de Procesos', 2),
    (20, 'Jefe de Recursos Humanos', 2),
    (21, 'Encargado de Logística', 2),
    (22, 'Subgerente Comercial', 2),
    (23, 'Coordinador de Finanzas', 2),
    (24, 'Profesor Jefe', 2),
    (25, 'Médico Jefe de Servicio', 2),
    (26, 'Supervisor de Producción', 2),
    (27, 'Encargado de Calidad', 2),
    (28, 'Coordinador de Marketing', 2),
    (29, 'Jefe de Operaciones', 2),
    (30, 'Coordinador Académico', 2);

-- Cargos Estratégicos (Nivel 3)
INSERT INTO CARGO 
    (ID_CARGO, NOMBRE_CARGO, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES
    (31, 'Gerente General', 3),
    (32, 'Director de Operaciones', 3),
    (33, 'Director Médico', 3),
    (34, 'CEO', 3),
    (35, 'CFO', 3),
    (36, 'COO', 3),
    (37, 'Gerente de Innovación', 3),
    (38, 'Gerente de Finanzas', 3),
    (39, 'Gerente de Recursos Humanos', 3),
    (40, 'Gerente Comercial', 3),
    (41, 'Gerente de Marketing', 3),
    (42, 'Director Académico', 3),
    (43, 'Rector de Universidad', 3),
    (44, 'Socio Fundador', 3),
    (45, 'Presidente de Empresa', 3);

-- =========================
-- Poblamiento de tabla Competencia
-- =========================

-- Competencias Organizacionales (Dimension 1)
INSERT INTO COMPETENCIA 
    (ID_COMPETENCIA, NOMBRE_COMPETENCIA, DIMENSION_ID_DIMENSION)    
VALUES
    (1, 'Creatividad e Innovación', 1),
    (2, 'Enfoque de Negocio', 1),
    (3, 'Identificación Cultural', 1),
    (4, 'Trabajo en Equipo', 1),
    (5, 'Visión Global y Sistemática', 1);

-- Competencias Funcionales (Dimension 2)
INSERT INTO COMPETENCIA 
    (ID_COMPETENCIA, NOMBRE_COMPETENCIA, DIMENSION_ID_DIMENSION) 
VALUES
    (6, 'Análisis y Solución de Problemas', 2),
    (7, 'Aprendizaje e Innovación', 2),
    (8, 'Comunicación', 2),
    (9, 'Innovación', 2),
    (10, 'Liderazgo', 2),
    (11, 'Liderazgo y Desarrollo de Equipos', 2),
    (12, 'Orientación a la Rentabilidad', 2),
    (13, 'Orientación al Logro', 2),
    (14, 'Planificación Estratégica', 2),
    (15, 'Proactividad', 2);

-- =========================
-- Poblamiento de tabla Trabajador
-- =========================

-- NIVEL 1: GERENCIA GENERAL
INSERT INTO TRABAJADOR 
    (ID_TRABAJADOR, RUT, ID_JEFE_DIRECTO, NOMBRE, APELLIDO_PATERNO, APELLIDO_MATERNO, EMAIL, GENERO, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO, CARGO_ID_CARGO, DEPARTAMENTO_ID_DEPARTAMENTO)
VALUES 
    (1, '10.234.567-1', NULL, 'Roberto', 'Méndez', 'Castro', 'r.mendez@mohala.cl', 'Masculino', 3, 31, 1),
    (2, '12.456.789-2', NULL, 'Patricia', 'Lorca', 'Vial', 'p.lorca@mohala.cl', 'Femenino', 3, 20, 2);

-- NIVEL 2: JEFATURAS (Reportan al ID 1)
INSERT INTO TRABAJADOR 
    (ID_TRABAJADOR, RUT, ID_JEFE_DIRECTO, NOMBRE, APELLIDO_PATERNO, APELLIDO_MATERNO, EMAIL, GENERO, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO, CARGO_ID_CARGO, DEPARTAMENTO_ID_DEPARTAMENTO)
VALUES 
    (3, '11.345.678-3', 1, 'Andrés', 'Tapia', 'Ruiz', 'a.tapia@mohala.cl', 'Masculino', 2, 29, 3),
    (4, '13.567.890-4', 1, 'Mónica', 'Sánchez', 'Paz', 'm.sanchez@mohala.cl', 'Femenino', 2, 22, 5);

-- NIVEL 3: ANALISTAS Y OPERATIVOS

-- Reportan a RRHH (Jefe ID: 2)
INSERT INTO TRABAJADOR 
    (ID_TRABAJADOR, RUT, ID_JEFE_DIRECTO, NOMBRE, APELLIDO_PATERNO, APELLIDO_MATERNO, EMAIL, GENERO, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO, CARGO_ID_CARGO, DEPARTAMENTO_ID_DEPARTAMENTO)
VALUES 
    (5, '18.456.789-9', 2, 'Valeria', 'Cáceres', 'Pinto', 'v.caceres@mohala.cl', 'Femenino', 1, 8, 2),
    (6, '19.567.890-0', 2, 'Sebastián', 'Marín', 'Rojas', 's.marin@mohala.cl', 'Masculino', 1, 10, 2);


-- =========================
-- Poblamiento de tabla Textos_Evaluacion
-- =========================

-- 1. CREATIVIDAD E INNOVACIÓN (ID_COMPETENCIA: 1)
-- Operativo (Nivel 1), Táctico (Nivel 2), Estratégico (Nivel 3)
INSERT INTO TEXTOS_EVALUACION 
    (ID_TEXTOS_EVALUACION, CODIGO_EXCEL, TEXTO, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (1, 'CIO1.1', 'Trabaja con mecanismos conocidos y rutinarios.', 1, 1, 1),
    (2, 'CIO1.2', 'Se mueve con facilidad en situaciones conocidas con pautas de acción prefijadas.', 1, 1, 1),
    (3, 'CIO1.3', 'Implementa ideas y soluciones que le permiten resolver situaciones rutinarias y complejas.', 1, 1, 1),
    (4, 'CIT1.1', 'Promueve un estilo de gestión innovador y de vinculación con su entorno, brindando a su equipo herramientas para que trabajen con el mismo enfoque.', 1, 1, 2),
    (5, 'CIT1.2', 'Estructura equipos de alto rendimiento, que suelen tener formatos atípicos utilizando las formas más adecuadas para la consecución de sus objetivos.', 1, 1, 2),
    (6, 'CIT1.3', 'Lidera la implementación de nuevas ideas y soluciones dentro del negocio, es requerido por su aporte de creatividad y visión innovadora, que le permiten resolver situaciones complejas que otros no han podido solucionar.', 1, 1, 2),
    (7, 'CIE1.1', 'Es consultado por pares y subordinados porque se le reconoce por su habilidad de abordar desde nuevos enfoques los problemas y dificultades, pudiendo plantear alternativas impensadas.', 1, 1, 3),
    (8, 'CIE1.2', 'Es intelectualmente curioso, le gusta estar informado y mantenerse en constante aprendizaje para aplicar los conocimientos a la organización.', 1, 1, 3),
    (9, 'CIE1.3', 'Plantea mejoras o soluciones nuevas a problemas sencillos y complejos, garantizando su efectividad y calidad.', 1, 1, 3);

-- 2. ENFOQUE DE NEGOCIO (ID_COMPETENCIA: 2)
INSERT INTO TEXTOS_EVALUACION 
    (ID_TEXTOS_EVALUACION, CODIGO_EXCEL, TEXTO, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (10, 'ENO2.1', 'Comprende las peculiaridades de los servicios.', 1, 2, 1),
    (11, 'ENO2.2', 'Conoce las estrategias, principios y valores corporativos.', 1, 2, 1),
    (12, 'ENO2.3', 'Invierte tiempo adicional para identificar y capturar oportunidades de crecimiento y desarrollo de la empresa.', 1, 2, 1),
    (13, 'ENT2.1', 'Es capaz de establecer relaciones interpersonales en cualquier contexto, promoviendo los servicios a través del networking.', 1, 2, 2),
    (14, 'ENT2.2', 'Es hábil para adaptarse rápidamente y funcionar con eficacia en nuevos contextos laborales.', 1, 2, 2),
    (15, 'ENT2.3', 'Promueve en todas las áreas de trabajo, la capacidad para comprender las peculiaridades de los servicios.', 1, 2, 2),
    (16, 'ENE2.1', 'Desarrolla dentro y fuera de la organización la capacidad de adecuar productos, servicios y procedimientos organizacionales, a fin de amoldarse a nuevos contextos de acuerdo con la estrategia del negocio.', 1, 2, 3),
    (17, 'ENE2.2', 'Es un referente dentro y fuera de la organización por su capacidad de identificar y desarrollar oportunidades de negocio.', 1, 2, 3),
    (18, 'ENE2.3', 'Es reconocido por su expertise, su alto conocimiento  cultural y estrategias de relacionamiento.', 1, 2, 3);

-- 6. ANÁLISIS Y SOLUCIÓN DE PROBLEMAS (ID_COMPETENCIA: 6) 
INSERT INTO TEXTOS_EVALUACION  
    (ID_TEXTOS_EVALUACION, CODIGO_EXCEL, TEXTO, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (19, 'ASO1.1', 'Resuelve problemas rutinarios de forma efectiva.', 2, 6, 1),
    (20, 'ASO1.2', 'Acude a sus superiores o pares para crear alternativas que le permitan resolver los problemas con mayor grado de dificultad.', 2, 6, 1),
    (21, 'ASO1.3', 'Logra detectar las variables que influyen en el problema de forma oportuna.', 2, 6, 1),
    (22, 'AST1.1', 'Utiliza eficazmente datos históricos y actuales como ayuda para prever tendencias futuras, siendo efectivo en crear contingencias para que no afecten los resultados.', 2, 6, 2),
    (23, 'AST1.2', 'Analiza las relaciones entre las distintas partes y causales de un problema, anticipándose a los obstáculos y creando alternativas.', 2, 6, 2),
    (24, 'AST1.3', 'Aporta soluciones validas para la situación en tiempo y forma, responsabilizándose de ellas.', 2, 6, 2),
    (25, 'ASE1.1', 'Realiza análisis complejos utilizando hipótesis y diferentes escenarios, logrando rescatar los aspectos más significativos.', 2, 6, 3),
    (26, 'ASE1.2', 'Comprende problemas complejos y los define en torno a principios y estrategias organizacionales.', 2, 6, 3),
    (27, 'ASE1.3', 'Se anticipa a las situaciones, previendo y planteando respuestas adecuadas y rentables antes que se presente la situación. ', 2, 6, 3);

-- ==========================================================
-- Poblamiento DESCRIPCION RESPUESTA
-- ==========================================================

-- Competencia: Creatividad / Nivel: Operativo

-- CIO1.1
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (1, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'CIO1.1', 1, 1, 1, 1),
    (2, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'CIO1.1', 2, 1, 1, 1),
    (3, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'CIO1.1', 3, 1, 1, 1),
    (4, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'CIO1.1', 4, 1, 1, 1);

-- CIO1.2
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (5, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'CIO1.2', 1, 1, 1, 1),
    (6, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'CIO1.2', 2, 1, 1, 1),
    (7, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'CIO1.2', 3, 1, 1, 1),
    (8, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'CIO1.2', 4, 1, 1, 1);

-- CIO1.3
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (9, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'CIO1.3', 1, 1, 1, 1),
    (10, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'CIO1.3', 2, 1, 1, 1),
    (11, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'CIO1.3', 3, 1, 1, 1),
    (12, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'CIO1.3', 4, 1, 1, 1);

-- Competencia: Creatividad / Nivel: Táctico

-- CIT1.1
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (13, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'CIT1.1', 1, 1, 1, 2),
    (14, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'CIT1.1', 2, 1, 1, 2),
    (15, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'CIT1.1', 3, 1, 1, 2),
    (16, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'CIT1.1', 4, 1, 1, 2);

-- CIT1.2
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (17, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'CIT1.2', 1, 1, 1, 2),
    (18, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'CIT1.2', 2, 1, 1, 2),
    (19, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'CIT1.2', 3, 1, 1, 2),
    (20, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'CIT1.2', 4, 1, 1, 2);

-- CIT1.3
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (21, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'CIT1.3', 1, 1, 1, 2),
    (22, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'CIT1.3', 2, 1, 1, 2),
    (23, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'CIT1.3', 3, 1, 1, 2),
    (24, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'CIT1.3', 4, 1, 1, 2);

-- Competencia: Creatvidad / Nivel: Estratégico

-- CIE1.1
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (25, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'CIE1.1', 1, 1, 1, 3),
    (26, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'CIE1.1', 2, 1, 1, 3),
    (27, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'CIE1.1', 3, 1, 1, 3),
    (28, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'CIE1.1', 4, 1, 1, 3);

-- CIE1.2
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (29, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'CIE1.2', 1, 1, 1, 3),
    (30, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'CIE1.2', 2, 1, 1, 3),
    (31, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'CIE1.2', 3, 1, 1, 3),
    (32, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'CIE1.2', 4, 1, 1, 3);

-- CIE1.3
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (33, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'CIE1.3', 1, 1, 1, 3),
    (34, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'CIE1.3', 2, 1, 1, 3),
    (35, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'CIE1.3', 3, 1, 1, 3),
    (36, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'CIE1.3', 4, 1, 1, 3);

-- Competencia: Enfoque de Negocio / Nivel: Operativo

-- ENO2.1
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (37, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ENO2.1', 1, 1, 2, 1),
    (38, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ENO2.1', 2, 1, 2, 1),
    (39, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ENO2.1', 3, 1, 2, 1),
    (40, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ENO2.1', 4, 1, 2, 1);

-- ENO2.2
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (41, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ENO2.2', 1, 1, 2, 1),
    (42, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ENO2.2', 2, 1, 2, 1),
    (43, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ENO2.2', 3, 1, 2, 1),
    (44, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ENO2.2', 4, 1, 2, 1);

-- ENO2.3
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (45, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ENO2.3', 1, 1, 2, 1),
    (46, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ENO2.3', 2, 1, 2, 1),
    (47, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ENO2.3', 3, 1, 2, 1),
    (48, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ENO2.3', 4, 1, 2, 1);

-- Competencia: Enfoque de Negocio / Nivel: Táctico

-- ENT2.1
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (49, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ENT2.1', 1, 1, 2, 2),
    (50, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ENT2.1', 2, 1, 2, 2),
    (51, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ENT2.1', 3, 1, 2, 2),
    (52, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ENT2.1', 4, 1, 2, 2);

-- ENT2.2
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (53, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ENT2.2', 1, 1, 2, 2),
    (54, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ENT2.2', 2, 1, 2, 2),
    (55, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ENT2.2', 3, 1, 2, 2),
    (56, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ENT2.2', 4, 1, 2, 2);

-- ENT2.3
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (57, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ENT2.3', 1, 1, 2, 2),
    (58, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ENT2.3', 2, 1, 2, 2),
    (59, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ENT2.3', 3, 1, 2, 2),
    (60, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ENT2.3', 4, 1, 2, 2);

-- Competencia: Enfoque de Negocio / Nivel: Estratégico

-- ENE2.1
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (61, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ENE2.1', 1, 1, 2, 3),
    (62, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ENE2.1', 2, 1, 2, 3),
    (63, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ENE2.1', 3, 1, 2, 3),
    (64, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ENE2.1', 4, 1, 2, 3);

-- ENE2.2
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (65, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ENE2.2', 1, 1, 2, 3),
    (66, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ENE2.2', 2, 1, 2, 3),
    (67, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ENE2.2', 3, 1, 2, 3),
    (68, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ENE2.2', 4, 1, 2, 3);

-- ENE2.3
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (69, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ENE2.3', 1, 1, 2, 3),
    (70, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ENE2.3', 2, 1, 2, 3),
    (71, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ENE2.3', 3, 1, 2, 3),
    (72, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ENE2.3', 4, 1, 2, 3);

-- Competencia: Análisis y Solución de Problemas / Nivel: Operativo

-- ASO1.1
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (73, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ASO1.1', 1, 2, 6, 1),
    (74, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ASO1.1', 2, 2, 6, 1),
    (75, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ASO1.1', 3, 2, 6, 1),
    (76, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ASO1.1', 4, 2, 6, 1);

-- ASO1.2
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (77, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ASO1.2', 1, 2, 6, 1),
    (78, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ASO1.2', 2, 2, 6, 1),
    (79, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ASO1.2', 3, 2, 6, 1),
    (80, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ASO1.2', 4, 2, 6, 1);

-- ASO1.3
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (81, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ASO1.3', 1, 2, 6, 1),
    (82, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ASO1.3', 2, 2, 6, 1),
    (83, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ASO1.3', 3, 2, 6, 1),
    (84, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ASO1.3', 4, 2, 6, 1);

-- Competencia: Análisis y Solución de Problemas / Nivel: Táctico

-- AST1.1
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (85, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'AST1.1', 1, 2, 6, 2),
    (86, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'AST1.1', 2, 2, 6, 2),
    (87, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'AST1.1', 3, 2, 6, 2),
    (88, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'AST1.1', 4, 2, 6, 2);

-- AST1.2
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (89, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'AST1.2', 1, 2, 6, 2),
    (90, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'AST1.2', 2, 2, 6, 2),
    (91, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'AST1.2', 3, 2, 6, 2),
    (92, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'AST1.2', 4, 2, 6, 2);

-- AST1.3
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (93, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'AST1.3', 1, 2, 6, 2),
    (94, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'AST1.3', 2, 2, 6, 2),
    (95, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'AST1.3', 3, 2, 6, 2),
    (96, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'AST1.3', 4, 2, 6, 2);

-- Competencia: Análisis y Solución de Problemas / Nivel: Estratégico

-- ASE1.1
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (97, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ASE1.1', 1, 2, 6, 3),
    (98, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ASE1.1', 2, 2, 6, 3),
    (99, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ASE1.1', 3, 2, 6, 3),
    (100, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ASE1.1', 4, 2, 6, 3);

-- ASE1.2
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (101, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ASE1.2', 1, 2, 6, 3),
    (102, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ASE1.2', 2, 2, 6, 3),
    (103, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ASE1.2', 3, 2, 6, 3),
    (104, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ASE1.2', 4, 2, 6, 3);

-- ASE1.3
INSERT INTO DESCRIPCION_RESPUESTA 
    (ID_DESCRIPCION_RESPUESTA, TITULO, DESCRIPCION, CODIGO_EXCEL, ESCALA_ID_ESCALA, DIMENSION_ID_DIMENSION, COMPETENCIA_ID_COMPETENCIA, NIVEL_JERARQUICO_ID_NIVEL_JERARQUICO) 
VALUES 
    (105, 'No Logra lo Esperado', 'No cumple con los comportamientos y resultados mínimos definidos para la competencia.', 'ASE1.3', 1, 2, 6, 3),
    (106, 'Logra Parcialmente lo Esperado', 'Cumple solo en forma incompleta o inconsistente con los comportamientos y resultados definidos para la competencia.', 'ASE1.3', 2, 2, 6, 3),
    (107, 'Logra lo Esperado', 'Cumple de manera consistente con los comportamientos y resultados definidos para la competencia.', 'ASE1.3', 3, 2, 6, 3),
    (108, 'Supera lo Esperado', 'Supera de forma sostenida los comportamientos y resultados definidos para la competencia, agregando valor más allá de lo requerido.', 'ASE1.3', 4, 2, 6, 3);
