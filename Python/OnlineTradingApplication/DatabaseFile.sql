-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 05, 2024 at 05:30 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
--Database: `automatedtradingapp`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `account_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `account_type` enum('Cash','Margin') DEFAULT 'Cash',
  `leverage` decimal(5,2) DEFAULT 1.00,
  `balance` decimal(15,2) DEFAULT 0.00,
  `equity` decimal(15,2) DEFAULT 0.00,
  `risk_limit` decimal(15,2) DEFAULT 10000.00,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`account_id`, `user_id`, `account_type`, `leverage`, `balance`, `equity`, `risk_limit`, `created_at`) VALUES
(1, 1, 'Cash', 1.00, 1100.00, 0.00, 10000.00, '2024-10-02 13:31:24');

-- --------------------------------------------------------

--
-- Table structure for table `apikeys`
--

CREATE TABLE `apikeys` (
  `api_key_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `platform_name` varchar(255) NOT NULL,
  `api_key` varchar(255) NOT NULL,
  `api_secret` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_rotated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `rotation_schedule` int(11) DEFAULT 90,
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `assets`
--

CREATE TABLE `assets` (
  `asset_id` int(11) NOT NULL,
  `asset_name` varchar(255) NOT NULL,
  `asset_symbol` varchar(20) NOT NULL,
  `asset_type` enum('Stock','Forex','Crypto') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `assets`
--

INSERT INTO `assets` (`asset_id`, `asset_name`, `asset_symbol`, `asset_type`) VALUES
(1, 'Company A', 'Non', 'Stock');

-- --------------------------------------------------------

--
-- Table structure for table `auditlogs`
--

CREATE TABLE `auditlogs` (
  `audit_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `action_type` enum('Login','Trade Submission','Trade Modification','Account Update','API Call') NOT NULL,
  `action_details` text NOT NULL,
  `performed_by` varchar(255) DEFAULT 'User',
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `ip_address` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `compliancerecords`
--

CREATE TABLE `compliancerecords` (
  `compliance_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `document_type` enum('Passport','ID Card','Driving License') NOT NULL,
  `document_number` varchar(255) NOT NULL,
  `submission_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `verification_status` enum('Pending','Verified','Rejected') DEFAULT 'Pending',
  `verified_by` varchar(255) DEFAULT NULL,
  `verification_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `failedlogins`
--

CREATE TABLE `failedlogins` (
  `failed_login_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `attempt_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `ip_address` varchar(50) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `margincalls`
--

CREATE TABLE `margincalls` (
  `margin_call_id` int(11) NOT NULL,
  `account_id` int(11) DEFAULT NULL,
  `margin_used` decimal(15,2) NOT NULL,
  `available_margin` decimal(15,2) NOT NULL,
  `margin_call_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `resolved` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `marketdata`
--

CREATE TABLE `marketdata` (
  `market_data_id` int(11) NOT NULL,
  `asset_id` int(11) DEFAULT NULL,
  `price` decimal(15,2) NOT NULL,
  `volume` decimal(15,2) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `notification_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `notification_type` enum('Email','SMS','Push') NOT NULL,
  `message` text NOT NULL,
  `sent_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_read` tinyint(1) DEFAULT 0,
  `alert_type` enum('Trade Executed','Price Alert','Margin Call','Account Update') DEFAULT NULL,
  `importance` enum('Low','Medium','High') DEFAULT 'Medium'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `passwordresetrequests`
--

CREATE TABLE `passwordresetrequests` (
  `request_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `reset_token` varchar(255) NOT NULL,
  `request_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `token_expiry` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `is_completed` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `riskmanagement`
--

CREATE TABLE `riskmanagement` (
  `risk_id` int(11) NOT NULL,
  `trade_id` int(11) DEFAULT NULL,
  `last_price` decimal(15,2) NOT NULL,
  `risk_level` enum('Low','Medium','High') DEFAULT 'Medium',
  `margin_call_triggered` tinyint(1) DEFAULT 0,
  `stop_loss_triggered` tinyint(1) DEFAULT 0,
  `take_profit_triggered` tinyint(1) DEFAULT 0,
  `last_check` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tradehistory`
--

CREATE TABLE `tradehistory` (
  `history_id` int(11) NOT NULL,
  `trade_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `asset_id` int(11) DEFAULT NULL,
  `trade_type` enum('Buy','Sell','Short') DEFAULT NULL,
  `trade_amount` decimal(15,2) DEFAULT NULL,
  `trade_price` decimal(15,2) DEFAULT NULL,
  `leverage` decimal(5,2) DEFAULT 1.00,
  `profit_loss` decimal(15,2) DEFAULT NULL,
  `open_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `close_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `duration` int(11) DEFAULT NULL,
  `market_condition` enum('Bullish','Bearish','Neutral') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `trades`
--

CREATE TABLE `trades` (
  `trade_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `account_id` int(11) DEFAULT NULL,
  `asset_id` int(11) DEFAULT NULL,
  `trade_type` enum('Buy','Sell','Short') NOT NULL,
  `order_type` enum('Market','Limit','Stop') NOT NULL,
  `trade_amount` decimal(15,2) NOT NULL,
  `trade_price` decimal(15,2) NOT NULL,
  `stop_loss` decimal(15,2) DEFAULT NULL,
  `take_profit` decimal(15,2) DEFAULT NULL,
  `leverage` decimal(5,2) DEFAULT 1.00,
  `trade_status` enum('Pending','Open','Closed') DEFAULT 'Pending',
  `open_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `close_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `profit_loss` decimal(15,2) DEFAULT 0.00,
  `margin_used` decimal(15,2) DEFAULT 0.00,
  `position_size` decimal(15,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `trades`
--

INSERT INTO `trades` (`trade_id`, `user_id`, `account_id`, `asset_id`, `trade_type`, `order_type`, `trade_amount`, `trade_price`, `stop_loss`, `take_profit`, `leverage`, `trade_status`, `open_time`, `close_time`, `profit_loss`, `margin_used`, `position_size`) VALUES
(6, 1, 1, 1, 'Buy', 'Market', 2.00, 94.52, NULL, NULL, NULL, 'Open', '2024-10-05 06:34:32', '2024-10-05 06:34:32', NULL, NULL, NULL),
(58, 1, NULL, 1, 'Sell', 'Market', 2.00, 64.20, NULL, NULL, NULL, 'Closed', '2024-10-05 08:14:17', '2024-10-05 02:44:17', -60.64, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `userpreferences`
--

CREATE TABLE `userpreferences` (
  `preference_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `notification_preference` enum('Email','SMS','Push') DEFAULT 'Email',
  `risk_tolerance` enum('Low','Medium','High') DEFAULT 'Medium',
  `default_trade_amount` decimal(15,2) DEFAULT 0.00,
  `default_stop_loss_percentage` decimal(5,2) DEFAULT 0.00,
  `default_take_profit_percentage` decimal(5,2) DEFAULT 0.00,
  `preferred_currency` varchar(10) DEFAULT 'USD',
  `preferred_asset_types` set('Stock','Forex','Crypto') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `two_factor_enabled` tinyint(1) DEFAULT 0,
  `phone_number` varchar(20) DEFAULT NULL,
  `registration_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` datetime DEFAULT current_timestamp(),
  `is_verified` tinyint(1) DEFAULT 0,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `postal_code` varchar(20) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `email`, `password_hash`, `two_factor_enabled`, `phone_number`, `registration_date`, `last_login`, `is_verified`, `first_name`, `last_name`, `address`, `city`, `country`, `postal_code`, `date_of_birth`) VALUES
(1, 'zalamayursinh45@gmail.com', '$2b$12$Q2sWjgNRucAzNXjl0Qa9P.v8ZdWL4vbGGa7REehSW91ULmDq1nlWm', 0, '8866159795', '2024-10-02 12:40:35', NULL, 1, 'Zala', 'Mayursinh', 'Sector 3', 'Gandhinagar', 'Gandhinagar ', '382110', '2024-10-03');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`account_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `apikeys`
--
ALTER TABLE `apikeys`
  ADD PRIMARY KEY (`api_key_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `assets`
--
ALTER TABLE `assets`
  ADD PRIMARY KEY (`asset_id`);

--
-- Indexes for table `auditlogs`
--
ALTER TABLE `auditlogs`
  ADD PRIMARY KEY (`audit_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `compliancerecords`
--
ALTER TABLE `compliancerecords`
  ADD PRIMARY KEY (`compliance_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `failedlogins`
--
ALTER TABLE `failedlogins`
  ADD PRIMARY KEY (`failed_login_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `margincalls`
--
ALTER TABLE `margincalls`
  ADD PRIMARY KEY (`margin_call_id`),
  ADD KEY `account_id` (`account_id`);

--
-- Indexes for table `marketdata`
--
ALTER TABLE `marketdata`
  ADD PRIMARY KEY (`market_data_id`),
  ADD KEY `asset_id` (`asset_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`notification_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `passwordresetrequests`
--
ALTER TABLE `passwordresetrequests`
  ADD PRIMARY KEY (`request_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `riskmanagement`
--
ALTER TABLE `riskmanagement`
  ADD PRIMARY KEY (`risk_id`),
  ADD KEY `trade_id` (`trade_id`);

--
-- Indexes for table `tradehistory`
--
ALTER TABLE `tradehistory`
  ADD PRIMARY KEY (`history_id`),
  ADD KEY `trade_id` (`trade_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `asset_id` (`asset_id`);

--
-- Indexes for table `trades`
--
ALTER TABLE `trades`
  ADD PRIMARY KEY (`trade_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `account_id` (`account_id`),
  ADD KEY `asset_id` (`asset_id`);

--
-- Indexes for table `userpreferences`
--
ALTER TABLE `userpreferences`
  ADD PRIMARY KEY (`preference_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `account_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `apikeys`
--
ALTER TABLE `apikeys`
  MODIFY `api_key_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `assets`
--
ALTER TABLE `assets`
  MODIFY `asset_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `auditlogs`
--
ALTER TABLE `auditlogs`
  MODIFY `audit_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `compliancerecords`
--
ALTER TABLE `compliancerecords`
  MODIFY `compliance_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `failedlogins`
--
ALTER TABLE `failedlogins`
  MODIFY `failed_login_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `margincalls`
--
ALTER TABLE `margincalls`
  MODIFY `margin_call_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `marketdata`
--
ALTER TABLE `marketdata`
  MODIFY `market_data_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `notification_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `passwordresetrequests`
--
ALTER TABLE `passwordresetrequests`
  MODIFY `request_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `riskmanagement`
--
ALTER TABLE `riskmanagement`
  MODIFY `risk_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tradehistory`
--
ALTER TABLE `tradehistory`
  MODIFY `history_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `trades`
--
ALTER TABLE `trades`
  MODIFY `trade_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;

--
-- AUTO_INCREMENT for table `userpreferences`
--
ALTER TABLE `userpreferences`
  MODIFY `preference_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accounts`
--
ALTER TABLE `accounts`
  ADD CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `apikeys`
--
ALTER TABLE `apikeys`
  ADD CONSTRAINT `apikeys_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `auditlogs`
--
ALTER TABLE `auditlogs`
  ADD CONSTRAINT `auditlogs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `compliancerecords`
--
ALTER TABLE `compliancerecords`
  ADD CONSTRAINT `compliancerecords_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `failedlogins`
--
ALTER TABLE `failedlogins`
  ADD CONSTRAINT `failedlogins_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `margincalls`
--
ALTER TABLE `margincalls`
  ADD CONSTRAINT `margincalls_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`) ON DELETE CASCADE;

--
-- Constraints for table `marketdata`
--
ALTER TABLE `marketdata`
  ADD CONSTRAINT `marketdata_ibfk_1` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`asset_id`);

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `passwordresetrequests`
--
ALTER TABLE `passwordresetrequests`
  ADD CONSTRAINT `passwordresetrequests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `riskmanagement`
--
ALTER TABLE `riskmanagement`
  ADD CONSTRAINT `riskmanagement_ibfk_1` FOREIGN KEY (`trade_id`) REFERENCES `trades` (`trade_id`) ON DELETE CASCADE;

--
-- Constraints for table `tradehistory`
--
ALTER TABLE `tradehistory`
  ADD CONSTRAINT `tradehistory_ibfk_1` FOREIGN KEY (`trade_id`) REFERENCES `trades` (`trade_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tradehistory_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tradehistory_ibfk_3` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`asset_id`);

--
-- Constraints for table `trades`
--
ALTER TABLE `trades`
  ADD CONSTRAINT `trades_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `trades_ibfk_2` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `trades_ibfk_3` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`asset_id`);

--
-- Constraints for table `userpreferences`
--
ALTER TABLE `userpreferences`
  ADD CONSTRAINT `userpreferences_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
