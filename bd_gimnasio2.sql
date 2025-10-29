-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-10-2025 a las 17:39:52
-- Versión del servidor: 9.0.1
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bd_gimnasio2`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `acceso`
--

CREATE TABLE `acceso` (
  `id_acceso` int NOT NULL,
  `fecha_inicio` datetime NOT NULL,
  `fecha_fin` datetime DEFAULT NULL,
  `duracion` time NOT NULL DEFAULT '00:00:00',
  `tipo_acceso` varchar(20) DEFAULT NULL,
  `id_usuario` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `acceso`
--

INSERT INTO `acceso` (`id_acceso`, `fecha_inicio`, `fecha_fin`, `duracion`, `tipo_acceso`, `id_usuario`) VALUES
(89, '2025-09-05 09:29:04', '2025-09-05 09:33:18', '00:00:00', 'Inactive', 4),
(90, '2025-09-05 09:37:40', '2025-09-05 09:39:26', '00:01:46', 'Inactive', 2),
(91, '2025-09-05 09:41:49', '2025-09-12 18:23:42', '176:41:53', 'Inactive', 19),
(92, '2025-09-05 09:42:10', NULL, '00:00:00', 'Active', 9),
(93, '2025-09-12 16:09:34', '2025-09-12 17:18:10', '01:08:36', 'Inactive', 4),
(94, '2025-09-12 16:38:11', NULL, '00:00:00', 'Active', 34),
(95, '2025-09-12 18:24:18', NULL, '00:00:00', 'Active', 4);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `acceso_con_duracion`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `acceso_con_duracion` (
`id_acceso` int
,`id_usuario` int
,`tipo_acceso` varchar(20)
,`fecha_inicio` datetime
,`fecha_fin` datetime
,`duracion` time
);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignacion_rutina`
--

