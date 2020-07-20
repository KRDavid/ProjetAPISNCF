-- Request for table importation
-- Author : Nicolas Campion
-- Date 20/07/2020

-- WARNING :
-- - Tables 'distance', 'region', and 'trajet' requests must be executed first
-- - Execute one request once

-- vacances.distance definition

CREATE TABLE `distance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cumul_duree` int(11) DEFAULT NULL,
  `co2_emission` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- vacances.region definition

CREATE TABLE `region` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `label` varchar(100) DEFAULT NULL,
  `coord` varchar(100) DEFAULT NULL,
  `insee` int(11) DEFAULT NULL,
  `zip_code` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- vacances.trajet definition

CREATE TABLE `trajet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `inseedepart` int(11) DEFAULT NULL,
  `inseearrivee` int(11) DEFAULT NULL,
  `duree` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- vacances.distance_trajet definition

CREATE TABLE `distance_trajet` (
  `id_distance` int(11) DEFAULT NULL,
  `id_trajet` int(11) DEFAULT NULL,
  KEY `distance_trajet_fk` (`id_distance`),
  KEY `distance_trajet_fk_1` (`id_trajet`),
  CONSTRAINT `distance_trajet_fk` FOREIGN KEY (`id_distance`) REFERENCES `distance` (`id`),
  CONSTRAINT `distance_trajet_fk_1` FOREIGN KEY (`id_trajet`) REFERENCES `trajet` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- vacances.`pt-date-time` definition

CREATE TABLE `pt-date-time` (
  `id` int(11) NOT NULL,
  `departure_date_time` datetime DEFAULT NULL,
  `arrival_date_time` datetime DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `id_trajet` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `pt_date_time_fk` FOREIGN KEY (`id`) REFERENCES `trajet` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- vacances.trajet_region definition

CREATE TABLE `trajet_region` (
  `id_trajet` int(11) DEFAULT NULL,
  `id_region` int(11) DEFAULT NULL,
  KEY `trajet_region_fk` (`id_trajet`),
  KEY `trajet_region_fk_1` (`id_region`),
  CONSTRAINT `trajet_region_fk` FOREIGN KEY (`id_trajet`) REFERENCES `trajet` (`id`),
  CONSTRAINT `trajet_region_fk_1` FOREIGN KEY (`id_region`) REFERENCES `region` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;