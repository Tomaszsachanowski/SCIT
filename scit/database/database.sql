CREATE DATABASE shopingdatabase;
use shopingdatabase;

CREATE TABLE `product` (
	`id` int unsigned COLLATE utf8mb4_unicode_ci NOT NULL AUTO_INCREMENT,
	`name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
	`code` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
	`image` text COLLATE utf8mb4_unicode_ci NOT NULL,
	`price` double COLLATE utf8mb4_unicode_ci NOT NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

INSERT INTO `product` (`id`, `name`, `code`, `image`, `price`) VALUES
(1, 'IPhone 12', 'IP12', 'Iphone_12.jpeg', 45000.00),
(2, 'IPhone 13 Pro', 'IP13P', 'Iphone_13Pro.jpeg', 5800.00),
(3, 'Realme 6', 'REA5', 'Realme_6.jpeg', 1200.00),
(4, 'Realme X2', 'REAX2', 'Realme_X2.jpeg', 21000.00),
(5, 'Redmi 9', 'RED8', 'Redmi_9.jpeg', 800.00),
(6, 'Redmi 10', 'RED10', 'Redmi_10.jpeg', 1300.00),
(7, 'Samsun J7', 'SJ7', 'Samsung_J7.jpeg', 2200.00),
(8, 'Samsung S10', 'S10', 'Samsung_S10.jpeg', 1800.00);
