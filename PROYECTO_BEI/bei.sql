-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-09-2024 a las 16:36:50
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bei`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contactus`
--

CREATE TABLE `contactus` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `message` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish2_ci;

--
-- Volcado de datos para la tabla `contactus`
--

INSERT INTO `contactus` (`id`, `name`, `email`, `message`) VALUES
(1, 'primer registro', 'primer@registro.com', 'primerregistrO'),
(2, 'AAAAAAAAAAAAA', 'AAAA@AAA.AA', 'AAAXAAAUn mago nunca llega tarde, Frodo Bolsón, ni pronto. · \"El camino va siempre, siempre hacia adelante\"'),
(3, 'EEE', 'EEE@EEE.EE', 'EEEE'),
(4, 'TEEE', 'AAAA@AAA.AA', 'aaaasasas'),
(5, 'EEE', 'EEE@EEE.EE', 'EEEEEEE'),
(6, 'Esteban Quintero Rodríguez', 'admin@admin.admin', 'Hola me gustaría saber cosas gracias!!!!!!! Soy Aragorn hijo de Arathorn y me llaman Elessar, Piedra de Elfo, Dúnadan, heredero del hijo de Isildur, hijo de Elendil de Gondor.'),
(7, 'Felipincio Garcimba', 'felipeencio@gmla.com.co', 'No te apresures a dar muerte y juicio. Incluso los más sabios no ven todos los fines». (Gandalf). La sabiduría de Gandalf ');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `precio` varchar(255) NOT NULL,
  `cantidad` varchar(255) NOT NULL,
  `imagen` varchar(255) NOT NULL,
  `disponibilidad` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `signup`
--

CREATE TABLE `signup` (
  `id` int(11) NOT NULL,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(150) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `tipo` tinyint(10) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish2_ci;

--
-- Volcado de datos para la tabla `signup`
--

INSERT INTO `signup` (`id`, `name`, `email`, `password`, `direccion`, `telefono`, `tipo`) VALUES
(3, 'SENA', 'sena@soysena.com', 'asasas', 'SENA', '53744568', 1),
(5, 'NUEVO USER5', 'esteban.quintero699@edcionbogota.edu.co', '3eroooo', 'cra 101 assda', '423343', 0),
(7, 'XAAAAAA', 'aeaeae@gm.com', 'AAAAAAAAAAA', 'AAA', '444', 0),
(8, 'JUANDAPEDRAZALEON', 'xxesteban@gm.com', 'AAAAAAAA', 'KRA 101 c', '12121212', 0),
(9, 'ESTEBITANN', 'estebaaaquin500@mail.com', 'AAAAA', 'XXESTEBANXX', '12345678909876', 0),
(10, 'PIPEPUNK', 'luifelipelecra@gg.com', 'DANIELMUÑOZ', 'socratescalle1', '989898989', 0),
(11, 'GABRIELEPINILLA', 'xxestean@gm.com', 'GABRIELLE', '12121', '2222222', 0),
(12, 'ADMINISTRADOR', 'admin@admin.admin', 'admin', 'admin123muñoz', '4dm1n', 0),
(13, ' registro', 'primer@registro.com', 'aa', 'aaa', 'aaa', 0),
(14, 'AAAAAAAAAAAAA', 'AAAA@AAA.AA', 'AAAAAAA', 'AAAAAAA', 'AAAAAAA', 0),
(15, 'k', 'k@k.k', 'k', 'k', 'k', 0),
(16, 'X', 'x@x.x', 'x', 'x', 'x', 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `contactus`
--
ALTER TABLE `contactus`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `signup`
--
ALTER TABLE `signup`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `contactus`
--
ALTER TABLE `contactus`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `signup`
--
ALTER TABLE `signup`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
