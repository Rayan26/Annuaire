CREATE TABLE `user` (
  `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `email` varchar(250) NOT NULL,
  `password` varchar(250) NOT NULL,
  `name` varchar(250) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `role` varchar(250) NOT NULL,
  `job` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `user` (`email`, `password`, `name`, `phone`, `id`, `role`, `job`, `location`) VALUES
('admin', 'sha256$BWBUtpBRxAY31zyV$05340c4597426bb65ad2502701c8b49175829d32e6262d2d1461556a1839b318', 'admin', '0677896578', 20, 'ADMIN', 'Administrator', '12 Avenue Luminy');