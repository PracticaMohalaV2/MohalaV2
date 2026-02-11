-- =========================
-- Poblamiento de tabla Dimension
-- =========================
INSERT INTO DIMENSION (id_dimension, nombre_dimension)
VALUES 
(1, 'Organizacionales'),
(2, 'Funcionales');

-- =========================
-- Poblamiento de tabla Departamento
-- =========================
INSERT INTO DEPARTAMENTO (id_departamento, nombre_departamento)
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
INSERT INTO NIVEL_JERARQUICO (id_nivel_jerarquico, nombre_nivel_jerarquico)
VALUES 
(1, 'Operativo'),
(2, 'Táctico'),
(3, 'Estratégico');

-- =========================
-- Poblamiento de tabla Cargo
-- =========================

-- Cargos Operativos (Nivel 1)
INSERT INTO CARGO (id_cargo, nombre_cargo, nivel_jerarquico_id_nivel_jerarquico) VALUES
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
INSERT INTO CARGO (id_cargo, nombre_cargo, nivel_jerarquico_id_nivel_jerarquico) VALUES
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
INSERT INTO CARGO (id_cargo, nombre_cargo, nivel_jerarquico_id_nivel_jerarquico) VALUES
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
INSERT INTO COMPETENCIA (id_competencia, nombre_competencia, dimension_id_dimension) VALUES
(1, 'Creatividad e Innovación', 1),
(2, 'Enfoque de Negocio', 1),
(3, 'Identificación Cultural', 1),
(4, 'Trabajo en Equipo', 1),
(5, 'Visión Global y Sistemática', 1);

-- Competencias Funcionales (Dimension 2)
INSERT INTO COMPETENCIA (id_competencia, nombre_competencia, dimension_id_dimension) VALUES
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
INSERT INTO TRABAJADOR (id_trabajador, rut, id_jefe_directo, nombre, apellido_paterno, apellido_materno, email, genero, nivel_jerarquico_id_nivel_jerarquico, cargo_id_cargo, departamento_id_departamento)
VALUES 
(1, '10.234.567-1', NULL, 'Roberto', 'Méndez', 'Castro', 'r.mendez@mohala.cl', 'Masculino', 3, 31, 1),
(2, '12.456.789-2', NULL, 'Patricia', 'Lorca', 'Vial', 'p.lorca@mohala.cl', 'Femenino', 3, 20, 2);

-- NIVEL 2: JEFATURAS (Reportan al ID 1)
INSERT INTO TRABAJADOR (id_trabajador, rut, id_jefe_directo, nombre, apellido_paterno, apellido_materno, email, genero, nivel_jerarquico_id_nivel_jerarquico, cargo_id_cargo, departamento_id_departamento)
VALUES 
(3, '11.345.678-3', 1, 'Andrés', 'Tapia', 'Ruiz', 'a.tapia@mohala.cl', 'Masculino', 2, 29, 3),
(4, '13.567.890-4', 1, 'Mónica', 'Sánchez', 'Paz', 'm.sanchez@mohala.cl', 'Femenino', 2, 22, 5);

-- NIVEL 3: ANALISTAS Y OPERATIVOS

-- Reportan a RRHH (Jefe ID: 2)
INSERT INTO TRABAJADOR (id_trabajador, rut, id_jefe_directo, nombre, apellido_paterno, apellido_materno, email, genero, nivel_jerarquico_id_nivel_jerarquico, cargo_id_cargo, departamento_id_departamento)
VALUES 
(5, '18.456.789-9', 2, 'Valeria', 'Cáceres', 'Pinto', 'v.caceres@mohala.cl', 'Femenino', 1, 8, 2),
(6, '19.567.890-0', 2, 'Sebastián', 'Marín', 'Rojas', 's.marin@mohala.cl', 'Masculino', 1, 10, 2);


-- =========================
-- Poblamiento de tabla Textos_Evaluacion
-- =========================

