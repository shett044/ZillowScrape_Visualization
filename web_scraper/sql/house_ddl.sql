-- --------------------------------------------------------
-- Host:                         csom-idsdl.oit.umn.edu
-- Server version:               5.6.17-log - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             8.3.0.4799
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping structure for table realestate.houses
DROP TABLE IF EXISTS `houses`;
CREATE TABLE IF NOT EXISTS `houses` (
  `zpid` int(11) NOT NULL,
  `longitude` int(11) DEFAULT NULL,
  `latitude` int(11) DEFAULT NULL,
  `link` varchar(200) CHARACTER SET latin1 DEFAULT NULL,
  `zestimate` int(11) DEFAULT NULL,
  `soldprice` int(11) DEFAULT NULL,
  `soldon` date DEFAULT NULL,
  `address` varchar(60) CHARACTER SET latin1 DEFAULT NULL,
  `beds` int(11) DEFAULT NULL,
  `baths` float DEFAULT NULL,
  `sqft` int(11) DEFAULT NULL,
  `built` int(11) DEFAULT NULL,
  `lot` float DEFAULT NULL,
  `capture_date` datetime DEFAULT NULL,
  PRIMARY KEY (`zpid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
