-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 16, 2023 at 01:12 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rubygym`
--

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE `client` (
  `client_id` int(11) NOT NULL,
  `client_fname` varchar(75) NOT NULL,
  `client_lname` varchar(75) NOT NULL,
  `client_phone` varchar(25) NOT NULL,
  `client_address` varchar(255) DEFAULT NULL,
  `client_email` varchar(100) DEFAULT NULL,
  `client_pwd` varchar(100) DEFAULT NULL,
  `client_subscription` enum('monthly','3 months','6 months','annually') NOT NULL DEFAULT 'monthly',
  `program` enum('self','group','private training') NOT NULL DEFAULT 'self',
  `client_regdate` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`client_id`, `client_fname`, `client_lname`, `client_phone`, `client_address`, `client_email`, `client_pwd`, `client_subscription`, `program`, `client_regdate`) VALUES
(6, 'Lizzy', 'Asa', '08123456789', '16 Gimpo lagos', 'lizzy@asa.com', 'pbkdf2:sha256:260000$urxtGClublQcH0sq$06875720727b729c95ce82322e890cb6b9e95574202bcca9c09a60d773eacd', '3 months', 'self', '2023-09-15 18:40:22'),
(7, 'Princess', 'Nwosu', '08123451189', '72 church busstop osun', 'princess@yahoo.com', 'pbkdf2:sha256:260000$SocrlHvm5IFCeKbD$acd5715d284fd9e431aba3cb370f4c2f8e82cd405c5d13cf84d8396f198c4d', 'annually', 'private training', '2023-09-15 18:42:20'),
(8, 'John', 'Oko', '08123456789', '15 johnson street lagos', 'john@oko.com', 'pbkdf2:sha256:260000$MW36KFnc2O31kUvR$8197a385b299640bc1e9742932fbb1280af8f5ac536d202a5d627f46759d9e', '6 months', 'group', '2023-09-15 18:42:39'),
(9, 'Mark', 'Essien', '08123409789', '7 pelican street lagos', 'markessien@yahoo.com', 'pbkdf2:sha256:600000$W5KsFWGvy4P44QAH$9486cfcc26730e584c49649822524d23b548b9627738d669848e747a81801c', 'monthly', '', '2023-09-15 21:43:08');

-- --------------------------------------------------------

--
-- Table structure for table `emergency_contact`
--

CREATE TABLE `emergency_contact` (
  `emcontact_id` int(11) NOT NULL,
  `em_fname` varchar(75) NOT NULL,
  `em_lname` varchar(75) NOT NULL,
  `em_phonenum` varchar(25) NOT NULL,
  `em_address` varchar(255) DEFAULT NULL,
  `clientID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `emergency_contact`
--

INSERT INTO `emergency_contact` (`emcontact_id`, `em_fname`, `em_lname`, `em_phonenum`, `em_address`, `clientID`) VALUES
(6, 'Jude', 'Miracle', '08234567890', '50 orange town ikeja', 6),
(7, 'Blessing', 'Nwosu', '0812345678', '72 church busstop osun', 7),
(8, 'Dexter', 'George', '08234567890', '50 blue street ikeja', 8),
(9, 'Bello', 'Jim', '08224567890', '7 pelican street lagos', 9);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`client_id`),
  ADD UNIQUE KEY `client_email` (`client_email`),
  ADD UNIQUE KEY `client_pwd` (`client_pwd`);

--
-- Indexes for table `emergency_contact`
--
ALTER TABLE `emergency_contact`
  ADD PRIMARY KEY (`emcontact_id`),
  ADD KEY `clientID` (`clientID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `client`
--
ALTER TABLE `client`
  MODIFY `client_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `emergency_contact`
--
ALTER TABLE `emergency_contact`
  MODIFY `emcontact_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `emergency_contact`
--
ALTER TABLE `emergency_contact`
  ADD CONSTRAINT `emergency_contact_ibfk_1` FOREIGN KEY (`clientID`) REFERENCES `client` (`client_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