CREATE TABLE `asignacion_rutina` (
  `id_asignacion` int NOT NULL,
  `id_rutina` int NOT NULL,
  `id_cliente` int NOT NULL,
  `id_dia` int NOT NULL,
  `id_estado_rutina` int NOT NULL,
  `fecha_asignacion` date NOT NULL,
  `id_entrenador` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `asignacion_rutina`
--

INSERT INTO `asignacion_rutina` (`id_asignacion`, `id_rutina`, `id_cliente`, `id_dia`, `id_estado_rutina`, `fecha_asignacion`, `id_entrenador`) VALUES
(33, 4, 9, 2, 1, '2025-09-29', 19),
(34, 3, 9, 3, 1, '2025-09-29', 19),
(35, 4, 9, 3, 1, '2025-09-29', 19),
(36, 3, 9, 1, 1, '2025-09-29', 19),
(37, 1, 9, 4, 1, '2025-09-30', 19),
(38, 4, 9, 4, 1, '2025-09-30', 19),
(39, 5, 9, 4, 1, '2025-09-30', 19),
(40, 6, 9, 4, 1, '2025-09-30', 19),
(41, 7, 9, 4, 1, '2025-09-30', 19),
(42, 17, 9, 5, 1, '2025-09-30', 19),
(43, 18, 9, 5, 1, '2025-09-30', 19),
(44, 19, 9, 5, 1, '2025-09-30', 19),
(45, 20, 9, 5, 1, '2025-09-30', 19),
(46, 21, 9, 5, 1, '2025-09-30', 19),
(47, 2, 9, 6, 1, '2025-09-30', 19),
(48, 3, 9, 6, 1, '2025-09-30', 19),
(49, 4, 9, 6, 1, '2025-09-30', 19),
(50, 5, 9, 6, 1, '2025-09-30', 19);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clase`
--

CREATE TABLE `clase` (
  `id_clase` int NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `hora` time NOT NULL,
  `duracion` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `clase`
--

INSERT INTO `clase` (`id_clase`, `nombre`, `fecha_inicio`, `hora`, `duracion`) VALUES
(3, 'Cross', '2025-10-01', '22:00:00', 2),
(6, 'Rumba', '2025-10-01', '22:00:00', 2),
(7, 'Stretching', '2025-10-25', '08:00:00', 2),
(8, 'Step', '2025-10-17', '10:00:00', 2),
(9, 'Pilates', '2025-10-17', '20:00:00', 2),
(10, 'BodyPum', '2025-11-01', '10:00:00', 2),
(11, 'BodyCombat', '2025-11-23', '22:00:00', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente_entrenador`
--

CREATE TABLE `cliente_entrenador` (
  `id_cliente` int NOT NULL,
  `id_entrenador` int NOT NULL,
  `fecha_asignacion` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `cliente_entrenador`
--

INSERT INTO `cliente_entrenador` (`id_cliente`, `id_entrenador`, `fecha_asignacion`) VALUES
(4, 34, '2025-09-12 16:38:16'),
(9, 19, '2025-09-12 16:03:54');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dia_semana`
--

CREATE TABLE `dia_semana` (
  `id_dia` int NOT NULL,
  `nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `dia_semana`
--

INSERT INTO `dia_semana` (`id_dia`, `nombre`) VALUES
(1, 'Lunes'),
(2, 'Martes'),
(3, 'Miércoles'),
(4, 'Jueves'),
(5, 'Viernes'),
(6, 'Sábado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ejercicio_rutina`
--

CREATE TABLE `ejercicio_rutina` (
  `id_ejercicio_rutina` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id_usuario_entrenador` int DEFAULT NULL,
  `id_dia` int DEFAULT NULL,
  `id_zona_cuerpo` int DEFAULT NULL,
  `id_maquina` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `ejercicio_rutina`
--

INSERT INTO `ejercicio_rutina` (`id_ejercicio_rutina`, `nombre`, `descripcion`, `id_usuario_entrenador`, `id_dia`, `id_zona_cuerpo`, `id_maquina`) VALUES
(1, 'Calentamiento: 10 minutos.', 'Inclínate hacia delante desde tus caderas y sostén las asas. Manteniendo la espalda recta, estira las piernas con fuerza. Mientras las estiras, inclínate ligeramente hacia atrás extendiendo las caderas. Lleva las asas hacia tu pecho.', 19, 1, 1, 3),
(2, 'Press de banca (10x3)', 'Siéntate en la punta del banco de espaldas a la barra y túmbate de forma que la barra quede por detrás de tu cabeza. Sujeta la barra con las manos, retrae las escápulas y deslízate por el banco hasta que la barra quede justo a la altura de tus ojos.', NULL, NULL, NULL, NULL),
(3, 'Remo con barra (10x3)', 'Agarra con ambas manos la barra y con las muñecas rectas y bloqueadas, empieza a llevarla hacia el pecho, abriendo ligeramente los codos al final para llegar lo más cerca posible.', NULL, NULL, NULL, NULL),
(4, 'Press militar con mancuernas(10x3)', 'Extiende los brazos para empujar las mancuernas hacia arriba hasta que los codos estén extendidos pero no bloqueados. Baja lentamente el peso hasta que sus manos estén justo por encima de los hombros. Asegúrate de no arquear la espalda cuando realices el ejercicio.', NULL, NULL, NULL, NULL),
(5, 'Curl de bíceps (10x3)', 'Sube ambos brazos flexionándolos hasta que las manos lleguen casi a la altura de los hombros. Mantén esta posición un par de segundos y vuelve a bajar los brazos desflexionándolos. Intenta permanecer con la espalda erguida, los hombros relajados y realizando el movimiento lentamente.', NULL, NULL, NULL, NULL),
(6, 'Tríceps en polea (10x3)', 'Asegúrate de que los codos están ubicados cómodamente cerca de tus laterales. Presiona la barra suavemente hacia abajo hasta que los brazos estén extendidos completamente. Luego, regresa lentamente a la posición inicial. ', NULL, NULL, NULL, NULL),
(7, 'Plancha (3 series de 30 segundos).', 'Túmbate bocabajo en una posición de tabla, apoyándote sobre los antebrazos y la punta de los pies.\r\nAlínea hombros, cadera, rodillas y tobillos para mantener la espalda recta.\r\nActiva el abdomen metiendo el ombligo hacia adentro y contrae glúteos y piernas.\r\nLos codos deben presionar contra el suelo haciendo que la espalda se eleve ligeramente', NULL, NULL, NULL, NULL),
(8, 'Elevación de piernas (15x3)', 'Siéntate en el banco abdominal vertical con la espalda bien apoyada y agarra las asas o barras laterales para estabilizarte.\r\nLevanta las piernas estiradas hacia arriba utilizando la fuerza de tus abdominales inferiores, asegurándote de no balancearte para mantener el control del movimiento.', NULL, NULL, NULL, NULL),
(9, 'Sentadillas con barra (4x10)', 'Separa levemente tus piernas, asegurándote que están al mismo nivel que tus hombros.\r\nLa planta de los pies debe estar unos 30 grados hacia afuera.\r\nEn esta posición, baja tu cuerpo como si estuvieras sentado en una silla.\r\n¡Importante! Vigila que las rodillas no sobresalgan más que la punta de los pies, ya que podrías lesionarte.', NULL, NULL, NULL, NULL),
(10, 'Prensa de piernas (10x4)', 'Coloca los pies en la plataforma de la máquina, asegurándote de que estén al ancho de los hombros y bien posicionados antes de comenzar el movimiento.\r\nDesciende la plataforma hacia abajo flexionando las rodillas y las caderas hasta que tus muslos estén paralelos al suelo.\r\nEmpuja la plataforma hacia arriba extendiendo las piernas completamente sin bloquear las rodillas.\r\n\r\n', NULL, NULL, NULL, NULL),
(11, 'Peso muerto con barra (10x4)', 'Colócate de pie con los pies separados a la anchura de los hombros y la barra frente a ti en el suelo.\r\nAgáchate y agarra la barra con las manos separadas a una distancia ligeramente mayor que la anchura de los hombros.\r\nMantén la espalda recta, el pecho hacia fuera y los hombros hacia atrás mientras levantas la barra, empujando con las piernas y extendiendo las caderas.', NULL, NULL, NULL, NULL),
(12, 'Elevación de talones (10x4)', 'Colócate en la máquina de gemelos con las hombreras sobre tus hombros.\r\nAjusta la posición de tus pies de modo que las puntas estén en el escalón y los tobillos en flexión pasiva.\r\nEleva los talones mientras inhalas, extendiendo completamente los tobillos.\r\nBaja lentamente los talones de vuelta a la posición inicial mientras exhalas.', NULL, NULL, NULL, NULL),
(13, 'Caminadora 30 minutos', 'Camina a una velocidad moderada durante 12 minutos.\r\nIntensifica el ritmo: Aumenta la inclinación de la caminadora al 12% y camina a una velocidad de 3 millas por hora (aproximadamente 4.8 km/h) durante 3 minutos.\r\nRepite el ciclo: Alterna entre 12 minutos de caminata moderada y 3 minutos de mayor intensidad durante 30 minutos en total', NULL, NULL, NULL, NULL),
(14, 'Remo con mancuernas', 'Agarra una mancuerna con una mano mientras te apoyas en una superficie estable con la rodilla y la mano opuesta para mantener el equilibrio.\r\nCon la espalda recta, lleva la mancuerna hacia arriba hacia tu torso, manteniendo el codo cerca del cuerpo y contrayendo la espalda baja y media.', NULL, NULL, NULL, NULL),
(15, 'Zancadas con peso (12x3 por pierna)', 'Colócate debajo de la barra guiada y coloca los hombros bajo los soportes.\r\nDa un paso hacia adelante con una pierna y flexiona ambas rodillas hasta que la pierna adelantada forme un ángulo de 90 grados.\r\nEmpuja con la pierna adelantada para volver a la posición inicial.', NULL, NULL, NULL, NULL),
(16, 'Burpess', 'Comienza en posición de pie, agáchate y lleva tus manos al suelo, luego salta hacia atrás para quedar en posición de plancha, realiza una flexión, vuelve a saltar hacia adelante y termina con un salto explosivo hacia arriba.', NULL, NULL, NULL, NULL),
(17, 'Thrusters', 'Combina una sentadilla frontal con un press de hombros. Con una barra a la altura de los hombros, baja en una sentadilla profunda y, al levantarte, empuja el peso por encima de la cabeza en un movimiento fluido.', NULL, NULL, NULL, NULL),
(18, 'Sentadillas Búlgaras', 'Con un pie apoyado en un banco o plataforma detrás de ti y el otro pie adelante en el suelo, baja hasta que la rodilla de la pierna delantera forme un ángulo de 90 grados y luego vuelve a subir.', NULL, NULL, NULL, NULL),
(19, 'Hip Thrust', 'Acuéstate con la espalda sobre un banco y los pies en el suelo. Coloca una barra sobre las caderas, empuja las caderas hacia arriba apretando los glúteos al final del movimiento, y baja de manera controlada.', NULL, NULL, NULL, NULL),
(20, 'Step-ups', 'Con una pierna sube a un banco o plataforma, mantén el control y vuelve a bajar de manera alternada. Puedes añadir peso utilizando mancuernas.', NULL, NULL, NULL, NULL),
(21, 'Sentadilla con salto', 'Realiza una sentadilla regular y, al subir, haz un salto explosivo. Aterriza suavemente y baja directamente a la siguiente sentadilla.', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_membresia`
--

CREATE TABLE `estado_membresia` (
  `id_estado_membresia` int NOT NULL,
  `nombre` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `estado_membresia`
--

INSERT INTO `estado_membresia` (`id_estado_membresia`, `nombre`) VALUES
(1, 'Activa'),
(2, 'Congelada'),
(3, 'Suspendida'),
(4, 'Expirada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_revision`
--

CREATE TABLE `estado_revision` (
  `id_estado_revision` int NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `estado_revision`
--

INSERT INTO `estado_revision` (`id_estado_revision`, `nombre`) VALUES
(1, 'Recibida'),
(2, 'En proceso'),
(3, 'Cancelada'),
(4, 'Finalizada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado_rutina`
--

CREATE TABLE `estado_rutina` (
  `id_estado_rutina` int NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `estado_rutina`
--

INSERT INTO `estado_rutina` (`id_estado_rutina`, `nombre`) VALUES
(1, 'Active'),
(2, 'Inactive');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `genero`
--

CREATE TABLE `genero` (
  `id_genero` int NOT NULL,
  `tipo` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `genero`
--

INSERT INTO `genero` (`id_genero`, `tipo`) VALUES
(1, 'Masculino'),
(2, 'Femenino'),
(3, 'Cisgénero'),
(5, 'Transgénero'),
(6, 'No binario'),
(7, 'Genderqueer'),
(8, 'Intersexual'),
(9, 'Género fluido'),
(10, 'Agénero'),
(11, 'Género no conforme'),
(12, 'Bigénero'),
(13, 'Omnigénero'),
(14, 'Prefiero no decir');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario`
--

CREATE TABLE `horario` (
  `id_horario` int NOT NULL,
  `nombre` varchar(15) NOT NULL,
  `descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `horario`
--

INSERT INTO `horario` (`id_horario`, `nombre`, `descripcion`) VALUES
(1, 'Turno 1', 'Lunes-Viernes (Mañana 5am - 2pm)\r\nSábado (7am -11am)'),
(2, 'Turno 2', 'Lunes-Viernes (Tarde 2pm - 11pm)\r\nSábados (2pm - 5pm)'),
(3, 'Turno 3', 'Miércoles-Viernes (Mañana 5am - 2pm),Sábado (7am -7pm), Domingo (7am -4pm)\r\n'),
(4, 'Turno 4', 'Miercoles-Viernes (Tarde 5am - 2pm),Sábado (7am -7pm), Domingo (7am -4pm)\r\n'),
(5, 'Turno 4', 'Lunes-Viernes (Mañana 8am - 6pm)\r\nSábado (7am -11am)');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario_entrenador`
--

CREATE TABLE `horario_entrenador` (
  `id_horario_entrenador` int NOT NULL,
  `id_usuario` int NOT NULL,
  `id_horario` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `horario_entrenador`
--

INSERT INTO `horario_entrenador` (`id_horario_entrenador`, `id_usuario`, `id_horario`) VALUES
(1, 2, 1),
(2, 19, 1),
(3, 28, 3),
(4, 34, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario_maquina`
--

CREATE TABLE `inventario_maquina` (
  `id_inventario_maquina` int NOT NULL,
  `fecha_compra` date NOT NULL,
  `precio` int NOT NULL,
  `serial` varchar(20) NOT NULL,
  `id_proveedor` int NOT NULL,
  `id_maquina` int NOT NULL,
  `disponibilidad` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `inventario_maquina`
--

INSERT INTO `inventario_maquina` (`id_inventario_maquina`, `fecha_compra`, `precio`, `serial`, `id_proveedor`, `id_maquina`, `disponibilidad`) VALUES
(1, '2023-07-01', 2000000, 'N00156478S023', 2, 1, 1),
(2, '2025-03-01', 3000000, 'N45P56', 1, 2, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `maquina`
--

CREATE TABLE `maquina` (
  `id_maquina` int NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `maquina`
--

INSERT INTO `maquina` (`id_maquina`, `nombre`) VALUES
(1, 'Caminadora'),
(2, 'Escalera1'),
(3, 'Banco de musculacion'),
(4, 'Dorsalera'),
(5, 'Bici eliptica'),
(6, 'Prensa inclinada'),
(7, 'Press Banca'),
(8, 'Bicicleta vertical'),
(9, 'Remo'),
(10, 'Polea'),
(11, 'Banco de abdominale'),
(12, 'Jaula'),
(13, 'Extension de cuadriceps'),
(14, 'Curl Femoral Sentado'),
(15, 'Elevacion de gemelos'),
(16, 'Barra'),
(17, 'Mancuernas'),
(18, 'Inducción'),
(19, 'Abducción'),
(20, 'Máquina de gemelos'),
(21, 'Banco');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `membresia`
--

CREATE TABLE `membresia` (
  `id_membresia` int NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `costo` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `membresia`
--

INSERT INTO `membresia` (`id_membresia`, `tipo`, `costo`) VALUES
(1, 'Semanal', 17500),
(2, 'Mensual', 70000),
(3, 'Anual', 1500000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `membresia_usuario`
--

CREATE TABLE `membresia_usuario` (
  `id_membresia_usuario` int NOT NULL,
  `id_usuario` int NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `id_membresia` int NOT NULL,
  `id_estado_membresia` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `membresia_usuario`
--

INSERT INTO `membresia_usuario` (`id_membresia_usuario`, `id_usuario`, `fecha_inicio`, `fecha_fin`, `id_membresia`, `id_estado_membresia`) VALUES
(1, 15, '2025-08-14', '2025-09-14', 2, 1),
(5, 3, '2024-10-09', '2024-10-16', 1, 1),
(6, 4, '2025-09-03', '2025-09-10', 1, 1),
(9, 8, '2025-08-12', '2026-08-12', 3, 2),
(10, 33, '2025-09-05', '2025-10-05', 1, 1),
(28, 9, '2025-09-05', '2025-10-05', 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `nomina`
--

CREATE TABLE `nomina` (
  `id_nomina` int NOT NULL,
  `id_usuario` int DEFAULT NULL,
  `fecha_generacion` date DEFAULT NULL,
  `salario_base` int DEFAULT NULL,
  `auxilio_transporte` int DEFAULT NULL,
  `aporte_salud` int DEFAULT NULL,
  `aporte_pension` int DEFAULT NULL,
  `total_devengado` int DEFAULT NULL,
  `total_deducciones` int DEFAULT NULL,
  `liquido_a_recibir` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `nomina`
--

INSERT INTO `nomina` (`id_nomina`, `id_usuario`, `fecha_generacion`, `salario_base`, `auxilio_transporte`, `aporte_salud`, `aporte_pension`, `total_devengado`, `total_deducciones`, `liquido_a_recibir`) VALUES
(4, 2, '2025-08-10', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000),
(5, 2, '2025-08-10', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000),
(6, 19, '2025-08-09', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(7, 20, '2025-08-09', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(8, 22, '2025-08-09', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(9, 24, '2025-08-09', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(10, 24, '2025-08-09', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(11, 20, '2025-08-09', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(12, 20, '2025-08-09', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(13, 23, '2025-08-09', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(14, 2, '2025-08-09', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000),
(15, 19, '2025-08-17', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(16, 22, '2025-08-10', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(17, 2, '2025-08-17', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000),
(18, 19, '2025-08-10', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(19, 2, '2025-08-13', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000),
(20, 22, '2025-08-23', 1800000, 75000, 6000, 40000, 2400000, 1200000, 1700000),
(21, 24, '2025-08-21', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(22, 2, '2025-08-31', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000),
(23, 23, '2025-08-30', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(24, 20, '2025-08-14', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(25, 2, '2025-08-17', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000),
(26, 24, '2025-08-29', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(27, 2, '2025-08-30', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000),
(28, 24, '2025-08-21', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(29, 2, '2025-08-12', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000),
(30, 2, '2025-08-15', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000),
(31, 20, '2025-08-30', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(32, 23, '2025-08-13', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(33, 23, '2025-08-13', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(34, 24, '2025-08-15', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(35, 23, '2025-08-23', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(36, 22, '2025-08-14', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(37, 20, '2025-08-24', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(38, 19, '2025-08-23', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(39, 2, '2025-08-23', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000),
(42, 23, '2025-08-21', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(43, 20, '2025-08-24', 1300000, 65000, 52000, 52000, 1365000, 104000, 1261000),
(44, 19, '2025-08-11', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(45, 19, '2025-08-13', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(46, 19, '2025-08-14', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(47, 19, '2025-08-14', 2900000, 145000, 116000, 116000, 3045000, 232000, 2813000),
(48, 2, '2025-08-29', 3500000, 175000, 140000, 140000, 3675000, 280000, 3395000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `observacion_revision`
--

CREATE TABLE `observacion_revision` (
  `id_obs_revision` int NOT NULL,
  `id_revision` int NOT NULL,
  `id_usuario` int NOT NULL,
  `observacion_admin` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `observacion_tecnico` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `observacion_revision`
--

INSERT INTO `observacion_revision` (`id_obs_revision`, `id_revision`, `id_usuario`, `observacion_admin`, `observacion_tecnico`, `fecha`) VALUES
(1, 13, 2, 'falla de cable de poder', 'Se reemplaza el cable de poder por uno nuevo', '2025-08-28 16:27:09'),
(2, 14, 2, 'falla en encendido de la maquina', 'CAMBIO DE CABLE DE PODER ', '2025-08-28 15:52:43'),
(3, 15, 2, 'falla en la revision', 'se realiza la respectiva revisión y mantenimiento de la maquina', '2025-08-28 15:55:43'),
(7, 16, 2, 'La maquina no prende', NULL, '2025-08-29 10:16:06');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `plan_trabajo`
--

CREATE TABLE `plan_trabajo` (
  `id_plan_trabajo` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `plan_trabajo`
--

INSERT INTO `plan_trabajo` (`id_plan_trabajo`, `nombre`, `descripcion`) VALUES
(1, 'Aumento de masa muscular', 'Mejorar la definición muscular y resistencia'),
(2, 'Pérdida de peso', 'Reducir grasa corporal y mejorar la condición cardiovascular.'),
(3, 'Resistencia muscular y cardiovascular', 'Mejorar la resistencia física y cardiovascular.'),
(4, 'CrossFit', 'Mejorar la fuerza, resistencia y agilidad mediante entrenamientos funcionales de alta intensidad.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `progreso_trabajo`
--

CREATE TABLE `progreso_trabajo` (
  `id_progreso_trabajo` int NOT NULL,
  `peso` int NOT NULL,
  `descripcion` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `fecha` datetime NOT NULL,
  `id_usuario_miembro` int NOT NULL,
  `id_usuario_entrenador` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `progreso_trabajo`
--

INSERT INTO `progreso_trabajo` (`id_progreso_trabajo`, `peso`, `descripcion`, `fecha`, `id_usuario_miembro`, `id_usuario_entrenador`) VALUES
(3, 60, 'aumento de masa', '2025-08-13 11:06:28', 15, 22),
(4, 54, 'Inicio de entrenamiento diario con peso inicial de 20kg para los ejercicios en general', '2025-08-13 11:07:27', 4, 22),
(5, 60, 'Avance de tiempo en cardio escalera con aumento de 5 minutos', '2025-08-14 08:25:10', 8, 23),
(6, 80, 'Excelente rendimiento, enfoque y constancia por parte del usuario.', '2025-08-27 11:52:07', 9, 19),
(7, 60, 'aumento de levantamiento de pesas a 20 kg en brazo', '2025-08-29 10:01:23', 8, 23);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `id_proveedor` int NOT NULL,
  `nombre` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`id_proveedor`, `nombre`) VALUES
(1, 'Industrias Fitness'),
(2, 'Gym Company'),
(3, 'MoviFit'),
(4, 'SportFitness'),
(5, 'FitnessMarket'),
(6, 'Gym Home'),
(11, 'Decatlhon');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reserva_clase`
--

CREATE TABLE `reserva_clase` (
  `id_reserva_clase` int NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `id_clase` int NOT NULL,
  `id_membresia_usuario` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `reserva_clase`
--

INSERT INTO `reserva_clase` (`id_reserva_clase`, `fecha`, `hora`, `id_clase`, `id_membresia_usuario`) VALUES
(20, '2025-09-01', '22:00:00', 6, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reserva_maquina`
--

CREATE TABLE `reserva_maquina` (
  `id_reserva` int NOT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `id_membresia_usuario` int NOT NULL,
  `id_inventario_maquina` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `reserva_maquina`
--

INSERT INTO `reserva_maquina` (`id_reserva`, `fecha`, `hora_inicio`, `hora_fin`, `id_membresia_usuario`, `id_inventario_maquina`) VALUES
(1, '2024-11-18', '18:00:00', '18:15:00', 6, 1),
(2, '2024-11-02', '11:00:00', '11:15:00', 6, 1),
(3, '2025-05-01', '20:15:17', '20:30:17', 6, 1),
(4, '2025-06-22', '15:20:45', '15:35:45', 6, 1),
(5, '2025-06-22', '18:00:47', '18:20:47', 6, 2),
(6, '2025-06-22', '20:00:33', '20:15:33', 9, 2),
(7, '2025-06-25', '16:30:57', '16:45:57', 9, 2),
(8, '2025-06-25', '17:00:04', '17:15:04', 6, 2),
(12, '2025-06-25', '18:45:00', '19:00:00', 6, 2),
(13, '2025-06-26', '10:45:00', '11:00:00', 6, 1),
(14, '2025-06-26', '11:00:00', '11:15:00', 6, 1),
(15, '2025-06-26', '11:15:00', '11:30:00', 6, 1),
(16, '2025-06-26', '10:00:00', '10:15:00', 6, 2),
(17, '2025-06-26', '18:00:00', '18:15:00', 6, 1),
(18, '2025-06-26', '12:00:00', '12:15:00', 6, 1),
(19, '2025-06-26', '13:00:00', '13:15:00', 6, 1),
(20, '2025-06-26', '18:45:00', '19:00:00', 6, 1),
(21, '2025-06-26', '15:30:00', '15:45:00', 6, 1),
(22, '2025-06-26', '16:45:00', '17:00:00', 6, 1),
(23, '2025-06-26', '14:15:00', '14:30:00', 6, 1),
(24, '2025-06-26', '14:45:00', '15:00:00', 6, 1),
(25, '2025-06-26', '17:30:00', '17:45:00', 6, 1),
(26, '2025-06-26', '16:00:00', '16:15:00', 6, 1),
(27, '2025-06-26', '06:15:00', '06:30:00', 6, 1),
(28, '2025-06-26', '12:30:00', '12:45:00', 6, 1),
(29, '2025-06-26', '19:45:00', '20:00:00', 6, 1),
(30, '2025-06-26', '06:45:00', '07:00:00', 6, 1),
(31, '2025-06-26', '13:30:00', '13:45:00', 6, 1),
(32, '2025-06-26', '20:45:00', '21:00:00', 6, 1),
(33, '2025-06-26', '09:15:00', '09:30:00', 6, 2),
(34, '2025-06-26', '08:30:00', '08:45:00', 6, 1),
(35, '2025-06-26', '21:30:00', '21:45:00', 6, 1),
(36, '2025-06-26', '08:30:00', '08:45:00', 6, 2),
(37, '2025-06-26', '08:00:00', '08:15:00', 6, 2),
(38, '2025-06-26', '07:30:00', '07:45:00', 6, 2),
(39, '2025-06-26', '09:15:00', '09:30:00', 6, 1),
(40, '2025-06-26', '19:15:00', '19:30:00', 6, 1),
(41, '2025-06-26', '20:15:00', '20:30:00', 6, 1),
(42, '2025-06-27', '14:30:00', '14:45:00', 6, 1),
(43, '2025-06-27', '12:45:00', '13:00:00', 6, 2),
(44, '2025-07-02', '12:15:00', '12:30:00', 6, 1),
(45, '2025-07-02', '12:15:00', '12:30:00', 6, 2),
(47, '2025-08-11', '07:00:00', '07:15:00', 6, 1),
(48, '2025-08-12', '13:30:00', '13:45:00', 6, 1),
(49, '2025-08-12', '16:45:00', '17:00:00', 6, 1),
(50, '2025-08-13', '11:45:00', '12:00:00', 6, 1),
(51, '2025-08-29', '12:30:00', '12:45:00', 6, 1),
(52, '2025-08-29', '15:15:00', '15:30:00', 6, 1),
(53, '2025-09-01', '11:00:00', '11:15:00', 6, 1),
(54, '2025-09-01', '12:30:00', '12:45:00', 6, 1),
(57, '2025-09-05', '21:00:00', '21:15:00', 6, 1),
(60, '2025-09-06', '18:15:00', '18:30:00', 6, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `revision`
--

CREATE TABLE `revision` (
  `id_revision` int NOT NULL,
  `fecha_revision` datetime NOT NULL,
  `id_inventario_maquina` int NOT NULL,
  `id_estado_revision` int NOT NULL,
  `id_usuario` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `revision`
--

INSERT INTO `revision` (`id_revision`, `fecha_revision`, `id_inventario_maquina`, `id_estado_revision`, `id_usuario`) VALUES
(1, '2025-08-14 00:00:00', 1, 2, 3),
(13, '2025-08-25 15:42:53', 2, 4, 2),
(14, '2025-08-25 16:28:40', 2, 2, 2),
(15, '2025-08-25 16:45:47', 2, 4, 2),
(16, '2025-08-29 10:16:06', 2, 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id_rol` int NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `salario` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id_rol`, `nombre`, `salario`) VALUES
(1, 'Administrador', 3500000),
(2, 'Entrenador', 2900000),
(5, 'Miembro', NULL),
(6, 'Recepcionista', 1300000),
(7, 'Servicios generales', 1300000),
(8, 'Tecnico', 1800000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rutina`
--

CREATE TABLE `rutina` (
  `id_rutina` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(400) DEFAULT NULL,
  `id_plan_trabajo` int NOT NULL,
  `id_usuario_entrenador` int NOT NULL,
  `fecha_asignacion` date DEFAULT NULL,
  `id_estado_rutina` int DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `rutina`
--

INSERT INTO `rutina` (`id_rutina`, `nombre`, `descripcion`, `id_plan_trabajo`, `id_usuario_entrenador`, `fecha_asignacion`, `id_estado_rutina`) VALUES
(1, 'Rutina de Pecho Básica', 'Press banca, aperturas con mancuernas, flexiones.', 1, 19, '2025-09-29', 1),
(2, 'Rutina de Piernas Intermedia', 'Sentadillas, prensa, zancadas, peso muerto rumano.', 1, 19, '2025-09-29', 1),
(3, 'Rutina de Espalda Avanzada', 'Dominadas, remo con barra, jalón al pecho.', 1, 19, '2025-09-29', 1),
(4, 'Rutina de Abdomen', 'Crunch, elevación de piernas, planchas.', 1, 19, '2025-09-29', 1),
(5, 'Rutina Full Body', 'Circuito general: sentadillas, flexiones, remo, abdominales.', 1, 19, '2025-09-29', 1),
(6, 'Rutina Cliente 9', 'Plan personalizado', 1, 19, '2025-09-29', 1),
(7, 'Rutina Cliente 9', 'Plan personalizado', 1, 19, '2025-09-29', 1),
(8, 'Rutina Cliente 9', 'Plan personalizado', 1, 19, '2025-09-29', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rutina_ejercicio`
--

CREATE TABLE `rutina_ejercicio` (
  `id_rutina_ejercicio` int NOT NULL,
  `id_rutina` int NOT NULL,
  `id_ejercicio_rutina` int NOT NULL,
  `id_dia` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `rutina_ejercicio`
--

INSERT INTO `rutina_ejercicio` (`id_rutina_ejercicio`, `id_rutina`, `id_ejercicio_rutina`, `id_dia`) VALUES
(7, 4, 1, 1),
(8, 3, 5, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `supervision`
--

CREATE TABLE `supervision` (
  `id_supervision` int NOT NULL,
  `id_acceso_miembro` int NOT NULL,
  `id_acceso_entrenador` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL,
  `identificacion` int NOT NULL,
  `nombre` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `apellido` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `edad` int NOT NULL,
  `correo` varchar(50) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `id_genero` int NOT NULL,
  `id_plan_trabajo` int DEFAULT NULL,
  `id_rol` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `identificacion`, `nombre`, `apellido`, `edad`, `correo`, `telefono`, `contrasena`, `id_genero`, `id_plan_trabajo`, `id_rol`) VALUES
(2, 12345, 'david', 'sanchez', 30, 'david@gmail.com', '3144912788', 'scrypt:32768:8:1$muewGj4arh7hJUiU$c9717c7316514ff390bd1eda09c301856337592f6280605672978c0d7d23e5fcffa16d18537b30a0b93526b41cf5b0fe893b340666fdee09859aed70013b2463', 1, NULL, 1),
(3, 1, 'prueba', 'p', 23, 'prueba@gmail.com', '1111111111', 'prueba1', 2, 4, 5),
(4, 1054374698, 'Luz Nidian', 'Lasso Chavarro', 26, 'nidianlassocha@gmail.com', '3208237758', 'scrypt:32768:8:1$KBQY9zuAsjPtyUJZ$9cd1eea910112f7affd311e5570feeecdbc51e20ade4eb13431ca376161a939c8361be4e71b1475cf3b496b60cb99cf92a581284e713873723b88b124ad61bbd', 2, 1, 5),
(8, 1234567800, 'Felipe', 'Torres', 29, 'felipet@gmail.com', '3143102083', '000000000', 8, 3, 5),
(9, 23823670, 'Jeronimo', 'Lasso', 25, 'jlasso@gmail.com', '3203441369', 'jeronimo', 1, 2, 5),
(10, 657453, 'Juliana', 'Galán', 45, 'juliana@gmail.com', '3256785147', 'juliana', 12, 3, 5),
(15, 9876543, 'Daniel', 'Chavez', 50, 'davidf.sanchezt@gmail.com', '3123459479', 'daniel', 14, 1, 5),
(16, 101785444, 'Fernando', 'Zuñiga', 45, 'fernando@gmail.com', '3345663424', 'fernando', 1, 1, 5),
(17, 12345678, 'Ximena', 'Ortega', 19, 'ximena@gmail.com', '3212209845', 'ximena**', 2, 4, 5),
(18, 456731, 'Milena', 'Morales', 35, 'milenamorales@gmail.com', '3156732145', 'milena**', 2, 1, 5),
(19, 4286273, 'Juan Carlos', 'Vanegas', 35, 'juanvanegas@gmail.com', '3507861111', 'jvanegas*', 1, 2, 2),
(20, 1051567842, 'Irene', 'Herrera', 25, 'ireneh@gmail.com', '3003900123', 'irene1234', 2, NULL, 6),
(22, 238236701, 'Andres', 'Galindo', 25, 'andresg@gmail.com', '3019875413', 'scrypt:32768:8:1$XkafiPDPXF4vgLGs$c914361ae9580e3ac7c3edbaeb04c34ca8f2c7f73826856882e74e347547c1c97fd9e0c3d089a619d0154d65e1c1e5e69e64a23ceadfba7cb396c11969295f06', 1, 1, 2),
(23, 170718, 'Mirtha', 'Ramirez', 30, 'mramirez@gmail.com', '3149001234', 'mirtha*', 2, 3, 2),
(24, 42825345, 'Rosa', 'Santander', 45, 'rsantander@hotmail.com', '3054886721', 'rosa', 2, NULL, 7),
(25, 42800, 'final', 'final', 24, 'final@gmail.com', '3178819283', 'final', 2, 1, 5),
(26, 929, 'Jorge Andrés', 'Vargas Cortéz', 45, 'jv@gmail.com', '3115806370', 'jorge', 1, NULL, 8),
(27, 90565500, 'Luz', 'Carreiro', 37, 'luzc@gmail.com', '3190074500', 'luz2025', 2, 2, 5),
(28, 2001, 'Camilo', 'Pardo', 30, 'cp@gmail.com', '3189091701', 'camilopardo', 1, 4, 2),
(33, 1724, 'Pamela', 'Porras', 12, 'pp@gmail.com', '3125242628', 'pamela', 2, 2, 5),
(34, 509, 'Lucas', 'De la rosa', 37, 'lrosa@gmail.com', '3043022500', 'lucas', 1, 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `zona_cuerpo`
--

CREATE TABLE `zona_cuerpo` (
  `id_zona_cuerpo` int NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `zona_cuerpo`
--

INSERT INTO `zona_cuerpo` (`id_zona_cuerpo`, `nombre`) VALUES
(1, 'Pecho'),
(2, 'Espalda'),
(3, 'Hombros'),
(4, 'Brazos'),
(5, 'Piernas'),
(6, 'Glúteos'),
(7, 'Abdomen'),
(8, 'Cardio');

-- --------------------------------------------------------

--
-- Estructura para la vista `acceso_con_duracion`
--
DROP TABLE IF EXISTS `acceso_con_duracion`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `acceso_con_duracion`  AS SELECT `a`.`id_acceso` AS `id_acceso`, `a`.`id_usuario` AS `id_usuario`, `a`.`tipo_acceso` AS `tipo_acceso`, `a`.`fecha_inicio` AS `fecha_inicio`, `a`.`fecha_fin` AS `fecha_fin`, sec_to_time(timestampdiff(SECOND,`a`.`fecha_inicio`,`a`.`fecha_fin`)) AS `duracion` FROM `acceso` AS `a` ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `acceso`
--
ALTER TABLE `acceso`
  ADD PRIMARY KEY (`id_acceso`),
  ADD KEY `fk_acceso_usuario` (`id_usuario`);

--
-- Indices de la tabla `asignacion_rutina`
--
ALTER TABLE `asignacion_rutina`
  ADD PRIMARY KEY (`id_asignacion`),
  ADD KEY `id_rutina` (`id_rutina`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_dia` (`id_dia`),
  ADD KEY `id_estado_rutina` (`id_estado_rutina`),
  ADD KEY `id_entrenador` (`id_entrenador`);

--
-- Indices de la tabla `clase`
--
ALTER TABLE `clase`
  ADD PRIMARY KEY (`id_clase`);

--
-- Indices de la tabla `cliente_entrenador`
--
ALTER TABLE `cliente_entrenador`
  ADD PRIMARY KEY (`id_cliente`),
  ADD KEY `id_entrenador` (`id_entrenador`);

--
-- Indices de la tabla `dia_semana`
--
ALTER TABLE `dia_semana`
  ADD PRIMARY KEY (`id_dia`);

--
-- Indices de la tabla `ejercicio_rutina`
--
ALTER TABLE `ejercicio_rutina`
  ADD PRIMARY KEY (`id_ejercicio_rutina`),
  ADD KEY `fk_rutina_usuario_entrenador` (`id_usuario_entrenador`),
  ADD KEY `fk_ejercicio_dia` (`id_dia`),
  ADD KEY `fk_ejercicio_zona` (`id_zona_cuerpo`),
  ADD KEY `fk_ejercicio_maquina` (`id_maquina`);

--
-- Indices de la tabla `estado_membresia`
--
ALTER TABLE `estado_membresia`
  ADD PRIMARY KEY (`id_estado_membresia`);

--
-- Indices de la tabla `estado_revision`
--
ALTER TABLE `estado_revision`
  ADD PRIMARY KEY (`id_estado_revision`);

--
-- Indices de la tabla `estado_rutina`
--
ALTER TABLE `estado_rutina`
  ADD PRIMARY KEY (`id_estado_rutina`);

--
-- Indices de la tabla `genero`
--
ALTER TABLE `genero`
  ADD PRIMARY KEY (`id_genero`);

--
-- Indices de la tabla `horario`
--
ALTER TABLE `horario`
  ADD PRIMARY KEY (`id_horario`);

--
-- Indices de la tabla `horario_entrenador`
--
ALTER TABLE `horario_entrenador`
  ADD PRIMARY KEY (`id_horario_entrenador`),
  ADD KEY `fk_horario_entrenador_horario` (`id_horario`),
  ADD KEY `fk_horario_entrenador_usuario` (`id_usuario`);

--
-- Indices de la tabla `inventario_maquina`
--
ALTER TABLE `inventario_maquina`
  ADD PRIMARY KEY (`id_inventario_maquina`),
  ADD KEY `fk_inventario_proveedor` (`id_proveedor`),
  ADD KEY `fk_inventario_maquina` (`id_maquina`);

--
-- Indices de la tabla `maquina`
--
ALTER TABLE `maquina`
  ADD PRIMARY KEY (`id_maquina`);

--
-- Indices de la tabla `membresia`
--
ALTER TABLE `membresia`
  ADD PRIMARY KEY (`id_membresia`);

--
-- Indices de la tabla `membresia_usuario`
--
ALTER TABLE `membresia_usuario`
  ADD PRIMARY KEY (`id_membresia_usuario`),
  ADD KEY `fk_membresia_usuario_estado_membresia` (`id_estado_membresia`),
  ADD KEY `fk_membresia_usuario_membresia` (`id_membresia`),
  ADD KEY `fkmem_usuario` (`id_usuario`);

--
-- Indices de la tabla `nomina`
--
ALTER TABLE `nomina`
  ADD PRIMARY KEY (`id_nomina`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `observacion_revision`
--
ALTER TABLE `observacion_revision`
  ADD PRIMARY KEY (`id_obs_revision`),
  ADD KEY `id_revision` (`id_revision`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `plan_trabajo`
--
ALTER TABLE `plan_trabajo`
  ADD PRIMARY KEY (`id_plan_trabajo`);

--
-- Indices de la tabla `progreso_trabajo`
--
ALTER TABLE `progreso_trabajo`
  ADD PRIMARY KEY (`id_progreso_trabajo`),
  ADD KEY `fk_progreso_miembro` (`id_usuario_miembro`),
  ADD KEY `fk_usuario_entrenador` (`id_usuario_entrenador`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`id_proveedor`);

--
-- Indices de la tabla `reserva_clase`
--
ALTER TABLE `reserva_clase`
  ADD PRIMARY KEY (`id_reserva_clase`),
  ADD KEY `fk_reserva_clase_clase` (`id_clase`),
  ADD KEY `fk_reserva_clase_membresia_usuario` (`id_membresia_usuario`);

--
-- Indices de la tabla `reserva_maquina`
--
ALTER TABLE `reserva_maquina`
  ADD PRIMARY KEY (`id_reserva`),
  ADD KEY `fk_reserva_membresia_usuario` (`id_membresia_usuario`),
  ADD KEY `fk_reserva_inventario` (`id_inventario_maquina`);

--
-- Indices de la tabla `revision`
--
ALTER TABLE `revision`
  ADD PRIMARY KEY (`id_revision`),
  ADD KEY `fk_revision_inventario` (`id_inventario_maquina`),
  ADD KEY `fk_revision_estado` (`id_estado_revision`),
  ADD KEY `fk_revision_maquina_usuario` (`id_usuario`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `rutina`
--
ALTER TABLE `rutina`
  ADD PRIMARY KEY (`id_rutina`),
  ADD KEY `id_plan_trabajo` (`id_plan_trabajo`),
  ADD KEY `id_usuario_entrenador` (`id_usuario_entrenador`),
  ADD KEY `id_estado_rutina` (`id_estado_rutina`);

--
-- Indices de la tabla `rutina_ejercicio`
--
ALTER TABLE `rutina_ejercicio`
  ADD PRIMARY KEY (`id_rutina_ejercicio`),
  ADD KEY `id_rutina` (`id_rutina`),
  ADD KEY `id_ejercicio_rutina` (`id_ejercicio_rutina`),
  ADD KEY `id_dia` (`id_dia`);

--
-- Indices de la tabla `supervision`
--
ALTER TABLE `supervision`
  ADD PRIMARY KEY (`id_supervision`),
  ADD KEY `fk_supervision_accesso_miembro` (`id_acceso_miembro`),
  ADD KEY `fk_supervision_accesso_entrenador` (`id_acceso_entrenador`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `unikey_identificacion` (`identificacion`),
  ADD KEY `fk_usuario_rol` (`id_rol`),
  ADD KEY `fk_usuario_plan_trabajo` (`id_plan_trabajo`),
  ADD KEY `fk_usuario_genero` (`id_genero`);

--
-- Indices de la tabla `zona_cuerpo`
--
ALTER TABLE `zona_cuerpo`
  ADD PRIMARY KEY (`id_zona_cuerpo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `acceso`
--
ALTER TABLE `acceso`
  MODIFY `id_acceso` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=96;

--
-- AUTO_INCREMENT de la tabla `asignacion_rutina`
--
ALTER TABLE `asignacion_rutina`
  MODIFY `id_asignacion` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `clase`
--
ALTER TABLE `clase`
  MODIFY `id_clase` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `dia_semana`
--
ALTER TABLE `dia_semana`
  MODIFY `id_dia` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `ejercicio_rutina`
--
ALTER TABLE `ejercicio_rutina`
  MODIFY `id_ejercicio_rutina` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `estado_membresia`
--
ALTER TABLE `estado_membresia`
  MODIFY `id_estado_membresia` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `estado_revision`
--
ALTER TABLE `estado_revision`
  MODIFY `id_estado_revision` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `estado_rutina`
--
ALTER TABLE `estado_rutina`
  MODIFY `id_estado_rutina` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `genero`
--
ALTER TABLE `genero`
  MODIFY `id_genero` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `horario`
--
ALTER TABLE `horario`
  MODIFY `id_horario` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `horario_entrenador`
--
ALTER TABLE `horario_entrenador`
  MODIFY `id_horario_entrenador` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `inventario_maquina`
--
ALTER TABLE `inventario_maquina`
  MODIFY `id_inventario_maquina` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `maquina`
--
ALTER TABLE `maquina`
  MODIFY `id_maquina` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `membresia`
--
ALTER TABLE `membresia`
  MODIFY `id_membresia` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `membresia_usuario`
--
ALTER TABLE `membresia_usuario`
  MODIFY `id_membresia_usuario` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `nomina`
--
ALTER TABLE `nomina`
  MODIFY `id_nomina` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT de la tabla `observacion_revision`
--
ALTER TABLE `observacion_revision`
  MODIFY `id_obs_revision` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `plan_trabajo`
--
ALTER TABLE `plan_trabajo`
  MODIFY `id_plan_trabajo` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `progreso_trabajo`
--
ALTER TABLE `progreso_trabajo`
  MODIFY `id_progreso_trabajo` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `id_proveedor` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `reserva_clase`
--
ALTER TABLE `reserva_clase`
  MODIFY `id_reserva_clase` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `reserva_maquina`
--
ALTER TABLE `reserva_maquina`
  MODIFY `id_reserva` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT de la tabla `revision`
--
ALTER TABLE `revision`
  MODIFY `id_revision` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id_rol` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `rutina`
--
ALTER TABLE `rutina`
  MODIFY `id_rutina` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `rutina_ejercicio`
--
ALTER TABLE `rutina_ejercicio`
  MODIFY `id_rutina_ejercicio` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `supervision`
--
ALTER TABLE `supervision`
  MODIFY `id_supervision` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `zona_cuerpo`
--
ALTER TABLE `zona_cuerpo`
  MODIFY `id_zona_cuerpo` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `acceso`
--
ALTER TABLE `acceso`
  ADD CONSTRAINT `fk_acceso_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `asignacion_rutina`
--
ALTER TABLE `asignacion_rutina`
  ADD CONSTRAINT `asignacion_rutina_ibfk_1` FOREIGN KEY (`id_rutina`) REFERENCES `ejercicio_rutina` (`id_ejercicio_rutina`),
  ADD CONSTRAINT `asignacion_rutina_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `asignacion_rutina_ibfk_3` FOREIGN KEY (`id_dia`) REFERENCES `dia_semana` (`id_dia`),
  ADD CONSTRAINT `asignacion_rutina_ibfk_4` FOREIGN KEY (`id_estado_rutina`) REFERENCES `estado_rutina` (`id_estado_rutina`),
  ADD CONSTRAINT `asignacion_rutina_ibfk_5` FOREIGN KEY (`id_entrenador`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `cliente_entrenador`
--
ALTER TABLE `cliente_entrenador`
  ADD CONSTRAINT `cliente_entrenador_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `cliente_entrenador_ibfk_2` FOREIGN KEY (`id_entrenador`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `ejercicio_rutina`
--
ALTER TABLE `ejercicio_rutina`
  ADD CONSTRAINT `fk_ejercicio_dia` FOREIGN KEY (`id_dia`) REFERENCES `dia_semana` (`id_dia`),
  ADD CONSTRAINT `fk_ejercicio_maquina` FOREIGN KEY (`id_maquina`) REFERENCES `maquina` (`id_maquina`),
  ADD CONSTRAINT `fk_ejercicio_zona` FOREIGN KEY (`id_zona_cuerpo`) REFERENCES `zona_cuerpo` (`id_zona_cuerpo`),
  ADD CONSTRAINT `fk_rutina_usuario_entrenador` FOREIGN KEY (`id_usuario_entrenador`) REFERENCES `usuario` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Filtros para la tabla `horario_entrenador`
--
ALTER TABLE `horario_entrenador`
  ADD CONSTRAINT `fk_horario_entrenador_horario` FOREIGN KEY (`id_horario`) REFERENCES `horario` (`id_horario`),
  ADD CONSTRAINT `fk_horario_entrenador_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `inventario_maquina`
--
ALTER TABLE `inventario_maquina`
  ADD CONSTRAINT `fk_inventario_maquina` FOREIGN KEY (`id_maquina`) REFERENCES `maquina` (`id_maquina`),
  ADD CONSTRAINT `fk_inventario_proveedor` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedor` (`id_proveedor`);

--
-- Filtros para la tabla `membresia_usuario`
--
ALTER TABLE `membresia_usuario`
  ADD CONSTRAINT `fk_membresia_usuario_estado_membresia` FOREIGN KEY (`id_estado_membresia`) REFERENCES `estado_membresia` (`id_estado_membresia`),
  ADD CONSTRAINT `fk_membresia_usuario_membresia` FOREIGN KEY (`id_membresia`) REFERENCES `membresia` (`id_membresia`),
  ADD CONSTRAINT `fkmem_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `nomina`
--
ALTER TABLE `nomina`
  ADD CONSTRAINT `nomina_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `observacion_revision`
--
ALTER TABLE `observacion_revision`
  ADD CONSTRAINT `observacion_revision_ibfk_1` FOREIGN KEY (`id_revision`) REFERENCES `revision` (`id_revision`),
  ADD CONSTRAINT `observacion_revision_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `progreso_trabajo`
--
ALTER TABLE `progreso_trabajo`
  ADD CONSTRAINT `fk_usuario_entrenador` FOREIGN KEY (`id_usuario_entrenador`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `reserva_clase`
--
ALTER TABLE `reserva_clase`
  ADD CONSTRAINT `fk_reserva_clase_clase` FOREIGN KEY (`id_clase`) REFERENCES `clase` (`id_clase`),
  ADD CONSTRAINT `fk_reserva_clase_membresia_usuario` FOREIGN KEY (`id_membresia_usuario`) REFERENCES `membresia_usuario` (`id_membresia_usuario`);

--
-- Filtros para la tabla `reserva_maquina`
--
ALTER TABLE `reserva_maquina`
  ADD CONSTRAINT `fk_reserva_inventario` FOREIGN KEY (`id_inventario_maquina`) REFERENCES `inventario_maquina` (`id_inventario_maquina`),
  ADD CONSTRAINT `fk_reserva_membresia_usuario` FOREIGN KEY (`id_membresia_usuario`) REFERENCES `membresia_usuario` (`id_membresia_usuario`);

--
-- Filtros para la tabla `revision`
--
ALTER TABLE `revision`
  ADD CONSTRAINT `fk_revision_estado` FOREIGN KEY (`id_estado_revision`) REFERENCES `estado_revision` (`id_estado_revision`),
  ADD CONSTRAINT `fk_revision_inventario` FOREIGN KEY (`id_inventario_maquina`) REFERENCES `inventario_maquina` (`id_inventario_maquina`),
  ADD CONSTRAINT `fk_revision_maquina_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `rutina`
--
ALTER TABLE `rutina`
  ADD CONSTRAINT `rutina_ibfk_1` FOREIGN KEY (`id_plan_trabajo`) REFERENCES `plan_trabajo` (`id_plan_trabajo`),
  ADD CONSTRAINT `rutina_ibfk_2` FOREIGN KEY (`id_usuario_entrenador`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `rutina_ibfk_3` FOREIGN KEY (`id_estado_rutina`) REFERENCES `estado_rutina` (`id_estado_rutina`);

--
-- Filtros para la tabla `rutina_ejercicio`
--
ALTER TABLE `rutina_ejercicio`
  ADD CONSTRAINT `rutina_ejercicio_ibfk_1` FOREIGN KEY (`id_rutina`) REFERENCES `rutina` (`id_rutina`),
  ADD CONSTRAINT `rutina_ejercicio_ibfk_2` FOREIGN KEY (`id_ejercicio_rutina`) REFERENCES `ejercicio_rutina` (`id_ejercicio_rutina`),
  ADD CONSTRAINT `rutina_ejercicio_ibfk_3` FOREIGN KEY (`id_dia`) REFERENCES `dia_semana` (`id_dia`);

--
-- Filtros para la tabla `supervision`
--
ALTER TABLE `supervision`
  ADD CONSTRAINT `fk_supervision_accesso_entrenador` FOREIGN KEY (`id_acceso_entrenador`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `fk_supervision_accesso_miembro` FOREIGN KEY (`id_acceso_miembro`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `fk_usuario_genero` FOREIGN KEY (`id_genero`) REFERENCES `genero` (`id_genero`),
  ADD CONSTRAINT `fk_usuario_plan_trabajo` FOREIGN KEY (`id_plan_trabajo`) REFERENCES `plan_trabajo` (`id_plan_trabajo`),
  ADD CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