-- 1. CREATIVIDAD E INNOVACIÓN (ID_COMPETENCIA: 1)
-- Operativo (Nivel 1), Táctico (Nivel 2), Estratégico (Nivel 3)
INSERT INTO TEXTOS_EVALUACION (id_textos_evaluacion, codigo_excel, texto, competencia_id_competencia, nivel_jerarquico_id_nivel_jerarquico) VALUES 
(1, 'CIO1.1', 'Trabaja con mecanismos conocidos y rutinarios.', 1, 1),
(2, 'CIO1.2', 'Se mueve con facilidad en situaciones conocidas con pautas de acción prefijadas.', 1, 1),
(3, 'CIO1.3', 'Implementa ideas y soluciones que le permiten resolver situaciones rutinarias y complejas.', 1, 1),
(4, 'CIT1.1', 'Promueve un estilo de gestión innovador y de vinculación con su entorno...', 1, 2),
(5, 'CIT1.2', 'Estructura equipos de alto rendimiento, que suelen tener formatos atípicos...', 1, 2),
(6, 'CIT1.3', 'Lidera la implementación de nuevas ideas y soluciones dentro del negocio...', 1, 2),
(7, 'CIE1.1', 'Es consultado por pares y subordinados porque se le reconoce por su habilidad...', 1, 3),
(8, 'CIE1.2', 'Es intelectualmente curioso, le gusta estar informado y mantenerse en constante aprendizaje.', 1, 3),
(9, 'CIE1.3', 'Plantea mejoras o soluciones nuevas a problemas sencillos y complejos.', 1, 3);

-- 2. ENFOQUE DE NEGOCIO (ID_COMPETENCIA: 2)
INSERT INTO TEXTOS_EVALUACION (id_textos_evaluacion, codigo_excel, texto, competencia_id_competencia, nivel_jerarquico_id_nivel_jerarquico) VALUES 
(10, 'ENO2.1', 'Comprende las peculiaridades de los servicios.', 2, 1),
(11, 'ENO2.2', 'Conoce las estrategias, principios y valores corporativos.', 2, 1),
(12, 'ENO2.3', 'Invierte tiempo adicional para identificar oportunidades de crecimiento.', 2, 1),
(13, 'ENT2.1', 'Es capaz de establecer relaciones interpersonales a través del networking.', 2, 2),
(14, 'ENT2.2', 'Es hábil para adaptarse rápidamente a nuevos contextos laborales.', 2, 2),
(15, 'ENT2.3', 'Promueve la capacidad para comprender las peculiaridades de los servicios.', 2, 2),
(16, 'ENE2.1', 'Desarrolla la capacidad de adecuar productos y servicios a la estrategia.', 2, 3),
(17, 'ENE2.2', 'Referente por su capacidad de identificar y desarrollar oportunidades de negocio.', 2, 3),
(18, 'ENE2.3', 'Reconocido por su expertise, alto conocimiento cultural y estrategias.', 2, 3);

-- 6. ANÁLISIS Y SOLUCIÓN DE PROBLEMAS (ID_COMPETENCIA: 6) 
INSERT INTO TEXTOS_EVALUACION (id_textos_evaluacion, codigo_excel, texto, competencia_id_competencia, nivel_jerarquico_id_nivel_jerarquico) VALUES 
(19, 'ASO1.1', 'Resuelve problemas rutinarios de forma efectiva.', 6, 1),
(20, 'ASO1.2', 'Acude a sus superiores o pares para crear alternativas.', 6, 1),
(21, 'ASO1.3', 'Logra detectar las variables que influyen en el problema de forma oportuna.', 6, 1),
(22, 'AST1.1', 'Utiliza eficazmente datos históricos y actuales para prever tendencias.', 6, 2),
(23, 'AST1.2', 'Analiza las relaciones entre las distintas partes y causales de un problema.', 6, 2),
(24, 'AST1.3', 'Aporta soluciones validas para la situación en tiempo y forma.', 6, 2),
(25, 'ASE1.1', 'Realiza análisis complejos utilizando hipótesis y diferentes escenarios.', 6, 3),
(26, 'ASE1.2', 'Comprende problemas complejos y los define en torno a principios estratégicos.', 6, 3),
(27, 'ASE1.3', 'Se anticipa a las situaciones, previendo respuestas adecuadas y rentables.', 6, 3);