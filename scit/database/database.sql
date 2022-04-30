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
(1, 'Apple 13 Pro', 'App13P', 'images/Apple_13_pro.jpg', 4000.00),
(2, 'Realme 7 Pro', 'REA07P', 'images/Realme_7_pro.jpg', 2100.00),
(3, 'Samsung A32', 'SAMA32', 'images/Samsung_A32.jpg', 2500.00),
(4, 'Xiaomi MI 11T', 'XIA11T', 'images/Xiaomi_Mi_11T.jpg', 2300.00),
(5, 'Xiaomi READMI 10S', 'XIA10S', 'images/Xiaomi_readmi_10S.jpg', 1800.00);
