-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: iluled1
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actividad`
--

DROP TABLE IF EXISTS `actividad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `actividad` (
  `id_actividad` int(11) NOT NULL AUTO_INCREMENT,
  `id_luminaria` int(11) DEFAULT NULL,
  `id_municipio` int(11) NOT NULL,
  `id_barrio` int(11) DEFAULT NULL,
  `barrio` varchar(80) DEFAULT NULL,
  `id_tipo_actividad` int(11) NOT NULL COMMENT 'Tipo de Actividad Ejecutada',
  `id_tercero` int(11) DEFAULT NULL,
  `id_tipo_reporte` int(11) DEFAULT NULL COMMENT 'Se llena con el reportado en la PQR',
  `id_estado_actividad` int(11) NOT NULL,
  `direccion` varchar(100) DEFAULT NULL,
  `fch_ejecucion_actividad` datetime DEFAULT NULL COMMENT 'Fecha en la cual el tecnico ejecuta la actividad',
  `fch_reporte` datetime DEFAULT NULL COMMENT 'se llena con la fecha de la PQR',
  `observacion` text DEFAULT NULL,
  `latitud` decimal(16,13) NOT NULL DEFAULT 0.0000000000000,
  `longitud` decimal(16,13) NOT NULL DEFAULT 0.0000000000000,
  `seq` int(11) DEFAULT NULL,
  `id_pqr` int(11) DEFAULT NULL,
  `id_tercero_registra` int(11) DEFAULT NULL,
  `fch_registro` datetime DEFAULT NULL,
  `id_vehiculo` int(11) DEFAULT NULL,
  `id_tipo_luminaria` int(11) DEFAULT NULL,
  `poste_no` varchar(45) DEFAULT NULL,
  `fch_actualizacion` datetime DEFAULT NULL,
  `id_luminaria_retirada_modernizacion` int(11) DEFAULT NULL,
  `id_plan_trabajo` int(11) DEFAULT NULL,
  `referencia_secuencia` int(11) DEFAULT NULL,
  `ot_anterior` varchar(100) DEFAULT NULL,
  `fch_programacion` datetime DEFAULT NULL COMMENT 'Fecha en la cual se programa la actividad',
  `fch_retroalimentacion` datetime DEFAULT NULL COMMENT 'Fecha en que se retroalimenta la actividad luego de su ejecucion',
  `id_usuario_retroalimenta` int(11) DEFAULT NULL,
  `fch_final_ejecucion_actividad` datetime DEFAULT NULL,
  PRIMARY KEY (`id_actividad`),
  KEY `fk_luminaria_actividad_idx` (`id_luminaria`),
  KEY `fk_municipio_actividad_idx` (`id_municipio`),
  KEY `fk_barrio_actividad_idx` (`id_barrio`),
  KEY `fk_tipo_actividad_actividad_idx` (`id_tipo_actividad`),
  KEY `fk_tercero_actividad_idx` (`id_tercero`),
  KEY `fk_tipo_reporte_actividad_idx` (`id_tipo_reporte`),
  KEY `fk_estado_actividad_actividad_idx` (`id_estado_actividad`),
  KEY `fk_actividad_pqr` (`id_pqr`),
  KEY `fk_actividad_tercero_registra` (`id_tercero_registra`),
  KEY `fk_actividad_vehiculo` (`id_vehiculo`),
  KEY `fk_actividad_tipo_luminaria` (`id_tipo_luminaria`),
  KEY `fk_actividad_tercero_retroalimenta` (`id_usuario_retroalimenta`),
  CONSTRAINT `fk_actividad_pqr` FOREIGN KEY (`id_pqr`) REFERENCES `pqr` (`id_pqr`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_actividad_tercero_registra` FOREIGN KEY (`id_tercero_registra`) REFERENCES `tercero` (`id_tercero`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_actividad_tercero_retroalimenta` FOREIGN KEY (`id_usuario_retroalimenta`) REFERENCES `tercero` (`id_tercero`),
  CONSTRAINT `fk_actividad_tipo_luminaria` FOREIGN KEY (`id_tipo_luminaria`) REFERENCES `tipo_luminaria` (`id_tipo_luminaria`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_actividad_vehiculo` FOREIGN KEY (`id_vehiculo`) REFERENCES `vehiculo` (`id_vehiculo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_barrio_actividad` FOREIGN KEY (`id_barrio`) REFERENCES `barrio` (`id_barrio`),
  CONSTRAINT `fk_estado_actividad_actividad` FOREIGN KEY (`id_estado_actividad`) REFERENCES `tipo_actividad` (`id_tipo_actividad`),
  CONSTRAINT `fk_luminaria_actividad` FOREIGN KEY (`id_luminaria`) REFERENCES `luminaria` (`id_luminaria`),
  CONSTRAINT `fk_municipio_actividad` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`),
  CONSTRAINT `fk_tercero_actividad` FOREIGN KEY (`id_tercero`) REFERENCES `tercero` (`id_tercero`),
  CONSTRAINT `fk_tipo_actividad_actividad` FOREIGN KEY (`id_tipo_actividad`) REFERENCES `tipo_actividad` (`id_tipo_actividad`),
  CONSTRAINT `fk_tipo_reporte_actividad` FOREIGN KEY (`id_tipo_reporte`) REFERENCES `tipo_reporte` (`id_tipo_reporte`)
) ENGINE=InnoDB AUTO_INCREMENT=105960 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `afp`
--

DROP TABLE IF EXISTS `afp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `afp` (
  `id_afp` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_afp`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `archivo_pqr`
--

DROP TABLE IF EXISTS `archivo_pqr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `archivo_pqr` (
  `id_archivo_pqr` int(11) NOT NULL AUTO_INCREMENT,
  `id_pqr` int(11) NOT NULL,
  `tipo` varchar(45) NOT NULL,
  `tamano` int(11) NOT NULL,
  `extension` varchar(45) NOT NULL,
  `nombre_archivo` varchar(45) NOT NULL,
  `archivo` longblob NOT NULL,
  `id_tercero_registra` int(11) DEFAULT NULL,
  `fch_registro` datetime DEFAULT NULL,
  PRIMARY KEY (`id_archivo_pqr`),
  KEY `fk_archivo_pqr` (`id_pqr`),
  KEY `fk_archivo_pqr_tercero` (`id_tercero_registra`),
  CONSTRAINT `fk_archivo_pqr` FOREIGN KEY (`id_pqr`) REFERENCES `pqr` (`id_pqr`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_archivo_pqr_tercero` FOREIGN KEY (`id_tercero_registra`) REFERENCES `tercero` (`id_tercero`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `arl`
--

DROP TABLE IF EXISTS `arl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `arl` (
  `id_arl` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_arl`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `articulo`
--

DROP TABLE IF EXISTS `articulo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articulo` (
  `id_articulo` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(150) NOT NULL,
  `clase` enum('S','M') NOT NULL DEFAULT 'M' COMMENT 'S:SERVICIO M:MATERIAL',
  `orden_reporte` int(10) unsigned DEFAULT NULL,
  `id_unidad_medida` int(11) DEFAULT NULL,
  `visualizar_en_formato_actividad` enum('S','N') NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id_articulo`),
  KEY `articulo_unidad_medida_FK` (`id_unidad_medida`),
  CONSTRAINT `articulo_unidad_medida_FK` FOREIGN KEY (`id_unidad_medida`) REFERENCES `unidad_medida` (`id_unidad_medida`)
) ENGINE=InnoDB AUTO_INCREMENT=335 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `articulo_actividad`
--

DROP TABLE IF EXISTS `articulo_actividad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articulo_actividad` (
  `id_actividad` int(11) NOT NULL,
  `id_articulo` int(11) NOT NULL,
  `serial` varchar(24) DEFAULT NULL,
  `cantidad` decimal(10,2) NOT NULL DEFAULT 0.00,
  `id_unidad_medida` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_actividad`,`id_articulo`),
  KEY `fk_articulo_actividad` (`id_articulo`),
  KEY `fk_articulo_actividad_unidad_medida` (`id_unidad_medida`),
  CONSTRAINT `fk_articulo_actividad` FOREIGN KEY (`id_articulo`) REFERENCES `articulo` (`id_articulo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulo_actividad_actividad` FOREIGN KEY (`id_actividad`) REFERENCES `actividad` (`id_actividad`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulo_actividad_unidad_medida` FOREIGN KEY (`id_unidad_medida`) REFERENCES `unidad_medida` (`id_unidad_medida`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `articulo_retirado_actividad`
--

DROP TABLE IF EXISTS `articulo_retirado_actividad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articulo_retirado_actividad` (
  `id_actividad` int(11) NOT NULL,
  `id_articulo` int(11) NOT NULL,
  `serial` varchar(24) DEFAULT NULL,
  `cantidad` decimal(10,2) NOT NULL DEFAULT 0.00,
  `id_unidad_medida` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_actividad`,`id_articulo`),
  KEY `fk_articulo_retirado_actividad` (`id_articulo`),
  KEY `fk_articulo_retirado_actividad_unidad_medida` (`id_unidad_medida`),
  CONSTRAINT `fk_articulo_retirado_actividad` FOREIGN KEY (`id_articulo`) REFERENCES `articulo` (`id_articulo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulo_retirado_actividad_actividad` FOREIGN KEY (`id_actividad`) REFERENCES `actividad` (`id_actividad`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulo_retirado_actividad_unidad_medida` FOREIGN KEY (`id_unidad_medida`) REFERENCES `unidad_medida` (`id_unidad_medida`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `barrio`
--

DROP TABLE IF EXISTS `barrio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `barrio` (
  `id_barrio` int(11) NOT NULL AUTO_INCREMENT,
  `id_municipio` int(11) NOT NULL,
  `descripcion` varchar(80) NOT NULL,
  `codigo` varchar(12) DEFAULT NULL COMMENT 'codigo referencia de migracion',
  `comuna` varchar(12) DEFAULT NULL COMMENT 'codigo comuna referencia de migracion',
  PRIMARY KEY (`id_barrio`),
  KEY `fk_barrio_municipio_idx` (`id_municipio`),
  CONSTRAINT `fk_barrio_municipio` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`)
) ENGINE=InnoDB AUTO_INCREMENT=934 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='Barrios y Corregimiento de los Municipio';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cantidad_servicio_junio`
--

DROP TABLE IF EXISTS `cantidad_servicio_junio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cantidad_servicio_junio` (
  `FECHA_RECLAMO` date DEFAULT NULL,
  `FECHA_REVISION` date DEFAULT NULL,
  `MUNICIPIO` varchar(50) DEFAULT NULL,
  `COD_LUMINARIA` int(11) DEFAULT NULL,
  `POSTE` varchar(50) DEFAULT NULL,
  `RECONEXION_A_LA_RED` int(11) DEFAULT NULL,
  `REPARACIONDE_CONEXIONES_INTERNAS` int(11) DEFAULT NULL,
  `CAMBIO_DE_FOTOCELDA_DE_220` int(11) DEFAULT NULL,
  `BASE_DE_FOTO_CELDA` int(11) DEFAULT NULL,
  `DRIVER_45W` int(11) DEFAULT NULL,
  `CONECTORES_DE_KZ` int(11) DEFAULT NULL,
  `CABLE_N_6` int(11) DEFAULT NULL,
  `ID_MUNICIPIO` int(11) DEFAULT NULL,
  `ID_LUMINARIA` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cargo`
--

DROP TABLE IF EXISTS `cargo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cargo` (
  `id_cargo` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `id_empresa` int(11) DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_cargo`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `cargo_ibfk_1` FOREIGN KEY (`id_empresa`) REFERENCES `empresa` (`id_empresa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cargue_20241229`
--

DROP TABLE IF EXISTS `cargue_20241229`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cargue_20241229` (
  `numero_transformador` varchar(50) DEFAULT NULL,
  `capacidad` varchar(50) DEFAULT NULL,
  `uso` varchar(50) DEFAULT NULL,
  `circuito` varchar(50) DEFAULT NULL,
  `nodo` varchar(50) DEFAULT NULL,
  `operador` varchar(50) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `comuna` varchar(50) DEFAULT NULL,
  `barrio` varchar(200) DEFAULT NULL,
  `periodo_modernizacion` varchar(50) DEFAULT NULL,
  `fecha_modernizacion` date DEFAULT NULL,
  `codigo_luminaria_anterior` varchar(50) DEFAULT NULL,
  `potencia_luminaria_anterior` varchar(50) DEFAULT NULL,
  `luminaria` varchar(50) DEFAULT NULL,
  `nodo_apoyo` varchar(50) DEFAULT NULL,
  `coordenada_x` varchar(50) DEFAULT NULL,
  `coordenada_y` varchar(50) DEFAULT NULL,
  `direccion_2` varchar(200) DEFAULT NULL,
  `potencia` varchar(50) DEFAULT NULL,
  `clase_luminaria` varchar(50) DEFAULT NULL,
  `tipo_luminaria` varchar(50) DEFAULT NULL,
  `cantidad` varchar(50) DEFAULT NULL,
  `ubicacion` varchar(50) DEFAULT NULL,
  `puesta_tierra` varchar(50) DEFAULT NULL,
  `tipo_apoyo` varchar(50) DEFAULT NULL,
  `sec` varchar(50) DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `material` varchar(50) DEFAULT NULL,
  `altura` varchar(50) DEFAULT NULL,
  `carga` varchar(50) DEFAULT NULL,
  `poste_exclusivo` varchar(50) DEFAULT NULL,
  `poste_compartido` varchar(50) DEFAULT NULL,
  `retenida` varchar(50) DEFAULT NULL,
  `configuracion` varchar(50) DEFAULT NULL,
  `tipo_red` varchar(50) DEFAULT NULL,
  `conf` varchar(50) DEFAULT NULL,
  `calibre` varchar(50) DEFAULT NULL,
  `clase_aislado` varchar(50) DEFAULT NULL,
  `material_aislado` varchar(50) DEFAULT NULL,
  `camara` varchar(50) DEFAULT NULL,
  `cantidad_2` varchar(50) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17455 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cargue_20250210`
--

DROP TABLE IF EXISTS `cargue_20250210`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cargue_20250210` (
  `numero_transformador` varchar(50) DEFAULT NULL,
  `capacidad` varchar(50) DEFAULT NULL,
  `uso` varchar(50) DEFAULT NULL,
  `circuito` varchar(50) DEFAULT NULL,
  `nodo` varchar(50) DEFAULT NULL,
  `operador` varchar(50) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `comuna` varchar(50) DEFAULT NULL,
  `barrio` varchar(200) DEFAULT NULL,
  `periodo_modernizacion` varchar(50) DEFAULT NULL,
  `fecha_modernizacion` varchar(50) DEFAULT NULL,
  `codigo_luminaria_anterior` varchar(50) DEFAULT NULL,
  `potencia_luminaria_anterior` varchar(50) DEFAULT NULL,
  `luminaria` varchar(50) DEFAULT NULL,
  `nodo_apoyo` varchar(50) DEFAULT NULL,
  `coordenada_x` varchar(50) DEFAULT NULL,
  `coordenada_y` varchar(50) DEFAULT NULL,
  `direccion_2` varchar(200) DEFAULT NULL,
  `potencia` varchar(50) DEFAULT NULL,
  `clase_luminaria` varchar(50) DEFAULT NULL,
  `tipo_luminaria` varchar(50) DEFAULT NULL,
  `cantidad` varchar(50) DEFAULT NULL,
  `ubicacion` varchar(50) DEFAULT NULL,
  `puesta_tierra` varchar(50) DEFAULT NULL,
  `tipo_apoyo` varchar(50) DEFAULT NULL,
  `sec` varchar(50) DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `material` varchar(50) DEFAULT NULL,
  `altura` varchar(50) DEFAULT NULL,
  `carga` varchar(50) DEFAULT NULL,
  `poste_exclusivo` varchar(50) DEFAULT NULL,
  `poste_compartido` varchar(50) DEFAULT NULL,
  `retenida` varchar(50) DEFAULT NULL,
  `configuracion` varchar(50) DEFAULT NULL,
  `tipo_red` varchar(50) DEFAULT NULL,
  `conf` varchar(50) DEFAULT NULL,
  `calibre` varchar(50) DEFAULT NULL,
  `clase_aislado` varchar(50) DEFAULT NULL,
  `material_aislado` varchar(50) DEFAULT NULL,
  `camara` varchar(50) DEFAULT NULL,
  `cantidad_2` varchar(50) DEFAULT NULL,
  `id_luminaria` int(11) DEFAULT NULL,
  `fecha_procesamiento` date DEFAULT NULL,
  KEY `cargue_20250210_luminaria_IDX` (`luminaria`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cargue_20250905`
--

DROP TABLE IF EXISTS `cargue_20250905`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cargue_20250905` (
  `numero_transformador` varchar(50) DEFAULT NULL,
  `capacidad` varchar(50) DEFAULT NULL,
  `uso` varchar(50) DEFAULT NULL,
  `circuito` varchar(50) DEFAULT NULL,
  `nodo` varchar(50) DEFAULT NULL,
  `operador` varchar(50) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `comuna` varchar(50) DEFAULT NULL,
  `barrio` varchar(200) DEFAULT NULL,
  `periodo_modernizacion` varchar(50) DEFAULT NULL,
  `fecha_modernizacion` varchar(50) DEFAULT NULL,
  `codigo_luminaria_anterior` varchar(50) DEFAULT NULL,
  `potencia_luminaria_anterior` varchar(50) DEFAULT NULL,
  `luminaria` varchar(50) DEFAULT NULL,
  `nodo_apoyo` varchar(50) DEFAULT NULL,
  `coordenada_x` varchar(50) DEFAULT NULL,
  `coordenada_y` varchar(50) DEFAULT NULL,
  `direccion_2` varchar(200) DEFAULT NULL,
  `potencia` varchar(50) DEFAULT NULL,
  `clase_luminaria` varchar(50) DEFAULT NULL,
  `tipo_luminaria` varchar(50) DEFAULT NULL,
  `cantidad` varchar(50) DEFAULT NULL,
  `ubicacion` varchar(50) DEFAULT NULL,
  `puesta_tierra` varchar(50) DEFAULT NULL,
  `tipo_apoyo` varchar(50) DEFAULT NULL,
  `sec` varchar(50) DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `material` varchar(50) DEFAULT NULL,
  `altura` varchar(50) DEFAULT NULL,
  `carga` varchar(50) DEFAULT NULL,
  `poste_exclusivo` varchar(50) DEFAULT NULL,
  `poste_compartido` varchar(50) DEFAULT NULL,
  `retenida` varchar(50) DEFAULT NULL,
  `configuracion` varchar(50) DEFAULT NULL,
  `tipo_red` varchar(50) DEFAULT NULL,
  `conf` varchar(50) DEFAULT NULL,
  `calibre` varchar(50) DEFAULT NULL,
  `clase_aislado` varchar(50) DEFAULT NULL,
  `material_aislado` varchar(50) DEFAULT NULL,
  `camara` varchar(50) DEFAULT NULL,
  `cantidad_2` varchar(50) DEFAULT NULL,
  `id_luminaria` int(11) DEFAULT NULL,
  `fecha_procesamiento` date DEFAULT NULL,
  KEY `cargue_20250210_luminaria_IDX` (`luminaria`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `categoria_licencia_conduccion`
--

DROP TABLE IF EXISTS `categoria_licencia_conduccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categoria_licencia_conduccion` (
  `id_categoria_licencia_conduccion` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_categoria_licencia_conduccion`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `clase_iluminacion`
--

DROP TABLE IF EXISTS `clase_iluminacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clase_iluminacion` (
  `id_clase_iluminacion` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `abreviatura` varchar(4) NOT NULL,
  PRIMARY KEY (`id_clase_iluminacion`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comentario_pqr`
--

DROP TABLE IF EXISTS `comentario_pqr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comentario_pqr` (
  `id_comentario_pqr` int(11) NOT NULL AUTO_INCREMENT,
  `id_pqr` int(11) NOT NULL,
  `id_tercero` int(11) NOT NULL,
  `comentario` text NOT NULL,
  `fch_registro` datetime NOT NULL,
  PRIMARY KEY (`id_comentario_pqr`),
  KEY `fk_comentario_pqr` (`id_pqr`),
  KEY `fk_comentario_pqr_tercero` (`id_tercero`),
  CONSTRAINT `fk_comentario_pqr` FOREIGN KEY (`id_pqr`) REFERENCES `pqr` (`id_pqr`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_comentario_pqr_tercero` FOREIGN KEY (`id_tercero`) REFERENCES `tercero` (`id_tercero`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comercializador_energia`
--

DROP TABLE IF EXISTS `comercializador_energia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comercializador_energia` (
  `id_comercializador_energia` int(11) NOT NULL AUTO_INCREMENT,
  `nit` bigint(20) unsigned NOT NULL,
  `dv` int(2) NOT NULL DEFAULT 0,
  `razon_social` varchar(100) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_comercializador_energia`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comuna`
--

DROP TABLE IF EXISTS `comuna`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comuna` (
  `id_comuna` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) NOT NULL,
  `zona` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`id_comuna`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `condicion_luminaria`
--

DROP TABLE IF EXISTS `condicion_luminaria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `condicion_luminaria` (
  `id_condicion_luminaria` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(120) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  `codigo` varchar(12) DEFAULT NULL COMMENT 'codigo referencia de migracion',
  PRIMARY KEY (`id_condicion_luminaria`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `configuracion`
--

DROP TABLE IF EXISTS `configuracion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configuracion` (
  `id_medio_recepcion_pqr` int(11) NOT NULL COMMENT 'Medio recepcion default utilizado en el formulario destinado para la pagina web',
  `id_estado_pqr` int(11) NOT NULL COMMENT 'Estado inicial con el que se registra una pqr',
  `id_tercero_registra_pqr` int(11) NOT NULL COMMENT 'Usuario default utilizado para registrar las pqr desde formulario pagina web',
  `politica_tratamiento_datos` text DEFAULT NULL COMMENT 'Politica de tratamiento de datos',
  `ruta_logo` varchar(80) DEFAULT NULL COMMENT 'Ruta del logo de la empresa',
  `nombre_empresa` varchar(120) NOT NULL COMMENT 'Nombre de la empresa',
  `color_primario` varchar(7) DEFAULT NULL COMMENT 'Color primario de la aplicacion',
  `tema` varchar(12) DEFAULT NULL,
  `ruta_logo_2` varchar(80) DEFAULT NULL,
  `id_estado_inicial_actividad` int(11) DEFAULT NULL,
  `id_estado_actividad_finalizada` int(11) DEFAULT NULL,
  `id_estado_pqr_cerrada` int(11) DEFAULT NULL,
  `id_tipo_actividad_predeterminada` int(11) DEFAULT NULL,
  `id_estado_activa_luminaria` int(11) DEFAULT NULL,
  `porcentaje_meta_nivel_eficiencia` decimal(4,2) DEFAULT NULL,
  KEY `fk_configuracion_estado_inicial_actividad` (`id_estado_inicial_actividad`),
  KEY `fk_configuracion_estado_actividad_finalizada` (`id_estado_actividad_finalizada`),
  KEY `fk_configuracion_estado_pqr_cerrada` (`id_estado_pqr_cerrada`),
  KEY `fk_configuracion_tipo_actividad_predeterminada` (`id_tipo_actividad_predeterminada`),
  KEY `fk_configuracion_estado_luminaria` (`id_estado_activa_luminaria`),
  CONSTRAINT `fk_configuracion_estado_actividad_finalizada` FOREIGN KEY (`id_estado_actividad_finalizada`) REFERENCES `estado_actividad` (`id_estado_actividad`),
  CONSTRAINT `fk_configuracion_estado_inicial_actividad` FOREIGN KEY (`id_estado_inicial_actividad`) REFERENCES `estado_actividad` (`id_estado_actividad`),
  CONSTRAINT `fk_configuracion_estado_luminaria` FOREIGN KEY (`id_estado_activa_luminaria`) REFERENCES `estado_luminaria` (`id_estado_luminaria`),
  CONSTRAINT `fk_configuracion_estado_pqr_cerrada` FOREIGN KEY (`id_estado_pqr_cerrada`) REFERENCES `estado_pqr` (`id_estado_pqr`),
  CONSTRAINT `fk_configuracion_tipo_actividad_predeterminada` FOREIGN KEY (`id_tipo_actividad_predeterminada`) REFERENCES `tipo_actividad` (`id_tipo_actividad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cuadrilla`
--

DROP TABLE IF EXISTS `cuadrilla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cuadrilla` (
  `id_cuadrilla` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) NOT NULL,
  `codigo` varchar(12) DEFAULT NULL COMMENT 'codigo referencia de migracion',
  PRIMARY KEY (`id_cuadrilla`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cuadrilla_tercero`
--

DROP TABLE IF EXISTS `cuadrilla_tercero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cuadrilla_tercero` (
  `id_cuadrilla_tercero` int(11) NOT NULL AUTO_INCREMENT,
  `id_cuadrilla` int(11) NOT NULL,
  `id_tercero` int(11) NOT NULL,
  PRIMARY KEY (`id_cuadrilla_tercero`),
  UNIQUE KEY `cuadrilla_tercero_UN` (`id_cuadrilla`,`id_tercero`),
  KEY `fk_cuadrilla_tercero_tercero` (`id_tercero`),
  CONSTRAINT `fk_cuadrilla_tercero_cuadrilla` FOREIGN KEY (`id_cuadrilla`) REFERENCES `cuadrilla` (`id_cuadrilla`),
  CONSTRAINT `fk_cuadrilla_tercero_tercero` FOREIGN KEY (`id_tercero`) REFERENCES `tercero` (`id_tercero`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `departamento`
--

DROP TABLE IF EXISTS `departamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departamento` (
  `id_departamento` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `codigo_dane` int(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_departamento`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `empleado`
--

DROP TABLE IF EXISTS `empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empleado` (
  `id_empleado` int(11) NOT NULL AUTO_INCREMENT,
  `id_empresa` int(11) DEFAULT NULL,
  `id_sede` int(11) DEFAULT NULL,
  `id_proceso` int(11) DEFAULT NULL,
  `id_empresa_servicio_temporal` int(11) DEFAULT NULL COMMENT 'Empresa de servicios temporales',
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `identificacion` varchar(20) NOT NULL,
  `id_tipo_identificacion` int(11) DEFAULT NULL,
  `id_estado_civil` int(11) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `edad` varchar(10) DEFAULT NULL,
  `id_nivel_escolaridad` int(11) DEFAULT NULL,
  `profesion` varchar(100) DEFAULT NULL,
  `lugar_nacimiento` varchar(100) DEFAULT NULL,
  `id_tipo_vivienda` int(11) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `id_municipio` int(11) DEFAULT NULL,
  `telefono_fijo` varchar(20) DEFAULT NULL,
  `celular_personal` varchar(20) DEFAULT NULL,
  `celular_corporativo` varchar(20) DEFAULT NULL,
  `email_personal` varchar(100) DEFAULT NULL,
  `email_corporativo` varchar(100) DEFAULT NULL,
  `email_nomina` varchar(100) DEFAULT NULL,
  `fecha_contratacion` date DEFAULT NULL,
  `fecha_retiro` date DEFAULT NULL,
  `id_eps` int(11) DEFAULT NULL,
  `id_ips` int(11) DEFAULT NULL,
  `id_afp` int(11) DEFAULT NULL,
  `id_arl` int(11) DEFAULT NULL,
  `id_nivel_riesgo` int(11) DEFAULT NULL,
  `id_grupo_sanguineo` int(11) DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo, R=Retirado',
  `id_cargo` int(11) DEFAULT NULL,
  `id_tipo_contrato` int(11) DEFAULT NULL,
  `cuenta_bancaria` varchar(50) DEFAULT NULL,
  `id_tipo_cuenta` int(11) DEFAULT NULL,
  `id_entidad_bancaria` int(11) DEFAULT NULL,
  `licencia_conduccion` varchar(20) DEFAULT NULL,
  `fecha_vencimiento_licencia` date DEFAULT NULL,
  `placa` varchar(20) DEFAULT NULL,
  `id_categoria_licencia_conduccion` int(11) DEFAULT NULL,
  `id_tercero_ingresa` int(11) DEFAULT NULL,
  `id_tercero_actualiza` int(11) DEFAULT NULL,
  `ejecuta_labor_operativa` char(1) DEFAULT 'S' COMMENT 'S=Sí, N=No',
  `privilegio_cumpleanos` char(1) DEFAULT 'S' COMMENT 'S=Sí, N=No',
  `foto` varchar(255) DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_actualizacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id_empleado`),
  KEY `id_empresa` (`id_empresa`),
  KEY `id_sede` (`id_sede`),
  KEY `id_proceso` (`id_proceso`),
  KEY `id_empresa_servicio_temporal` (`id_empresa_servicio_temporal`),
  KEY `id_tipo_identificacion` (`id_tipo_identificacion`),
  KEY `id_nivel_escolaridad` (`id_nivel_escolaridad`),
  KEY `id_tipo_vivienda` (`id_tipo_vivienda`),
  KEY `id_tipo_cuenta` (`id_tipo_cuenta`),
  KEY `id_entidad_bancaria` (`id_entidad_bancaria`),
  KEY `id_categoria_licencia_conduccion` (`id_categoria_licencia_conduccion`),
  KEY `id_eps` (`id_eps`),
  KEY `id_ips` (`id_ips`),
  KEY `id_afp` (`id_afp`),
  KEY `id_arl` (`id_arl`),
  KEY `id_cargo` (`id_cargo`),
  KEY `id_estado_civil` (`id_estado_civil`),
  KEY `id_nivel_riesgo` (`id_nivel_riesgo`),
  KEY `id_grupo_sanguineo` (`id_grupo_sanguineo`),
  KEY `id_tipo_contrato` (`id_tipo_contrato`),
  CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`id_empresa`) REFERENCES `empresa` (`id_empresa`),
  CONSTRAINT `empleado_ibfk_10` FOREIGN KEY (`id_categoria_licencia_conduccion`) REFERENCES `categoria_licencia_conduccion` (`id_categoria_licencia_conduccion`),
  CONSTRAINT `empleado_ibfk_11` FOREIGN KEY (`id_eps`) REFERENCES `eps` (`id_eps`),
  CONSTRAINT `empleado_ibfk_12` FOREIGN KEY (`id_ips`) REFERENCES `ips` (`id_ips`),
  CONSTRAINT `empleado_ibfk_13` FOREIGN KEY (`id_afp`) REFERENCES `afp` (`id_afp`),
  CONSTRAINT `empleado_ibfk_14` FOREIGN KEY (`id_arl`) REFERENCES `arl` (`id_arl`),
  CONSTRAINT `empleado_ibfk_15` FOREIGN KEY (`id_cargo`) REFERENCES `cargo` (`id_cargo`),
  CONSTRAINT `empleado_ibfk_16` FOREIGN KEY (`id_estado_civil`) REFERENCES `estado_civil` (`id_estado_civil`),
  CONSTRAINT `empleado_ibfk_17` FOREIGN KEY (`id_nivel_riesgo`) REFERENCES `nivel_riesgo` (`id_nivel_riesgo`),
  CONSTRAINT `empleado_ibfk_18` FOREIGN KEY (`id_grupo_sanguineo`) REFERENCES `grupo_sanguineo` (`id_grupo_sanguineo`),
  CONSTRAINT `empleado_ibfk_19` FOREIGN KEY (`id_tipo_contrato`) REFERENCES `tipo_contrato` (`id_tipo_contrato`),
  CONSTRAINT `empleado_ibfk_2` FOREIGN KEY (`id_sede`) REFERENCES `sede` (`id_sede`),
  CONSTRAINT `empleado_ibfk_3` FOREIGN KEY (`id_proceso`) REFERENCES `proceso` (`id_proceso`),
  CONSTRAINT `empleado_ibfk_4` FOREIGN KEY (`id_empresa_servicio_temporal`) REFERENCES `empresa_servicio_temporal` (`id_empresa_servicio_temporal`),
  CONSTRAINT `empleado_ibfk_5` FOREIGN KEY (`id_tipo_identificacion`) REFERENCES `tipo_identificacion` (`id_tipo_identificacion`),
  CONSTRAINT `empleado_ibfk_6` FOREIGN KEY (`id_nivel_escolaridad`) REFERENCES `nivel_escolaridad` (`id_nivel_escolaridad`),
  CONSTRAINT `empleado_ibfk_7` FOREIGN KEY (`id_tipo_vivienda`) REFERENCES `tipo_vivienda` (`id_tipo_vivienda`),
  CONSTRAINT `empleado_ibfk_8` FOREIGN KEY (`id_tipo_cuenta`) REFERENCES `tipo_cuenta` (`id_tipo_cuenta`),
  CONSTRAINT `empleado_ibfk_9` FOREIGN KEY (`id_entidad_bancaria`) REFERENCES `entidad_bancaria` (`id_entidad_bancaria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `empresa`
--

DROP TABLE IF EXISTS `empresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empresa` (
  `id_empresa` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_empresa`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `empresa_servicio_temporal`
--

DROP TABLE IF EXISTS `empresa_servicio_temporal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `empresa_servicio_temporal` (
  `id_empresa_servicio_temporal` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `nit` varchar(20) DEFAULT NULL,
  `direccion` text DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_empresa_servicio_temporal`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `encuesta`
--

DROP TABLE IF EXISTS `encuesta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encuesta` (
  `id_encuesta` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `id_usuario_servicio` int(11) DEFAULT NULL,
  `nombre_usuario_servicio` varchar(80) NOT NULL,
  `id_barrio` int(11) DEFAULT NULL,
  `direccion` varchar(80) NOT NULL,
  `telefono` varchar(45) DEFAULT NULL,
  `correo_electronico` varchar(80) DEFAULT NULL,
  `id_tercero_registra` int(11) NOT NULL,
  `fch_encuesta` date NOT NULL,
  `fch_registro` datetime NOT NULL,
  `calidad_servicio` enum('E','B','R','M') NOT NULL DEFAULT 'E',
  `tiempo_atencion` enum('E','B','R','M') NOT NULL DEFAULT 'E',
  `atencion_grupo_trabajo` enum('E','B','R','M') NOT NULL DEFAULT 'E',
  `comentario` text DEFAULT NULL,
  `fch_actualiza` datetime DEFAULT NULL,
  `id_tercero_actualiza` int(11) DEFAULT NULL,
  `id_pqr` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_encuesta`),
  KEY `fk_encuesta_barrio` (`id_barrio`),
  KEY `fk_encuesta_tercero` (`id_tercero_registra`),
  KEY `fk_encuesta_usuario_servicio` (`id_usuario_servicio`),
  KEY `fk_encuensta_tercero_actualiza` (`id_tercero_actualiza`),
  KEY `fk_encuesta_pqr` (`id_pqr`),
  CONSTRAINT `fk_encuensta_tercero_actualiza` FOREIGN KEY (`id_tercero_actualiza`) REFERENCES `tercero` (`id_tercero`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_encuesta_barrio` FOREIGN KEY (`id_barrio`) REFERENCES `barrio` (`id_barrio`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_encuesta_pqr` FOREIGN KEY (`id_pqr`) REFERENCES `pqr` (`id_pqr`),
  CONSTRAINT `fk_encuesta_tercero` FOREIGN KEY (`id_tercero_registra`) REFERENCES `tercero` (`id_tercero`) ON DELETE NO ACTION,
  CONSTRAINT `fk_encuesta_usuario_servicio` FOREIGN KEY (`id_usuario_servicio`) REFERENCES `usuario_servicio` (`id_usuario_servicio`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3305 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `entidad_bancaria`
--

DROP TABLE IF EXISTS `entidad_bancaria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entidad_bancaria` (
  `id_entidad_bancaria` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_entidad_bancaria`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eps`
--

DROP TABLE IF EXISTS `eps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eps` (
  `id_eps` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_eps`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_actividad`
--

DROP TABLE IF EXISTS `estado_actividad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estado_actividad` (
  `id_estado_actividad` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  PRIMARY KEY (`id_estado_actividad`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_civil`
--

DROP TABLE IF EXISTS `estado_civil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estado_civil` (
  `id_estado_civil` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_estado_civil`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_luminaria`
--

DROP TABLE IF EXISTS `estado_luminaria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estado_luminaria` (
  `id_estado_luminaria` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  PRIMARY KEY (`id_estado_luminaria`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estado_pqr`
--

DROP TABLE IF EXISTS `estado_pqr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estado_pqr` (
  `id_estado_pqr` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `permitir_edicion` enum('S','N') NOT NULL DEFAULT 'N',
  `permitir_eliminar` enum('S','N') NOT NULL DEFAULT 'N',
  `codigo` varchar(12) DEFAULT NULL COMMENT 'codigo referencia de migracion',
  PRIMARY KEY (`id_estado_pqr`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `factura_liquidacion`
--

DROP TABLE IF EXISTS `factura_liquidacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `factura_liquidacion` (
  `id_factura` int(11) NOT NULL AUTO_INCREMENT,
  `id_liquidacion` int(11) NOT NULL,
  `id_nic` int(11) NOT NULL,
  `lectura` int(11) DEFAULT NULL,
  `consumo` int(11) NOT NULL,
  `valor_tarifa` decimal(8,2) NOT NULL DEFAULT 0.00,
  `valor_consumo` decimal(15,2) NOT NULL DEFAULT 0.00,
  `fch_ini_facturacion` date NOT NULL,
  `fch_fin_facturacion` date NOT NULL,
  PRIMARY KEY (`id_factura`),
  KEY `factura_liquidacion_FK` (`id_liquidacion`),
  KEY `factura_liquidacion_FK_1` (`id_nic`),
  CONSTRAINT `factura_liquidacion_FK` FOREIGN KEY (`id_liquidacion`) REFERENCES `liquidacion` (`id_liquidacion`),
  CONSTRAINT `factura_liquidacion_FK_1` FOREIGN KEY (`id_nic`) REFERENCES `nic_municipio` (`id_nic`)
) ENGINE=InnoDB AUTO_INCREMENT=465 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `foto_luminaria`
--

DROP TABLE IF EXISTS `foto_luminaria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `foto_luminaria` (
  `id_foto_luminaria` int(11) NOT NULL AUTO_INCREMENT,
  `id_luminaria` int(11) NOT NULL,
  `tipo_foto` varchar(100) NOT NULL,
  `tamano_foto` int(11) NOT NULL,
  `foto` longblob DEFAULT NULL,
  `nombre_foto` varchar(100) NOT NULL,
  PRIMARY KEY (`id_foto_luminaria`),
  KEY `fk_foto_luminaria_luminaria` (`id_luminaria`),
  CONSTRAINT `fk_foto_luminaria_luminaria` FOREIGN KEY (`id_luminaria`) REFERENCES `luminaria` (`id_luminaria`)
) ENGINE=InnoDB AUTO_INCREMENT=66693 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `grupo_sanguineo`
--

DROP TABLE IF EXISTS `grupo_sanguineo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grupo_sanguineo` (
  `id_grupo_sanguineo` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(5) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_grupo_sanguineo`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ips`
--

DROP TABLE IF EXISTS `ips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ips` (
  `id_ips` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_ips`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `liquidacion`
--

DROP TABLE IF EXISTS `liquidacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `liquidacion` (
  `id_liquidacion` int(11) NOT NULL AUTO_INCREMENT,
  `id_municipio` int(11) NOT NULL,
  `periodo_liquidacion` int(4) NOT NULL,
  `mes_liquidacion` int(2) NOT NULL,
  `valor_consumo` decimal(15,2) NOT NULL DEFAULT 0.00,
  `facturacion_impuesto_ap` decimal(15,2) NOT NULL DEFAULT 0.00,
  `recaudo_impuesto_ap` decimal(15,2) NOT NULL DEFAULT 0.00,
  `facturacion_energia` decimal(15,2) NOT NULL DEFAULT 0.00,
  `facturacion_tsycc` decimal(15,2) NOT NULL DEFAULT 0.00,
  `recaudo_tsycc` decimal(15,2) NOT NULL DEFAULT 0.00,
  `id_tercero_registra` int(11) NOT NULL,
  `fch_registro` datetime NOT NULL,
  `id_tercero_actualiza` int(11) NOT NULL,
  `fch_actualiza` datetime NOT NULL,
  PRIMARY KEY (`id_liquidacion`),
  KEY `liquidacion_FK` (`id_municipio`),
  KEY `liquidacion_FK_1` (`id_tercero_registra`),
  KEY `liquidacion_FK_2` (`id_tercero_actualiza`),
  CONSTRAINT `liquidacion_FK` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`),
  CONSTRAINT `liquidacion_FK_1` FOREIGN KEY (`id_tercero_registra`) REFERENCES `tercero` (`id_tercero`),
  CONSTRAINT `liquidacion_FK_2` FOREIGN KEY (`id_tercero_actualiza`) REFERENCES `tercero` (`id_tercero`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`mes_liquidacion` >= 1 and `mes_liquidacion` <= 12)
) ENGINE=InnoDB AUTO_INCREMENT=402 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `luminaria`
--

DROP TABLE IF EXISTS `luminaria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `luminaria` (
  `id_luminaria` int(11) NOT NULL AUTO_INCREMENT,
  `poste_no` varchar(45) NOT NULL,
  `luminaria_no` varchar(45) DEFAULT NULL,
  `id_tipo_luminaria` int(11) DEFAULT NULL,
  `id_municipio` int(11) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  `id_barrio` int(11) NOT NULL,
  `latitud` decimal(16,13) NOT NULL DEFAULT 0.0000000000000,
  `longitud` decimal(16,13) NOT NULL DEFAULT 0.0000000000000,
  `id_tercero` int(11) DEFAULT NULL COMMENT 'Técnico Instalador',
  `referencia` varchar(45) DEFAULT NULL,
  `potencia` decimal(8,2) DEFAULT 0.00,
  `fch_instalacion` date DEFAULT NULL,
  `fch_registro` datetime NOT NULL,
  `id_tercero_registra` int(11) NOT NULL COMMENT 'Usuario del sistema quien realiza el registro de la luminaria',
  `id_estado_luminaria` int(11) NOT NULL,
  `id_tercero_proveedor` int(11) DEFAULT NULL COMMENT 'Proveedor de la luminaria',
  `id_periodo_mantenimiento` int(11) DEFAULT NULL,
  `fch_actualizacion` datetime DEFAULT NULL,
  `propiedad_poste` enum('C','E') NOT NULL DEFAULT 'C' COMMENT 'C:Compartido,E:Exclusivo',
  `id_tipo_poste` int(11) NOT NULL,
  `id_norma_tipo_poste` int(11) NOT NULL,
  `id_tipo_brazo` int(11) NOT NULL,
  `id_marca_luminaria` int(11) NOT NULL,
  `zona` enum('U','R') NOT NULL DEFAULT 'U' COMMENT 'U:Urbana, R:Rural',
  `nodo` varchar(12) DEFAULT NULL COMMENT 'marca en poste del nodo',
  `transformador_no` varchar(45) DEFAULT NULL COMMENT 'Identificacion del transformador',
  `potencia_transformador` decimal(6,2) DEFAULT NULL COMMENT 'Potencia del Transformador en KVA',
  `id_propiedad_transformador` int(11) DEFAULT NULL,
  `id_luminaria_retirada` int(11) DEFAULT NULL,
  `luminaria_no_retirada` varchar(45) DEFAULT NULL,
  `potencia_luminaria_retirada` varchar(45) DEFAULT NULL,
  `referencia_barrio` varchar(120) DEFAULT NULL,
  `referencia_secuencia` int(11) DEFAULT NULL,
  `id_comuna` int(11) DEFAULT NULL,
  `id_condicion_luminaria` int(11) DEFAULT NULL,
  `id_operador_red_energia` int(11) NOT NULL,
  `id_tipo_espacio` int(11) NOT NULL,
  `puesta_tierra` enum('S','N') NOT NULL DEFAULT 'S',
  `id_tipo_red` int(11) NOT NULL,
  `id_tipo_retenida` int(11) DEFAULT NULL,
  `id_tipo_apoyo` int(11) DEFAULT NULL,
  `circuito_no` varchar(12) DEFAULT NULL,
  `nodo_transformador` varchar(12) DEFAULT NULL COMMENT 'Número del nodo que identifica al transformador',
  `propiedad_circuito` enum('C','E') DEFAULT NULL COMMENT 'C:Compartido,E:Exclusivo',
  PRIMARY KEY (`id_luminaria`),
  KEY `fk_luminaria_tipo_luminaria_idx` (`id_tipo_luminaria`),
  KEY `fk_luminaria_municipio_idx` (`id_municipio`),
  KEY `fk_luminaria_barrio_idx` (`id_barrio`),
  KEY `fk_luminaria_tercero_idx` (`id_tercero`),
  KEY `fk_luminaria_estado_luminaria_idx` (`id_estado_luminaria`),
  KEY `fk_luminaria_periodo_mantenimiento` (`id_periodo_mantenimiento`),
  KEY `fk_luminaria_propiedad_transformador` (`id_propiedad_transformador`),
  KEY `fk_luminaria_comuna` (`id_comuna`),
  KEY `fk_luminaria_condicion_luminaria` (`id_condicion_luminaria`),
  KEY `fk_luminaria_operador_red_energia` (`id_operador_red_energia`),
  KEY `fk_luminaria_tipo_espacio` (`id_tipo_espacio`),
  KEY `fk_luminaria_tipo_red` (`id_tipo_red`),
  KEY `fk_luminaria_tipo_retenida` (`id_tipo_retenida`),
  KEY `fk_luminaria_tipo_apoyo` (`id_tipo_apoyo`),
  CONSTRAINT `fk_luminaria_barrio` FOREIGN KEY (`id_barrio`) REFERENCES `barrio` (`id_barrio`),
  CONSTRAINT `fk_luminaria_comuna` FOREIGN KEY (`id_comuna`) REFERENCES `comuna` (`id_comuna`),
  CONSTRAINT `fk_luminaria_condicion_luminaria` FOREIGN KEY (`id_condicion_luminaria`) REFERENCES `condicion_luminaria` (`id_condicion_luminaria`),
  CONSTRAINT `fk_luminaria_estado_luminaria` FOREIGN KEY (`id_estado_luminaria`) REFERENCES `estado_luminaria` (`id_estado_luminaria`),
  CONSTRAINT `fk_luminaria_municipio` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`),
  CONSTRAINT `fk_luminaria_operador_red_energia` FOREIGN KEY (`id_operador_red_energia`) REFERENCES `operador_red_energia` (`id_operador_red_energia`),
  CONSTRAINT `fk_luminaria_periodo_mantenimiento` FOREIGN KEY (`id_periodo_mantenimiento`) REFERENCES `periodo_mantenimiento` (`id_periodo_mantenimiento`),
  CONSTRAINT `fk_luminaria_propiedad_transformador` FOREIGN KEY (`id_propiedad_transformador`) REFERENCES `propiedad_transformador` (`id_propiedad_transformador`),
  CONSTRAINT `fk_luminaria_tercero` FOREIGN KEY (`id_tercero`) REFERENCES `tercero` (`id_tercero`),
  CONSTRAINT `fk_luminaria_tipo_apoyo` FOREIGN KEY (`id_tipo_apoyo`) REFERENCES `tipo_apoyo` (`id_tipo_apoyo`),
  CONSTRAINT `fk_luminaria_tipo_espacio` FOREIGN KEY (`id_tipo_espacio`) REFERENCES `tipo_espacio` (`id_tipo_espacio`),
  CONSTRAINT `fk_luminaria_tipo_luminaria` FOREIGN KEY (`id_tipo_luminaria`) REFERENCES `tipo_luminaria` (`id_tipo_luminaria`),
  CONSTRAINT `fk_luminaria_tipo_red` FOREIGN KEY (`id_tipo_red`) REFERENCES `tipo_red` (`id_tipo_red`),
  CONSTRAINT `fk_luminaria_tipo_retenida` FOREIGN KEY (`id_tipo_retenida`) REFERENCES `tipo_retenida` (`id_tipo_retenida`)
) ENGINE=InnoDB AUTO_INCREMENT=16343 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `marca_luminaria`
--

DROP TABLE IF EXISTS `marca_luminaria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `marca_luminaria` (
  `id_marca_luminaria` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  `codigo` varchar(12) DEFAULT NULL COMMENT 'codigo referencia de migracion',
  PRIMARY KEY (`id_marca_luminaria`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `medicion_luminaria`
--

DROP TABLE IF EXISTS `medicion_luminaria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medicion_luminaria` (
  `id_medicion` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `id_luminaria` int(11) NOT NULL,
  `id_clase_iluminacion` int(11) unsigned NOT NULL,
  `fch_visita` date NOT NULL,
  `hm` decimal(4,2) NOT NULL DEFAULT 0.00,
  `sm` decimal(4,2) NOT NULL DEFAULT 0.00,
  `wm` decimal(4,2) NOT NULL DEFAULT 0.00,
  `ilum_lux` decimal(4,2) NOT NULL DEFAULT 0.00,
  `uniformidad` decimal(5,2) NOT NULL DEFAULT 0.00,
  `cumple_retilap` enum('S','N') NOT NULL DEFAULT 'N',
  `id_tercero` int(11) NOT NULL,
  `fch_registro` datetime NOT NULL,
  `tipo` enum('D','V') NOT NULL DEFAULT 'D' COMMENT 'D:Medidas para el Diseño,V:Verificacion Medida en campo.',
  PRIMARY KEY (`id_medicion`),
  KEY `fk_medicion_luminaria` (`id_luminaria`),
  KEY `fk_medicion_luminaria_clase_iluminacion` (`id_clase_iluminacion`),
  KEY `fk_medicion_luminaria_tercero` (`id_tercero`),
  CONSTRAINT `fk_medicion_luminaria` FOREIGN KEY (`id_luminaria`) REFERENCES `luminaria` (`id_luminaria`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_medicion_luminaria_clase_iluminacion` FOREIGN KEY (`id_clase_iluminacion`) REFERENCES `clase_iluminacion` (`id_clase_iluminacion`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_medicion_luminaria_tercero` FOREIGN KEY (`id_tercero`) REFERENCES `tercero` (`id_tercero`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=191 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `medio_recepcion_pqr`
--

DROP TABLE IF EXISTS `medio_recepcion_pqr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medio_recepcion_pqr` (
  `id_medio_recepcion_pqr` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `codigo` varchar(12) DEFAULT NULL COMMENT 'codigo referencia de migracion',
  PRIMARY KEY (`id_medio_recepcion_pqr`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `menu` (
  `id_menu` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `ruta_pagina` varchar(80) DEFAULT NULL,
  `ejecutable` enum('S','N') NOT NULL DEFAULT 'N',
  `id_menu_padre` int(11) DEFAULT NULL,
  `descripcion` varchar(45) NOT NULL,
  `orden` int(11) NOT NULL,
  `icono` varchar(45) NOT NULL,
  PRIMARY KEY (`id_menu`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `menu_tercero`
--

DROP TABLE IF EXISTS `menu_tercero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `menu_tercero` (
  `id_menu` int(11) NOT NULL,
  `id_tercero` int(11) NOT NULL,
  `crear` enum('S','N') NOT NULL DEFAULT 'N',
  `actualizar` enum('S','N') NOT NULL DEFAULT 'N',
  `eliminar` enum('S','N') NOT NULL DEFAULT 'N',
  `imprimir` enum('S','N') NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id_menu`,`id_tercero`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `municipio`
--

DROP TABLE IF EXISTS `municipio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `municipio` (
  `id_municipio` int(11) NOT NULL AUTO_INCREMENT,
  `id_departamento` int(11) NOT NULL,
  `descripcion` varchar(45) NOT NULL,
  `tiene_contrato` enum('S','N') NOT NULL DEFAULT 'N',
  `latitud` decimal(16,13) DEFAULT NULL,
  `longitud` decimal(16,13) DEFAULT NULL,
  `codigo_dane` int(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_municipio`),
  KEY `fk_municipio_departamento_idx` (`id_departamento`),
  CONSTRAINT `fk_municipio_departamento` FOREIGN KEY (`id_departamento`) REFERENCES `departamento` (`id_departamento`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nic_municipio`
--

DROP TABLE IF EXISTS `nic_municipio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nic_municipio` (
  `id_nic` int(11) NOT NULL AUTO_INCREMENT,
  `id_municipio` int(11) NOT NULL,
  `nic` int(11) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  PRIMARY KEY (`id_nic`),
  KEY `nic_municipio_FK` (`id_municipio`),
  CONSTRAINT `nic_municipio_FK` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nivel_escolaridad`
--

DROP TABLE IF EXISTS `nivel_escolaridad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nivel_escolaridad` (
  `id_nivel_escolaridad` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_nivel_escolaridad`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nivel_riesgo`
--

DROP TABLE IF EXISTS `nivel_riesgo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nivel_riesgo` (
  `id_nivel_riesgo` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(10) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_nivel_riesgo`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `norma_tipo_poste`
--

DROP TABLE IF EXISTS `norma_tipo_poste`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `norma_tipo_poste` (
  `id_norma_tipo_poste` int(11) NOT NULL AUTO_INCREMENT,
  `id_tipo_poste` int(11) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_norma_tipo_poste`),
  KEY `fk_norma_tipo_poste_tipo_poste` (`id_tipo_poste`),
  CONSTRAINT `fk_norma_tipo_poste_tipo_poste` FOREIGN KEY (`id_tipo_poste`) REFERENCES `tipo_poste` (`id_tipo_poste`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `operador_red_energia`
--

DROP TABLE IF EXISTS `operador_red_energia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operador_red_energia` (
  `id_operador_red_energia` int(11) NOT NULL AUTO_INCREMENT,
  `nit` bigint(20) unsigned NOT NULL,
  `dv` int(2) NOT NULL DEFAULT 0,
  `razon_social` varchar(120) NOT NULL,
  `direccion` varchar(120) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_operador_red_energia`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `periodo_mantenimiento`
--

DROP TABLE IF EXISTS `periodo_mantenimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `periodo_mantenimiento` (
  `id_periodo_mantenimiento` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `dias` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_periodo_mantenimiento`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `plan_trabajo`
--

DROP TABLE IF EXISTS `plan_trabajo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plan_trabajo` (
  `id_plan_trabajo` int(11) NOT NULL AUTO_INCREMENT,
  `id_cuadrilla` int(11) NOT NULL,
  `id_vehiculo` int(11) DEFAULT NULL,
  `id_tercero_responsable` int(11) NOT NULL,
  `id_tercero_autoriza` int(11) NOT NULL,
  `estado_plan_trabajo` enum('AC','AU','EE','PS','FZ','IA') NOT NULL DEFAULT 'AC' COMMENT 'AC:ACTIVO,AU:AUTORIZADO,EE:EN EJECUCION,PS:PAUSADO,FZ:FINALIZADO,IA:INACTIVO',
  `fch_inicio_plan_trabajo` date NOT NULL,
  `fch_finaliza_plan_trabajo` date DEFAULT NULL,
  `descripcion` text NOT NULL,
  `id_tercero_registra` int(11) NOT NULL,
  `fch_registro` datetime NOT NULL,
  `nombre_cuadrilla` varchar(100) NOT NULL COMMENT 'Nombre de la cuadrilla configurada, se agrega para mantener el historial en la planeacion',
  `id_municipio` int(11) NOT NULL,
  `hora_inicio_plan_trabajo` time DEFAULT NULL,
  `id_tipo_plan_trabajo` int(11) DEFAULT NULL,
  `id_tercero_actualiza` int(11) DEFAULT NULL,
  `fch_actualiza` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id_plan_trabajo`),
  KEY `fk_plan_trabajo_vehiculo` (`id_vehiculo`),
  KEY `fk_plan_trabajo_cuadrilla` (`id_cuadrilla`),
  KEY `fk_plan_trabajo_tercero_responsable` (`id_tercero_responsable`),
  KEY `fk_plan_trabajo_tercero_autoriza` (`id_tercero_autoriza`),
  KEY `fk_plan_trabajo_tercero_registra` (`id_tercero_registra`),
  KEY `fk_plan_trabajo_municipio` (`id_municipio`),
  KEY `fk_plan_trabajo_tipo_plan_trabajo_2` (`id_tipo_plan_trabajo`),
  KEY `fk_plan_trabajo_tercero_actualiza` (`id_tercero_actualiza`),
  CONSTRAINT `fk_plan_trabajo_cuadrilla` FOREIGN KEY (`id_cuadrilla`) REFERENCES `cuadrilla` (`id_cuadrilla`),
  CONSTRAINT `fk_plan_trabajo_municipio` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`),
  CONSTRAINT `fk_plan_trabajo_tercero_actualiza` FOREIGN KEY (`id_tercero_actualiza`) REFERENCES `tercero` (`id_tercero`),
  CONSTRAINT `fk_plan_trabajo_tercero_autoriza` FOREIGN KEY (`id_tercero_autoriza`) REFERENCES `tercero` (`id_tercero`),
  CONSTRAINT `fk_plan_trabajo_tercero_registra` FOREIGN KEY (`id_tercero_registra`) REFERENCES `tercero` (`id_tercero`),
  CONSTRAINT `fk_plan_trabajo_tercero_responsable` FOREIGN KEY (`id_tercero_responsable`) REFERENCES `tercero` (`id_tercero`),
  CONSTRAINT `fk_plan_trabajo_tipo_plan_trabajo_2` FOREIGN KEY (`id_tipo_plan_trabajo`) REFERENCES `tipo_plan_trabajo` (`id_tipo_plan_trabajo`),
  CONSTRAINT `fk_plan_trabajo_vehiculo` FOREIGN KEY (`id_vehiculo`) REFERENCES `vehiculo` (`id_vehiculo`)
) ENGINE=InnoDB AUTO_INCREMENT=242 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `plan_trabajo_tercero_cuadrilla`
--

DROP TABLE IF EXISTS `plan_trabajo_tercero_cuadrilla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plan_trabajo_tercero_cuadrilla` (
  `id_plan_trabajo` int(11) NOT NULL,
  `id_tercero` int(11) NOT NULL,
  PRIMARY KEY (`id_plan_trabajo`,`id_tercero`),
  KEY `fk_plan_trabajo_tercero_cuadrilla` (`id_tercero`),
  CONSTRAINT `fk_plan_trabajo_tercero_cuadrilla` FOREIGN KEY (`id_tercero`) REFERENCES `tercero` (`id_tercero`),
  CONSTRAINT `fk_plan_trabajo_tercero_cuadrilla_plan` FOREIGN KEY (`id_plan_trabajo`) REFERENCES `plan_trabajo` (`id_plan_trabajo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pqr`
--

DROP TABLE IF EXISTS `pqr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pqr` (
  `id_pqr` int(11) NOT NULL AUTO_INCREMENT,
  `id_municipio` int(11) NOT NULL,
  `id_tipo_pqr` int(11) NOT NULL,
  `id_tipo_reporte` int(11) NOT NULL,
  `id_medio_recepcion_pqr` int(11) NOT NULL,
  `id_usuario_servicio` int(11) DEFAULT NULL,
  `id_luminaria` int(11) DEFAULT NULL,
  `comentario` text NOT NULL,
  `id_tercero_registra` int(11) NOT NULL,
  `fch_registro` datetime NOT NULL,
  `fch_pqr` date NOT NULL,
  `id_estado_pqr` int(11) NOT NULL,
  `fch_cierre` datetime DEFAULT NULL,
  `id_tercero_cierra` int(11) DEFAULT NULL,
  `id_barrio_reporte` int(11) DEFAULT NULL,
  `direccion_reporte` varchar(80) DEFAULT NULL,
  `nombre_usuario_servicio` varchar(80) DEFAULT NULL,
  `direccion_usuario_servicio` varchar(80) DEFAULT NULL,
  `telefono_usuario_servicio` varchar(45) DEFAULT NULL,
  `hora_pqr` time DEFAULT NULL,
  `fch_actualiza` datetime DEFAULT NULL,
  `id_tercero_actualiza` int(11) DEFAULT NULL,
  `apoyo_no` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`id_pqr`),
  KEY `fk_pqr_municipio` (`id_municipio`),
  KEY `fk_pqr_tipo_pqr` (`id_tipo_pqr`),
  KEY `fk_pqr_tipo_reporte` (`id_tipo_reporte`),
  KEY `fk_pqr_medio_recepcion` (`id_medio_recepcion_pqr`),
  KEY `fk_pqr_luminaria` (`id_luminaria`),
  KEY `fk_pqr_tercero` (`id_tercero_registra`),
  KEY `fk_pqr_estado_pqr` (`id_estado_pqr`),
  KEY `fk_pqr_usuario_cierra` (`id_tercero_cierra`),
  KEY `fk_pqr_usuario_servicio` (`id_usuario_servicio`),
  KEY `fk_tecero_actualiza` (`id_tercero_actualiza`),
  CONSTRAINT `fk_pqr_estado_pqr` FOREIGN KEY (`id_estado_pqr`) REFERENCES `estado_pqr` (`id_estado_pqr`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pqr_luminaria` FOREIGN KEY (`id_luminaria`) REFERENCES `luminaria` (`id_luminaria`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pqr_medio_recepcion` FOREIGN KEY (`id_medio_recepcion_pqr`) REFERENCES `medio_recepcion_pqr` (`id_medio_recepcion_pqr`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pqr_municipio` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pqr_tercero` FOREIGN KEY (`id_tercero_registra`) REFERENCES `tercero` (`id_tercero`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pqr_tipo_pqr` FOREIGN KEY (`id_tipo_pqr`) REFERENCES `tipo_pqr` (`id_tipo_pqr`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pqr_tipo_reporte` FOREIGN KEY (`id_tipo_reporte`) REFERENCES `tipo_reporte` (`id_tipo_reporte`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pqr_usuario_cierra` FOREIGN KEY (`id_tercero_cierra`) REFERENCES `tercero` (`id_tercero`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pqr_usuario_servicio` FOREIGN KEY (`id_usuario_servicio`) REFERENCES `usuario_servicio` (`id_usuario_servicio`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_tecero_actualiza` FOREIGN KEY (`id_tercero_actualiza`) REFERENCES `tercero` (`id_tercero`)
) ENGINE=InnoDB AUTO_INCREMENT=53791 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proceso`
--

DROP TABLE IF EXISTS `proceso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `proceso` (
  `id_proceso` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `id_empresa` int(11) DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_proceso`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `proceso_ibfk_1` FOREIGN KEY (`id_empresa`) REFERENCES `empresa` (`id_empresa`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `propiedad_transformador`
--

DROP TABLE IF EXISTS `propiedad_transformador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `propiedad_transformador` (
  `id_propiedad_transformador` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_propiedad_transformador`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sede`
--

DROP TABLE IF EXISTS `sede`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sede` (
  `id_sede` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `id_empresa` int(11) DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_sede`),
  KEY `id_empresa` (`id_empresa`),
  CONSTRAINT `sede_ibfk_1` FOREIGN KEY (`id_empresa`) REFERENCES `empresa` (`id_empresa`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tabla_tmp`
--

DROP TABLE IF EXISTS `tabla_tmp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabla_tmp` (
  `FECHA_DE_RECLAMO` varchar(50) DEFAULT NULL,
  `FECHA_DE_REVISION` varchar(50) DEFAULT NULL,
  `MUNICIPIO` varchar(50) DEFAULT NULL,
  `ID_MUNICIPIO` int(11) DEFAULT NULL,
  `BARRIO` varchar(50) DEFAULT NULL,
  `DIRECCION` varchar(50) DEFAULT NULL,
  `OBSERVACION` varchar(50) DEFAULT NULL,
  `DESCRIPCION` varchar(50) DEFAULT NULL,
  `COD_LUMINARIA` varchar(50) DEFAULT NULL,
  `POSTE` varchar(50) DEFAULT NULL,
  `TECNICO` varchar(50) DEFAULT NULL,
  `POTENCIA` int(11) DEFAULT NULL,
  `ID_BARRIO` bigint(20) unsigned DEFAULT NULL,
  `ID_LUMINARIA` bigint(20) unsigned DEFAULT NULL,
  `ID_TERCERO` bigint(20) unsigned DEFAULT NULL,
  `procesado` enum('S','N') NOT NULL DEFAULT 'S'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tercero`
--

DROP TABLE IF EXISTS `tercero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tercero` (
  `id_tercero` int(11) NOT NULL AUTO_INCREMENT,
  `id_tipo_identificacion` int(11) NOT NULL,
  `identificacion` varchar(45) NOT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `apellido` varchar(45) DEFAULT NULL,
  `direccion` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `telefono` varchar(45) DEFAULT NULL,
  `id_municipio` int(11) NOT NULL,
  `razon_social` varchar(45) DEFAULT NULL,
  `es_cliente` enum('S','N') NOT NULL DEFAULT 'N',
  `es_proveedor` enum('S','N') NOT NULL DEFAULT 'N',
  `es_empleado` enum('S','N') NOT NULL DEFAULT 'S',
  `es_usuario` enum('S','N') NOT NULL DEFAULT 'N',
  `clave` varchar(45) DEFAULT NULL,
  `usuario` varchar(45) DEFAULT NULL,
  `id_tercero_registra` int(11) DEFAULT NULL,
  `fch_registro` datetime NOT NULL,
  `ejecuta_labor_tecnica` enum('S','N') NOT NULL DEFAULT 'N',
  `super_usuario` enum('S','N') NOT NULL DEFAULT 'N',
  `tipo_foto` varchar(45) DEFAULT NULL,
  `tamano_foto` int(11) DEFAULT NULL,
  `extension_foto` varchar(45) DEFAULT NULL,
  `nombre_foto` varchar(45) DEFAULT NULL,
  `foto` blob DEFAULT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_tercero`),
  UNIQUE KEY `fk_tercero_usuario` (`usuario`),
  KEY `fk_tercero_tipo_identificacion_idx` (`id_tipo_identificacion`),
  KEY `fk_tercero_muniicipio_idx` (`id_municipio`),
  KEY `fk_tercero_tercero_idx` (`id_tercero_registra`),
  CONSTRAINT `fk_tercero_muniicipio` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`),
  CONSTRAINT `fk_tercero_tipo_identificacion` FOREIGN KEY (`id_tipo_identificacion`) REFERENCES `tipo_identificacion` (`id_tipo_identificacion`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_actividad`
--

DROP TABLE IF EXISTS `tipo_actividad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_actividad` (
  `id_tipo_actividad` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `instalacion` enum('S','N') NOT NULL DEFAULT 'N',
  `preventivo` enum('S','N') NOT NULL DEFAULT 'N',
  `correctivo` enum('S','N') NOT NULL DEFAULT 'N',
  `reubicacion` enum('S','N') NOT NULL DEFAULT 'N',
  `desmonte` enum('S','N') NOT NULL DEFAULT 'N',
  `codigo` varchar(12) DEFAULT NULL COMMENT 'codigo referencia de migracion',
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  `decripcion_a_ejecutar` text DEFAULT NULL,
  PRIMARY KEY (`id_tipo_actividad`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_apoyo`
--

DROP TABLE IF EXISTS `tipo_apoyo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_apoyo` (
  `id_tipo_apoyo` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_tipo_apoyo`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_brazo`
--

DROP TABLE IF EXISTS `tipo_brazo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_brazo` (
  `id_tipo_brazo` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_tipo_brazo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_contrato`
--

DROP TABLE IF EXISTS `tipo_contrato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_contrato` (
  `id_tipo_contrato` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_tipo_contrato`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_cuenta`
--

DROP TABLE IF EXISTS `tipo_cuenta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_cuenta` (
  `id_tipo_cuenta` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_tipo_cuenta`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_espacio`
--

DROP TABLE IF EXISTS `tipo_espacio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_espacio` (
  `id_tipo_espacio` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_tipo_espacio`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_identificacion`
--

DROP TABLE IF EXISTS `tipo_identificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_identificacion` (
  `id_tipo_identificacion` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `abreviatura` varchar(4) NOT NULL,
  PRIMARY KEY (`id_tipo_identificacion`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_luminaria`
--

DROP TABLE IF EXISTS `tipo_luminaria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_luminaria` (
  `id_tipo_luminaria` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `reactancia` decimal(9,4) NOT NULL DEFAULT 0.0000,
  `potencia` int(4) DEFAULT 0,
  `codigo` varchar(12) DEFAULT NULL COMMENT 'codigo referencia de migracion',
  `descripcion_corta` varchar(24) DEFAULT NULL COMMENT 'descripcion corta referencia de migracion',
  PRIMARY KEY (`id_tipo_luminaria`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_plan_trabajo`
--

DROP TABLE IF EXISTS `tipo_plan_trabajo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_plan_trabajo` (
  `id_tipo_plan_trabajo` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_tipo_plan_trabajo`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_poste`
--

DROP TABLE IF EXISTS `tipo_poste`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_poste` (
  `id_tipo_poste` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  `codigo` varchar(12) DEFAULT NULL COMMENT 'codigo referencia de migracion',
  PRIMARY KEY (`id_tipo_poste`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_pqr`
--

DROP TABLE IF EXISTS `tipo_pqr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_pqr` (
  `id_tipo_pqr` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `dias_vencimiento` int(3) NOT NULL DEFAULT 0,
  `estado` enum('A','I') NOT NULL,
  `incluido_en_calculo_nivel_eficiencia` enum('S','N') NOT NULL DEFAULT 'S',
  PRIMARY KEY (`id_tipo_pqr`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_red`
--

DROP TABLE IF EXISTS `tipo_red`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_red` (
  `id_tipo_red` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_tipo_red`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_reporte`
--

DROP TABLE IF EXISTS `tipo_reporte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_reporte` (
  `id_tipo_reporte` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `id_tipo_pqr` int(11) NOT NULL,
  `codigo` varchar(12) DEFAULT NULL COMMENT 'codigo referencia de migracion',
  PRIMARY KEY (`id_tipo_reporte`),
  KEY `tipo_reporte_tipo_pqr_FK` (`id_tipo_pqr`),
  CONSTRAINT `tipo_reporte_tipo_pqr_FK` FOREIGN KEY (`id_tipo_pqr`) REFERENCES `tipo_pqr` (`id_tipo_pqr`)
) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_retenida`
--

DROP TABLE IF EXISTS `tipo_retenida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_retenida` (
  `id_tipo_retenida` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_tipo_retenida`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipo_vivienda`
--

DROP TABLE IF EXISTS `tipo_vivienda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipo_vivienda` (
  `id_tipo_vivienda` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` char(1) DEFAULT 'A' COMMENT 'A=Activo, I=Inactivo',
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id_tipo_vivienda`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unidad_medida`
--

DROP TABLE IF EXISTS `unidad_medida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unidad_medida` (
  `id_unidad_medida` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(100) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  PRIMARY KEY (`id_unidad_medida`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuario_servicio`
--

DROP TABLE IF EXISTS `usuario_servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuario_servicio` (
  `id_usuario_servicio` int(11) NOT NULL AUTO_INCREMENT,
  `id_tipo_identificacion` int(11) NOT NULL,
  `identificacion` int(11) NOT NULL,
  `digito_verificacion` tinyint(1) NOT NULL DEFAULT 0,
  `nombre` varchar(80) NOT NULL,
  `id_municipio` int(11) NOT NULL,
  `direccion` varchar(80) NOT NULL,
  `telefono` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `id_tercero_registra` int(11) DEFAULT NULL,
  `fch_registro` datetime DEFAULT NULL,
  PRIMARY KEY (`id_usuario_servicio`),
  UNIQUE KEY `identificacion_UNIQUE` (`identificacion`),
  KEY `fk_usuario_servicio_tipo_identificacion` (`id_tipo_identificacion`),
  KEY `fk_usuario_servicio_municipio` (`id_municipio`),
  CONSTRAINT `fk_usuario_servicio_municipio` FOREIGN KEY (`id_municipio`) REFERENCES `municipio` (`id_municipio`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuario_servicio_tipo_identificacion` FOREIGN KEY (`id_tipo_identificacion`) REFERENCES `tipo_identificacion` (`id_tipo_identificacion`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vehiculo`
--

DROP TABLE IF EXISTS `vehiculo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vehiculo` (
  `id_vehiculo` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(45) NOT NULL,
  `estado` enum('A','I') NOT NULL DEFAULT 'A',
  `placa` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`id_vehiculo`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-27 20:15:47
