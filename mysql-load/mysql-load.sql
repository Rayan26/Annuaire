CREATE TABLE `user` (
  `email` varchar(250) NOT NULL,
  `password` varchar(250) NOT NULL,
  `name` varchar(250) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `id` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `role` varchar(250) NOT NULL,
  `job` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `user` (`email`, `password`, `name`, `phone`, `id`, `role`, `job`, `location`) VALUES
('z@z', 'sha256$WhyJUrGfwoNxPFNr$99c886a30b4c65ba4e16c684d10609104e9ba4a352acb601d59a0033be2a2f48', 'zzz', '0909999', 11, 'ADMIN', 'Student', '12 Avenue Luminy'),
('a@a', 'sha256$vawe6t0whLUHMD3K$2168d74e518c518657a98b256ae1aca8c01f2e4f60c88b45666f03a2504bf4aa', 'aaaa', 'aaa', 12, 'ADMIN', 'aaa', 'aaa'),
('q@q', 'sha256$Og7S9IUrsh2nIeul$9850fd65f151930091e0e87cce1d8a7d7f5e0e59f20eaff7a7b3170caed86c91', 'qqqq', 'qqqq', 14, 'USER', 'qqqq', 'qqqq'),
('tt@tt', 'sha256$32s8GfDCf0J2Wmaz$2689a1cff630dcf3de91b14e5a6ba6696b32d0c33b58cd94f7e9b8f1b32ce65c', 'ttt', '00000', 15, 'USER', 'ttt', 'ttt'),
('dd@dd', 'sha256$ELNdMPh41yIWybqu$f33f3476a09bd24ba08c7cfecc8bba16ffda3315c6ee07981fbc9dd533fdec79', 'dddd', '0909999', 18, 'ADMIN', 'Enginer', '12 Avenue Luminy'),
('kallabrayan@gmail.com', 'sha256$BWBUtpBRxAY31zyV$05340c4597426bb65ad2502701c8b49175829d32e6262d2d1461556a1839b318', 'Rayan', '0677896578', 20, 'ADMIN', 'Student', '12 Avenue Luminy'),
('somone@yahoo.com', 'sha256$xONSGnVJNa3Ur6Y8$9ed8f69044f31f033e609757bbc541c52b7d42727fc04e7d00f2656acfe7a8eb', 'MyTube', '0688896668', 21, 'USER', 'Administator', '66 Pl Av des Hommes'),
('r@r', 'sha256$Xze3lXlyDML1c1t2$3e7f6a0f3c719c95cfaa1197a8702a0f7e2b65f59434c37fb4f2e950ac5f26a3', 'rrr', 'rrr', 22, 'ADMIN', 'rrr', 'rrr'),
('user@gmail.com', 'sha256$BWBUtpBRxAY31zyV$05340c4597426bb65ad2502701c8b49175829d32e6262d2d1461556a1839b318', 'user', '0688896668', 23, 'USER', 'uSER', '66 Pl Av des Hommes'),
('qq@qq', 'sha256$6NJsQ18e6QCkVU40$75a971cac5e56b9b9bb2c629620a958b124399ea64db7d09990aed16f6a3f9de', 'qq', '0677896578', 24, 'ADMIN', 'Enginer', 'qqqq'),
('dddd@f', 'sha256$wFMhLOYhIi8UFoYu$4cd9f3e7924eb41ae14c851fd196a2c42a2e8873819271949f8f7348f5385476', 'Rayan', '0677896578', 25, 'USER', 'Enginer', '12 Avenue Luminy');