-- MySQL dump 10.13  Distrib 8.0.24, for macos11 (x86_64)
--
-- Host: localhost    Database: el_gran_poeta
-- ------------------------------------------------------
-- Server version	8.0.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `BODEGAS`
--

DROP TABLE IF EXISTS `BODEGAS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `BODEGAS` (
  `id_bodega` int NOT NULL AUTO_INCREMENT,
  `nombre_bodega` varchar(100) NOT NULL,
  PRIMARY KEY (`id_bodega`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BODEGAS`
--

LOCK TABLES `BODEGAS` WRITE;
/*!40000 ALTER TABLE `BODEGAS` DISABLE KEYS */;
INSERT INTO `BODEGAS` VALUES (1,'Sucursal Mall Curico '),(2,'Sucursal central');
/*!40000 ALTER TABLE `BODEGAS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EDITORIALES`
--

DROP TABLE IF EXISTS `EDITORIALES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EDITORIALES` (
  `id_editorial` int NOT NULL AUTO_INCREMENT,
  `nombre_editorial` varchar(100) NOT NULL,
  PRIMARY KEY (`id_editorial`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EDITORIALES`
--

LOCK TABLES `EDITORIALES` WRITE;
/*!40000 ALTER TABLE `EDITORIALES` DISABLE KEYS */;
INSERT INTO `EDITORIALES` VALUES (1,'Seix Barral'),(2,'Grupo Planeta'),(3,'Penguin Random House'),(4,'HarperCollins'),(5,'Anagrama'),(6,'LOM Ediciones'),(7,'Hueders'),(8,'Editorial Forja'),(9,'Editorial Zig.Zag'),(10,'Sudamericana'),(11,'Debolsillo'),(12,'Minotauro'),(13,'National Geographics Partners'),(14,'Zinet Media Group'),(15,'Time USA, LLC'),(16,'Conde Nast'),(17,'Editorial Oceano de Chile'),(18,'La Tercera'),(19,'Santillana'),(20,'Espasa'),(21,'Salvat Editores');
/*!40000 ALTER TABLE `EDITORIALES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `INVENTARIO`
--

DROP TABLE IF EXISTS `INVENTARIO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `INVENTARIO` (
  `id_inventario` int NOT NULL AUTO_INCREMENT,
  `id_bodega` int DEFAULT NULL,
  `id_producto` int DEFAULT NULL,
  `cantidad` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_inventario`),
  KEY `id_bodega` (`id_bodega`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`id_bodega`) REFERENCES `BODEGAS` (`id_bodega`),
  CONSTRAINT `inventario_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `PRODUCTOS` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `INVENTARIO`
--

LOCK TABLES `INVENTARIO` WRITE;
/*!40000 ALTER TABLE `INVENTARIO` DISABLE KEYS */;
INSERT INTO `INVENTARIO` VALUES (1,1,1,240),(2,2,1,100);
/*!40000 ALTER TABLE `INVENTARIO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MOVIMIENTOS`
--

DROP TABLE IF EXISTS `MOVIMIENTOS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MOVIMIENTOS` (
  `id_movimiento` int NOT NULL AUTO_INCREMENT,
  `fecha_movimiento` datetime DEFAULT CURRENT_TIMESTAMP,
  `id_usuario` int DEFAULT NULL,
  `bodega_origen` int DEFAULT NULL,
  `bodega_destino` int DEFAULT NULL,
  `id_producto` int DEFAULT NULL,
  `cantidad` int NOT NULL,
  PRIMARY KEY (`id_movimiento`),
  KEY `id_usuario` (`id_usuario`),
  KEY `bodega_origen` (`bodega_origen`),
  KEY `bodega_destino` (`bodega_destino`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `movimientos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `USUARIOS` (`id_usuario`),
  CONSTRAINT `movimientos_ibfk_2` FOREIGN KEY (`bodega_origen`) REFERENCES `BODEGAS` (`id_bodega`),
  CONSTRAINT `movimientos_ibfk_3` FOREIGN KEY (`bodega_destino`) REFERENCES `BODEGAS` (`id_bodega`),
  CONSTRAINT `movimientos_ibfk_4` FOREIGN KEY (`id_producto`) REFERENCES `PRODUCTOS` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MOVIMIENTOS`
--

LOCK TABLES `MOVIMIENTOS` WRITE;
/*!40000 ALTER TABLE `MOVIMIENTOS` DISABLE KEYS */;
INSERT INTO `MOVIMIENTOS` VALUES (1,'2026-06-17 01:50:10',1,NULL,1,1,100),(2,'2026-06-17 01:50:34',1,1,2,1,54),(3,'2026-06-17 01:55:26',1,NULL,2,1,40),(4,'2026-06-17 01:55:40',1,2,1,1,20),(5,'2026-06-17 15:55:22',2,NULL,2,1,23),(6,'2026-06-17 15:55:32',2,2,1,1,20),(7,'2026-06-17 20:26:19',2,NULL,2,1,23),(8,'2026-06-17 20:26:29',2,2,1,1,14),(9,'2026-06-17 21:17:30',2,NULL,2,1,14),(10,'2026-06-17 21:17:50',2,2,1,1,100),(11,'2026-06-17 21:19:38',2,NULL,2,1,140),(12,'2026-06-17 21:19:58',2,2,1,1,40);
/*!40000 ALTER TABLE `MOVIMIENTOS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PERFILES`
--

DROP TABLE IF EXISTS `PERFILES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PERFILES` (
  `id_perfil` int NOT NULL AUTO_INCREMENT,
  `nombre_perfil` varchar(50) NOT NULL,
  PRIMARY KEY (`id_perfil`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PERFILES`
--

LOCK TABLES `PERFILES` WRITE;
/*!40000 ALTER TABLE `PERFILES` DISABLE KEYS */;
INSERT INTO `PERFILES` VALUES (1,'Jefe de Bodega'),(2,'Bodeguero');
/*!40000 ALTER TABLE `PERFILES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PRODUCTOS`
--

DROP TABLE IF EXISTS `PRODUCTOS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PRODUCTOS` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `autor` varchar(100) DEFAULT NULL,
  `tipo_producto` varchar(50) DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `id_editorial` int DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  KEY `id_editorial` (`id_editorial`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_editorial`) REFERENCES `EDITORIALES` (`id_editorial`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PRODUCTOS`
--

LOCK TABLES `PRODUCTOS` WRITE;
/*!40000 ALTER TABLE `PRODUCTOS` DISABLE KEYS */;
INSERT INTO `PRODUCTOS` VALUES (1,'El Sol y sus flores','Rupi Kaur','Libro','Recopilacion de poemas',1),(2,'Cien años de soledad','Gabriel Garcia Marquez','Libro','La obra cumbre del realismo magico que narra la historia de la familia Buendia a lo largo de siete generaciones en el pueblo ficticio de Macondo',3),(3,'1984','George Orwell','Libro','Sigue a Winston Smith, un hombre que intenta pensar por si mismo y revelarse contra un gobierno totalitario que vigila y controla todo.',11),(4,'El Principito','Antoine de Saint-Exupery','Libro','Narra el encuentro en el desierto entre un aviador y un niño de otro planeta que le enseña lecciones sobre el amor, la amistad y la adultez.',9),(5,'El Señor de los Anillos: La Comunidad del Anillo','J.R.R. Tolkien','Libro','Un grupo de heroes emprende un peligroso viaje epico para destruir un anillo magico y evitar que el malvado Señor Oscuro domine el mundo.',12),(6,'National Geographic','Equipo editorial','Revista','Muestra reportajes fotograficos en profundidad sobre la vida animal, la naturaleza, los descubrimientos cientificos y las culturas del mundo.',13),(7,'Muy Interesante (Edicion Cono Sur)','Zinet Media Group','Revista','Explica de forma sencilla y entretenida curiosidades sobre la ciencia, salud, historia, avances tecnologicos y el universo.',14),(8,'TIME','Equipo periodistico ','Revista','Analiza los eventos y noticias mas importantes de la semana sobre politica internacional, economia, sociedad y personajes influyentes.',15),(9,'Wired','Equipo editorial','Revista','Explora como las nuevas tecnologias, la ciencia, la informatica y la innovacion digital estan transformando la cultura y el futuro.',16),(10,'Vogue Latinoamerica','Equipo editorial','Revista','Presenta las ultimas colecciones de alta costura, tendencia de moda, consejos de belleza y reportajes sobre figuras del espectaculo.',16),(11,'Diccionario Enciclopedico Universal Oceano','Equipo editorial Oceano','Enciclopedia','Define conceptos de la A a la Z y abarca conocimientos generales resumidos sobre la historia, geografia, ciencia, literatura y arte.',17),(12,'Enciclopedia Estudiantil Icarito','Equipo editorial e historiadores chilenos','Enciclopedia','Recopila informacion detallada sobre la historia de Chile, la geografia nacional, las ciencias naturales y la educacion civica.',18),(13,'Enciclopedia Escolar Visual','Equipo educativo','Enciclopedia','Explica materias escolares basicas como biologia, fisica y matematicas mediante infografias, esquemas y muchas imagenes ilustrativas.',19),(14,'Enciclopedia Universal Ilustrada Europeo-Americana','Varios autores','Enciclopedia','Detalla de manera sumamente extensa biografias, hechos historicos, descubrimientos y conceptos complejos en todas las ramas del saber humano.',20),(15,'Enciclopedia Salvat','Colaboradores expertos','Enciclopedia','Ofrece resumenes, explicaciones alfabeticas y datos estadisticos de temas universales, desde la flora y fauna hasta hitos tecnologicos.',21);
/*!40000 ALTER TABLE `PRODUCTOS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USUARIOS`
--

DROP TABLE IF EXISTS `USUARIOS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USUARIOS` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `id_perfil` int DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `username` (`username`),
  KEY `id_perfil` (`id_perfil`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_perfil`) REFERENCES `PERFILES` (`id_perfil`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USUARIOS`
--

LOCK TABLES `USUARIOS` WRITE;
/*!40000 ALTER TABLE `USUARIOS` DISABLE KEYS */;
INSERT INTO `USUARIOS` VALUES (1,'Pedro','1234',1),(2,'Benjamin','1234',2),(3,'Antonio','1234',2),(4,'Admin','1234',1);
/*!40000 ALTER TABLE `USUARIOS` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-08  0:04:44
