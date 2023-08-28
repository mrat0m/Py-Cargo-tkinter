DROP DATABASE IF EXISTS cargo_database;

CREATE DATABASE `cargo_database`;

USE `cargo_database`;

/*Table structure for table `bookings` */

DROP TABLE IF EXISTS `bookings`;

CREATE TABLE `bookings` (
  `booking_id` int(50) NOT NULL AUTO_INCREMENT,
  `customer_id` int(50) DEFAULT NULL,
  `booking_date` varchar(50) DEFAULT NULL,
  `from_loc` varchar(50) DEFAULT NULL,
  `toloc` varchar(50) DEFAULT NULL,
  `weight` varchar(50) DEFAULT NULL,
  `length` varchar(50) DEFAULT NULL,
  `width` varchar(50) DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  `booking_status` varchar(50) DEFAULT NULL,
  `pack_id` int(50) DEFAULT NULL,
  PRIMARY KEY (`booking_id`)
) AUTO_INCREMENT=1000 DEFAULT CHARSET=latin1;

/*Data for the table `bookings` */
insert  into `bookings`(`booking_id`,`customer_id`,`booking_date`,`from_loc`,`toloc`,`weight`,`length`,`width`,`amount`,`booking_status`,`pack_id`) values (1000,100,'2023-07-21','Kochi','Thevara','10','100','100','20000','collected',3000);

/*Table structure for table `cargo_status` */

DROP TABLE IF EXISTS `cargo_status`;

CREATE TABLE `cargo_status` (
  `status_id` int(50) NOT NULL AUTO_INCREMENT,
  `booking_id` int(50) DEFAULT NULL,
  `place_name` varchar(50) DEFAULT NULL,
  `status_date_time` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`status_id`)
) AUTO_INCREMENT=2000 DEFAULT CHARSET=latin1;

/*Data for the table `cargo_status` */

insert  into `cargo_status`(`status_id`,`booking_id`,`place_name`,`status_date_time`) values (2000,1000,'Kochi','2023-07-21 18:00:48');

/*Table structure for table `customers` */

DROP TABLE IF EXISTS `customers`;

CREATE TABLE `customers` (
  `customer_id` int(50) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) AUTO_INCREMENT=100 DEFAULT CHARSET=latin1;

/*Data for the table `customers` */

insert  into `customers`(`customer_id`,`username`,`first_name`,`last_name`,`phone`,`email`) values (100,'tonystark','Tony','Stark','9876543210','tony@stark.com');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `user_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`username`)
) DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`username`,`password`,`user_type`) values ('admin','admin','admin'),('tonystark','tonyst@rk123','customer');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(50) NOT NULL AUTO_INCREMENT,
  `booking_id` int(50) DEFAULT NULL,
  `amount_paid` varchar(50) DEFAULT NULL,
  `payment_date` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) AUTO_INCREMENT=5000 DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

insert  into `payment`(`payment_id`,`booking_id`,`amount_paid`,`payment_date`) values (5000,1000,'20000','2022-03-21 17:54:37');

/*Table structure for table `packages` */

DROP TABLE IF EXISTS `packages`;

CREATE TABLE `packages` (
  `pack_id` int(50) NOT NULL AUTO_INCREMENT,
  `packname` varchar(50) DEFAULT NULL,
  `maximum_weight` varchar(50) DEFAULT NULL,
  `maximum_height` varchar(50) DEFAULT NULL,
  `maximum_width` varchar(50) DEFAULT NULL,
  `minimum_price` varchar(50) DEFAULT NULL,
  `pstatus` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`pack_id`)
) AUTO_INCREMENT=3000 DEFAULT CHARSET=latin1;

/*Data for the table `packages` */

insert  into `packages`(`pack_id`,`packname`,`maximum_weight`,`maximum_height`,`maximum_width`,`minimum_price`,`pstatus`) values (3000,'Premium','25','100','100','20000','active');