-- MySQL dump 10.13  Distrib 9.3.0, for macos15.2 (arm64)
--
-- Host: localhost    Database: SPT
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activities`
--

DROP TABLE IF EXISTS `activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` varchar(255) NOT NULL,
  `category` varchar(50) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `activities_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1268 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activities`
--

LOCK TABLES `activities` WRITE;
/*!40000 ALTER TABLE `activities` DISABLE KEYS */;
INSERT INTO `activities` VALUES (352,39,'Logged out of the system','logout','2025-05-31 12:05:42'),(353,39,'Logged in to the system','login','2025-05-31 12:06:20'),(356,39,'Downloaded file: p_final.pdf from task 56','file','2025-05-31 13:04:47'),(357,39,'Updated user role: testactivity (ID: 48)','user','2025-05-31 16:25:41'),(358,39,'Logged out of the system','logout','2025-06-01 08:47:49'),(359,39,'Logged in to the system','login','2025-06-01 08:49:21'),(360,39,'Deleted user: fatuma (ID: 38)','user','2025-06-01 09:11:40'),(361,39,'Updated user role: muazman (ID: 46)','user','2025-06-01 09:34:44'),(362,39,'Created new user: tes22 (test2@gmail.com)','user','2025-06-01 09:35:29'),(363,39,'Deleted user: tes22 (ID: 49)','user','2025-06-01 09:35:33'),(364,39,'Created new user: staffqcp2 (staff@gmail.com)','user','2025-06-01 09:38:46'),(365,39,'Deleted user: staffqcp2 (ID: 50)','user','2025-06-01 09:38:54'),(366,39,'Logged in to the system','login','2025-06-02 07:45:22'),(367,39,'Logged in to the system','login','2025-06-02 10:23:23'),(369,39,'Created new user: managerqcp (qcpmanager@gmail.com)','user','2025-06-02 11:17:40'),(370,NULL,'Registered new account','user','2025-06-02 12:06:49'),(371,39,'Updated profile: First name changed from \'Admin\' to \'sadmin\', Last name changed from \'QCP\' to \'cavin\', Username changed from \'adminqcp\' to \'Cavamina\'','profile','2025-06-02 12:17:15'),(372,39,'Updated profile: First name changed from \'sadmin\' to \'Admin\', Last name changed from \'cavin\' to \'Qcp\', Username changed from \'Cavamina\' to \'adminqcp\'','profile','2025-06-02 12:31:07'),(373,39,'Logged in to the system','login','2025-06-02 17:36:30'),(374,39,'Created new task: notification test (ID: 59) with 1 assignees','task','2025-06-02 17:39:55'),(375,39,'Created new task: notification test (ID: 64) with 1 assignees','task','2025-06-02 17:39:57'),(376,39,'Created new task: notification test (ID: 63) with 1 assignees','task','2025-06-02 17:39:57'),(377,39,'Created new task: notification test (ID: 60) with 1 assignees','task','2025-06-02 17:39:57'),(378,39,'Created new task: notification test (ID: 62) with 1 assignees','task','2025-06-02 17:39:58'),(379,39,'Created new task: notification test (ID: 61) with 1 assignees','task','2025-06-02 17:39:58'),(380,39,'Created new task: notification test (ID: 65) with 1 assignees','task','2025-06-02 17:40:04'),(381,39,'Created new task: notification test (ID: 66) with 1 assignees','task','2025-06-02 17:40:07'),(382,39,'Created new task: notification test (ID: 67) with 1 assignees','task','2025-06-02 17:40:07'),(383,39,'Created new task: notification test (ID: 70) with 1 assignees','task','2025-06-02 17:40:07'),(384,39,'Created new task: notification test (ID: 68) with 1 assignees','task','2025-06-02 17:40:08'),(385,39,'Created new task: notification test (ID: 69) with 1 assignees','task','2025-06-02 17:40:08'),(386,39,'Created new task: notification test (ID: 71) with 1 assignees','task','2025-06-02 17:40:14'),(387,39,'Created new task: notification test (ID: 73) with 1 assignees','task','2025-06-02 17:40:16'),(388,39,'Created new task: notification test (ID: 76) with 1 assignees','task','2025-06-02 17:40:16'),(389,39,'Created new task: notification test (ID: 74) with 1 assignees','task','2025-06-02 17:40:17'),(390,39,'Created new task: notification test (ID: 72) with 1 assignees','task','2025-06-02 17:40:17'),(391,39,'Created new task: notification test (ID: 75) with 1 assignees','task','2025-06-02 17:40:18'),(392,39,'Created new task: notification test (ID: 77) with 1 assignees','task','2025-06-02 17:40:24'),(393,39,'Created new task: notification test (ID: 80) with 1 assignees','task','2025-06-02 17:40:26'),(394,39,'Created new task: notification test (ID: 79) with 1 assignees','task','2025-06-02 17:40:26'),(395,39,'Uploaded file Our_Services.jpg to task 59 (encrypted: False)','file','2025-06-02 17:40:26'),(396,39,'Created new task: notification test (ID: 82) with 1 assignees','task','2025-06-02 17:40:27'),(397,39,'Created new task: notification test (ID: 78) with 1 assignees','task','2025-06-02 17:40:28'),(398,39,'Created new task: notification test (ID: 81) with 1 assignees','task','2025-06-02 17:40:28'),(399,39,'Created new task: notification test (ID: 83) with 1 assignees','task','2025-06-02 17:40:33'),(400,39,'Created new task: notification test (ID: 86) with 1 assignees','task','2025-06-02 17:40:36'),(401,39,'Created new task: notification test (ID: 87) with 1 assignees','task','2025-06-02 17:40:36'),(402,39,'Created new task: notification test (ID: 84) with 1 assignees','task','2025-06-02 17:40:36'),(403,39,'Created new task: notification test (ID: 85) with 1 assignees','task','2025-06-02 17:40:36'),(404,39,'Created new task: notification test (ID: 88) with 1 assignees','task','2025-06-02 17:40:38'),(405,39,'Created new task: notification test (ID: 89) with 1 assignees','task','2025-06-02 17:40:43'),(406,39,'Uploaded file Our_Services.jpg to task 64 (encrypted: False)','file','2025-06-02 17:40:43'),(407,39,'Created new task: notification test (ID: 91) with 1 assignees','task','2025-06-02 17:40:44'),(408,39,'Uploaded file Our_Services.jpg to task 63 (encrypted: False)','file','2025-06-02 17:40:44'),(409,39,'Uploaded file Our_Services.jpg to task 60 (encrypted: False)','file','2025-06-02 17:40:44'),(410,39,'Uploaded file Our_Services.jpg to task 62 (encrypted: False)','file','2025-06-02 17:40:44'),(411,39,'Uploaded file Our_Services.jpg to task 61 (encrypted: False)','file','2025-06-02 17:40:44'),(412,39,'Uploaded file Our_Services.jpg to task 65 (encrypted: False)','file','2025-06-02 17:40:44'),(413,39,'Uploaded file Our_Services.jpg to task 66 (encrypted: False)','file','2025-06-02 17:40:44'),(414,39,'Uploaded file Our_Services.jpg to task 67 (encrypted: False)','file','2025-06-02 17:40:44'),(415,39,'Uploaded file Our_Services.jpg to task 70 (encrypted: False)','file','2025-06-02 17:40:44'),(416,39,'Uploaded file Our_Services.jpg to task 68 (encrypted: False)','file','2025-06-02 17:40:44'),(417,39,'Uploaded file Our_Services.jpg to task 69 (encrypted: False)','file','2025-06-02 17:40:44'),(418,39,'Uploaded file Our_Services.jpg to task 71 (encrypted: False)','file','2025-06-02 17:40:44'),(419,39,'Uploaded file Our_Services.jpg to task 73 (encrypted: False)','file','2025-06-02 17:40:44'),(420,39,'Uploaded file Our_Services.jpg to task 76 (encrypted: False)','file','2025-06-02 17:40:44'),(421,39,'Uploaded file Our_Services.jpg to task 74 (encrypted: False)','file','2025-06-02 17:40:44'),(422,39,'Uploaded file Our_Services.jpg to task 72 (encrypted: False)','file','2025-06-02 17:40:44'),(423,39,'Uploaded file Our_Services.jpg to task 75 (encrypted: False)','file','2025-06-02 17:40:44'),(424,39,'Uploaded file Our_Services.jpg to task 77 (encrypted: False)','file','2025-06-02 17:40:44'),(425,39,'Uploaded file Our_Services.jpg to task 80 (encrypted: False)','file','2025-06-02 17:40:44'),(426,39,'Uploaded file Our_Services.jpg to task 79 (encrypted: False)','file','2025-06-02 17:40:44'),(427,39,'Created new task: notification test (ID: 92) with 1 assignees','task','2025-06-02 17:40:44'),(428,39,'Created new task: notification test (ID: 93) with 1 assignees','task','2025-06-02 17:40:45'),(429,39,'Created new task: notification test (ID: 90) with 1 assignees','task','2025-06-02 17:40:45'),(430,39,'Created new task: notification test (ID: 94) with 1 assignees','task','2025-06-02 17:40:48'),(431,39,'Created new task: notification test (ID: 95) with 1 assignees','task','2025-06-02 17:40:53'),(432,39,'Uploaded file Our_Services.jpg to task 82 (encrypted: False)','file','2025-06-02 17:43:12'),(433,39,'Uploaded file Our_Services.jpg to task 81 (encrypted: False)','file','2025-06-02 17:43:12'),(434,39,'Uploaded file Our_Services.jpg to task 83 (encrypted: False)','file','2025-06-02 17:43:12'),(435,39,'Uploaded file Our_Services.jpg to task 86 (encrypted: False)','file','2025-06-02 17:43:12'),(436,39,'Uploaded file Our_Services.jpg to task 87 (encrypted: False)','file','2025-06-02 17:43:12'),(437,39,'Uploaded file Our_Services.jpg to task 78 (encrypted: False)','file','2025-06-02 17:43:12'),(438,39,'Uploaded file Our_Services.jpg to task 84 (encrypted: False)','file','2025-06-02 17:43:12'),(439,39,'Uploaded file Our_Services.jpg to task 85 (encrypted: False)','file','2025-06-02 17:43:12'),(440,39,'Uploaded file Our_Services.jpg to task 88 (encrypted: False)','file','2025-06-02 17:43:12'),(441,39,'Uploaded file Our_Services.jpg to task 89 (encrypted: False)','file','2025-06-02 17:43:12'),(442,39,'Uploaded file Our_Services.jpg to task 91 (encrypted: False)','file','2025-06-02 17:43:15'),(443,39,'Created new task: test notif (ID: 96) with 1 assignees','task','2025-06-02 17:43:57'),(444,39,'Created new task: test notif (ID: 98) with 1 assignees','task','2025-06-02 17:43:57'),(445,39,'Created new task: test notif (ID: 97) with 1 assignees','task','2025-06-02 17:43:58'),(446,39,'Deleted task: notification test (ID: 91)','task','2025-06-02 17:44:36'),(447,39,'Deleted task: notification test (ID: 92)','task','2025-06-02 17:44:38'),(448,39,'Deleted task: notification test (ID: 93)','task','2025-06-02 17:44:40'),(449,39,'Deleted task: notification test (ID: 89)','task','2025-06-02 17:44:43'),(450,39,'Deleted task: notification test (ID: 88)','task','2025-06-02 17:44:45'),(451,39,'Deleted task: notification test (ID: 87)','task','2025-06-02 17:44:48'),(452,39,'Deleted task: notification test (ID: 90)','task','2025-06-02 17:44:50'),(453,39,'Deleted task: notification test (ID: 85)','task','2025-06-02 17:44:53'),(454,39,'Deleted task: notification test (ID: 84)','task','2025-06-02 17:44:55'),(455,39,'Deleted task: notification test (ID: 83)','task','2025-06-02 17:44:57'),(456,39,'Deleted task: notification test (ID: 82)','task','2025-06-02 17:44:59'),(457,39,'Deleted task: notification test (ID: 86)','task','2025-06-02 17:45:01'),(458,39,'Deleted task: notification test (ID: 81)','task','2025-06-02 17:45:04'),(459,39,'Deleted task: notification test (ID: 94)','task','2025-06-02 17:45:06'),(460,39,'Deleted task: notification test (ID: 78)','task','2025-06-02 17:45:08'),(461,39,'Deleted task: notification test (ID: 59)','task','2025-06-02 17:45:10'),(462,39,'Deleted task: test notif (ID: 98)','task','2025-06-02 17:46:32'),(463,39,'Deleted task: notification test (ID: 76)','task','2025-06-02 17:46:34'),(464,39,'Deleted task: notification test (ID: 74)','task','2025-06-02 17:46:36'),(465,39,'Deleted task: notification test (ID: 75)','task','2025-06-02 17:46:38'),(466,39,'Deleted task: notification test (ID: 73)','task','2025-06-02 17:46:40'),(467,39,'Deleted task: notification test (ID: 72)','task','2025-06-02 17:46:42'),(468,39,'Deleted task: notification test (ID: 70)','task','2025-06-02 17:46:44'),(469,39,'Deleted task: notification test (ID: 71)','task','2025-06-02 17:46:46'),(470,39,'Deleted task: notification test (ID: 69)','task','2025-06-02 17:46:48'),(471,39,'Deleted task: notification test (ID: 68)','task','2025-06-02 17:46:50'),(472,39,'Deleted task: notification test (ID: 65)','task','2025-06-02 17:46:53'),(473,39,'Deleted task: notification test (ID: 66)','task','2025-06-02 17:46:55'),(474,39,'Deleted task: notification test (ID: 64)','task','2025-06-02 17:46:56'),(475,39,'Deleted task: notification test (ID: 63)','task','2025-06-02 17:46:58'),(476,39,'Deleted task: notification test (ID: 62)','task','2025-06-02 17:47:01'),(477,39,'Deleted task: encrypted (ID: 55)','task','2025-06-02 17:47:06'),(478,39,'Deleted task: notification test (ID: 95)','task','2025-06-02 17:47:08'),(479,39,'Deleted task: notification test (ID: 61)','task','2025-06-02 17:47:10'),(480,39,'Deleted task: notification test (ID: 67)','task','2025-06-02 17:47:12'),(481,39,'Deleted task: notification test (ID: 77)','task','2025-06-02 17:47:14'),(482,39,'Deleted task: notification test (ID: 79)','task','2025-06-02 17:47:15'),(483,39,'Deleted task: notification test (ID: 80)','task','2025-06-02 17:47:17'),(484,39,'Deleted task: notification test (ID: 60)','task','2025-06-02 17:47:20'),(485,39,'Deleted task: test notif (ID: 96)','task','2025-06-02 17:47:27'),(486,39,'Created new task: test (ID: 99) with 1 assignees','task','2025-06-02 17:47:46'),(487,39,'Created new task: why love (ID: 100) with 1 assignees','task','2025-06-02 17:51:24'),(488,39,'Created new task: my type (ID: 101) with 1 assignees','task','2025-06-02 17:52:45'),(489,39,'Uploaded file MT.png to task 101 (encrypted: False)','file','2025-06-02 17:52:45'),(490,39,'Deleted task: why love (ID: 100)','task','2025-06-02 17:59:34'),(491,39,'Deleted task: my type (ID: 101)','task','2025-06-02 17:59:37'),(492,39,'Deleted task: test notif (ID: 97)','task','2025-06-02 17:59:40'),(493,39,'Created new task: notification testing (ID: 102) with 1 assignees','task','2025-06-02 18:00:12'),(494,39,'Created new task: test 3 (ID: 103) with 1 assignees','task','2025-06-02 18:14:11'),(495,39,'Deleted task: test non key holder (ID: 58)','task','2025-06-02 18:17:14'),(496,39,'Deleted task: test (ID: 99)','task','2025-06-02 18:17:17'),(497,39,'Deleted task: notification testing (ID: 102)','task','2025-06-02 18:17:20'),(498,39,'Created new task: notify (ID: 108) with 1 assignees','task','2025-06-02 18:27:11'),(499,39,'Deleted task: test 3 (ID: 103)','task','2025-06-02 18:29:24'),(500,39,'Logged in to the system','login','2025-06-03 06:54:58'),(502,39,'Created new task: time test (ID: 109) with 1 assignees','task','2025-06-03 08:21:16'),(503,39,'Created new task: timezone (ID: 110) with 1 assignees','task','2025-06-03 10:01:46'),(504,39,'Created new task: timezone (ID: 111) with 1 assignees','task','2025-06-03 10:02:05'),(505,39,'Created new task: WWW (ID: 112) with 1 assignees','task','2025-06-03 10:10:39'),(507,39,'Downloaded file: Image_11-05-2025_at_3.57_PM.jpeg from task 114','file','2025-06-03 10:35:18'),(508,39,'Created new task: TRY (ID: 126) with 1 assignees','task','2025-06-03 11:24:54'),(509,39,'Created new task: GOT (ID: 127) with 1 assignees','task','2025-06-03 11:25:22'),(510,39,'Logged in to the system','login','2025-06-04 08:32:33'),(511,39,'Updated user role: saleem (ID: 52)','user','2025-06-04 08:32:53'),(512,39,'Deleted user: managerqcp (ID: 51)','user','2025-06-04 08:33:07'),(513,39,'Created new task: poll (ID: 128) with 1 assignees','task','2025-06-04 08:57:27'),(515,39,'Created new task: yes (ID: 131) with 1 assignees','task','2025-06-04 10:16:10'),(516,39,'Created new task: test time (ID: 132) with 1 assignees','task','2025-06-04 10:28:28'),(517,39,'Created new task: about (ID: 133) with 1 assignees','task','2025-06-04 10:40:12'),(518,39,'Created new task: timezone test (ID: 134) with 1 assignees','task','2025-06-04 10:52:21'),(519,39,'Created new task: wahala (ID: 135) with 1 assignees','task','2025-06-04 12:37:23'),(520,39,'Deleted task: yes (ID: 130)','task','2025-06-04 12:42:15'),(521,39,'Deleted task: yes (ID: 131)','task','2025-06-04 12:42:18'),(522,39,'Deleted task: test time (ID: 132)','task','2025-06-04 12:42:20'),(523,39,'Deleted task: about (ID: 133)','task','2025-06-04 12:42:23'),(524,39,'Deleted task: modified TIME (ID: 129)','task','2025-06-04 12:42:25'),(525,39,'Deleted task: timezone test (ID: 134)','task','2025-06-04 12:42:28'),(526,39,'Deleted task: wahala (ID: 135)','task','2025-06-04 12:42:30'),(527,39,'Deleted task: encrypted 2 (ID: 56)','task','2025-06-04 12:47:00'),(528,39,'Deleted task: test non encrypted (ID: 57)','task','2025-06-04 12:47:08'),(529,39,'Created new task: test LOCK (ID: 136) with 1 assignees','task','2025-06-04 13:09:27'),(530,39,'Uploaded file Image_11-05-2025_at_3.57_PM.jpeg to task 136 (encrypted: True)','file','2025-06-04 13:09:27'),(532,39,'Created new task: notification test (ID: 137) with 1 assignees','task','2025-06-04 13:31:54'),(533,39,'Logged in to the system','login','2025-06-04 14:52:22'),(534,39,'Deleted task: notification test (ID: 137)','task','2025-06-04 14:52:53'),(535,39,'Logged in to the system','login','2025-06-05 09:29:48'),(536,39,'Created new task: manager notification  (ID: 138) with 1 assignees','task','2025-06-05 09:41:53'),(538,39,'Created new task: overdue test (ID: 139) with 1 assignees','task','2025-06-05 09:57:50'),(539,39,'Created new task: send name change test (ID: 140) with 1 assignees','task','2025-06-05 10:27:35'),(540,39,'Created new task: deadline test (ID: 141) with 1 assignees','task','2025-06-05 10:29:13'),(541,39,'Created new task: sample (ID: 142) with 1 assignees','task','2025-06-05 10:38:43'),(542,39,'Uploaded file Lab_SP.pdf to task 142 (encrypted: True)','file','2025-06-05 10:38:43'),(548,39,'Deleted task: overdue test (ID: 139)','task','2025-06-05 12:25:55'),(550,39,'Logged out of the system','logout','2025-06-06 09:12:43'),(551,39,'Logged in to the system','login','2025-06-07 04:12:06'),(552,39,'Deleted task: send name change test (ID: 140)','task','2025-06-08 10:15:43'),(553,39,'Deleted task: notify (ID: 108)','task','2025-06-08 10:15:47'),(554,39,'Deleted task: sample (ID: 142)','task','2025-06-08 10:15:51'),(555,39,'Deleted task: manager notification  (ID: 138)','task','2025-06-08 10:15:53'),(556,39,'Deleted task: poll (ID: 128)','task','2025-06-08 10:16:04'),(557,39,'Logged out of the system','logout','2025-06-11 06:04:42'),(558,39,'Logged in to the system','login','2025-06-11 08:28:50'),(559,39,'Created new task: PSM2 (ID: 143) with 1 assignees','task','2025-06-11 08:35:13'),(560,39,'Logged out of the system','logout','2025-06-11 08:38:32'),(565,39,'Logged in to the system','login','2025-06-11 09:35:28'),(566,NULL,'Failed login attempt (email not found): wagmi@gmail.com','logout','2025-06-11 09:48:33'),(567,NULL,'Failed login attempt (email not found): wagmi@gmail.com','logout','2025-06-11 09:50:18'),(568,NULL,'Failed login attempt (email not found): wagmi@gmail.com','logout','2025-06-11 09:50:18'),(569,NULL,'Failed login attempt (email not found): wagmi@gmail.com','logout','2025-06-11 09:51:28'),(570,NULL,'Failed login attempt (email not found): wagmi@gmail.com','logout','2025-06-11 09:51:28'),(571,NULL,'Failed login attempt (email not found): wagmi@gmail.com','logout','2025-06-11 09:51:29'),(572,NULL,'Failed login attempt (email not found): wagmi@gmail.com','logout','2025-06-11 09:51:29'),(573,NULL,'Failed login attempt (email not found): wagmi@gmail.com','logout','2025-06-11 09:51:29'),(574,NULL,'Failed login attempt (email not found): wagmi@gmail.com','logout','2025-06-11 09:51:29'),(575,NULL,'invalid credentials','logout','2025-06-11 09:52:38'),(576,NULL,'invalid credentials','logout','2025-06-11 09:52:38'),(577,NULL,'invalid credentials','logout','2025-06-11 09:52:39'),(578,NULL,'invalid credentials','logout','2025-06-11 09:55:04'),(579,NULL,'invalid credentials','logout','2025-06-11 09:55:04'),(580,NULL,'Failed login attempt (invalid credentials): sal7@gmail.com','login','2025-06-11 10:00:41'),(581,NULL,'Failed login attempt (invalid credentials): sal7@gmail.com','logout','2025-06-11 10:03:50'),(582,NULL,'Failed email verification (invalid or expired code): saleemuddeen02@gmail.com','logout','2025-06-12 02:07:41'),(583,39,'Logged in to the system','login','2025-06-12 02:07:41'),(584,39,'Logged out of the system','logout','2025-06-12 03:51:42'),(585,NULL,'Failed email verification (invalid or expired code): saleemm1137@gmail.com','logout','2025-06-12 03:52:50'),(589,NULL,'Failed email verification (invalid or expired code): saleemuddeen02@gmail.com','logout','2025-06-12 10:13:59'),(590,39,'Logged in to the system','login','2025-06-12 10:13:59'),(591,39,'Updated user role: staffqcp (ID: 44)','user','2025-06-12 11:10:49'),(592,39,'Updated user role: staffqcp (ID: 44)','user','2025-06-12 11:12:12'),(593,39,'Updated user role: staffqcp (ID: 44)','user','2025-06-12 11:16:21'),(594,39,'Updated user role: staffqcp (ID: 44)','user','2025-06-12 11:18:24'),(595,NULL,'Failed login attempt (invalid credentials): osagede@graduate.utm.my','logout','2025-06-12 11:21:16'),(596,NULL,'Failed login attempt (invalid credentials): osagede@graduate.utm.my','logout','2025-06-12 11:21:22'),(597,NULL,'Failed email verification (invalid or expired code): saleemm1137@gmail.com','logout','2025-06-12 11:22:08'),(598,NULL,'Failed email verification (invalid or expired code): saleemm1137@gmail.com','logout','2025-06-12 11:29:20'),(599,NULL,'Failed login attempt (invalid credentials): osagede@graduate.utm.my','logout','2025-06-12 11:50:01'),(600,39,'Deleted user: saleem (ID: 52)','user','2025-06-13 09:46:47'),(601,39,'Created new user: testU (test@gmail.com)','user','2025-06-13 09:47:24'),(602,39,'Deleted user: testU (ID: 53)','user','2025-06-13 09:47:48'),(603,39,'Created new user: testuser (testuser@gmail.com)','user','2025-06-13 09:48:16'),(604,39,'Deleted user: testuser (ID: 54)','user','2025-06-13 09:53:52'),(605,39,'Created new user: testuser1 (testuser@gmail.com)','user','2025-06-13 09:54:45'),(606,39,'Deleted user: testuser1 (ID: 55)','user','2025-06-13 09:54:58'),(607,39,'Created new user: raved (dfvdfv@gmail.com)','user','2025-06-13 10:04:09'),(608,39,'Deleted user: raved (ID: 56)','user','2025-06-13 10:04:13'),(609,39,'Deleted user: Testuser (ID: 57)','user','2025-06-13 10:27:38'),(611,39,'Deleted user: testuser11 (ID: 58)','user','2025-06-13 10:37:51'),(612,NULL,'Registered new account','user','2025-06-13 10:38:01'),(613,NULL,'Logged out of the system','logout','2025-06-13 10:38:52'),(614,39,'Logged in to the system','login','2025-06-13 10:39:14'),(615,39,'Logged in to the system','login','2025-06-13 11:02:22'),(616,39,'Deleted user: testuser11 (ID: 59)','user','2025-06-13 11:02:32'),(617,NULL,'Registered new account','user','2025-06-13 11:07:52'),(618,39,'Deleted user: signuptest (ID: 60)','user','2025-06-13 11:14:09'),(620,NULL,'Failed login attempt (invalid credentials): osagede@gradaute.utm.my','logout','2025-06-13 11:16:34'),(621,NULL,'Failed login attempt (invalid credentials): osagede@gradaute.utm.my','logout','2025-06-13 11:16:44'),(622,NULL,'Failed login attempt (invalid credentials): osagede@gradaute.utm.my','logout','2025-06-13 11:16:45'),(623,NULL,'Failed login attempt (invalid credentials): osagede@gradaute.utm.my','logout','2025-06-13 11:16:46'),(624,NULL,'Failed login attempt (invalid credentials): osagede@gradaute.utm.my','logout','2025-06-13 11:17:08'),(625,NULL,'Failed login attempt (invalid credentials): osagede@gradaute.utm.my','logout','2025-06-13 11:17:09'),(626,NULL,'Failed login attempt (invalid credentials): osagede@gradaute.utm.my','logout','2025-06-13 11:17:17'),(627,NULL,'Failed login attempt (invalid credentials): osagede@gradaute.utm.my','logout','2025-06-13 11:17:18'),(628,NULL,'Failed login attempt (invalid credentials): osagede@gradaute.utm.my','logout','2025-06-13 11:17:21'),(629,NULL,'Failed login attempt (invalid credentials): osagede@gradaute.utm.my','logout','2025-06-13 11:17:33'),(634,39,'Deleted task: test 1 (ID: 144)','task','2025-06-13 11:48:36'),(635,39,'Deleted task: test 2 (ID: 145)','task','2025-06-13 11:48:39'),(636,39,'Deleted task: test 3 (ID: 146)','task','2025-06-13 11:48:41'),(637,39,'Deleted task: test 4 (ID: 147)','task','2025-06-13 11:48:44'),(638,39,'Deleted task: try (ID: 154)','task','2025-06-13 12:20:55'),(639,39,'Deleted task: test 3 (ID: 148)','task','2025-06-13 12:20:57'),(640,39,'Deleted task: test12345 (ID: 153)','task','2025-06-13 12:21:00'),(641,39,'Deleted task: test 44 (ID: 149)','task','2025-06-13 12:21:03'),(642,39,'Deleted task: test 444 (ID: 150)','task','2025-06-13 12:21:06'),(643,39,'Deleted task: test12345 (ID: 152)','task','2025-06-13 12:21:08'),(644,39,'Deleted task: test 444 (ID: 151)','task','2025-06-13 12:21:10'),(645,39,'Deleted task: gypsy (ID: 155)','task','2025-06-13 12:21:12'),(646,39,'Deleted task: goon (ID: 156)','task','2025-06-13 12:21:15'),(647,39,'Deleted task: bismillah2 (ID: 160)','task','2025-06-13 12:42:25'),(648,39,'Deleted task: error wahala (ID: 158)','task','2025-06-13 12:42:29'),(649,39,'Deleted task: jumbo (ID: 157)','task','2025-06-13 12:42:33'),(650,39,'Deleted task: bismillah (ID: 159)','task','2025-06-13 12:42:35'),(651,39,'Deleted task: okok (ID: 161)','task','2025-06-13 12:42:38'),(652,39,'Deleted task: okok alright (ID: 162)','task','2025-06-13 12:42:41'),(653,39,'Deleted task: okok alright (ID: 163)','task','2025-06-13 12:42:44'),(654,39,'Created new task: alright (ID: 164) with 1 assignees','task','2025-06-13 13:14:02'),(655,39,'Created new task: kilo (ID: 165) with 1 assignees','task','2025-06-13 13:14:38'),(656,39,'Deleted task: alright (ID: 164)','task','2025-06-13 13:31:50'),(657,39,'Deleted task: kilo (ID: 165)','task','2025-06-13 13:31:53'),(658,39,'Logged in to the system','login','2025-06-14 06:41:24'),(659,NULL,'Registered new account','user','2025-06-14 06:56:19'),(660,39,'Logged out of the system','logout','2025-06-15 09:15:42'),(661,NULL,'Failed email verification (invalid or expired code): saleemuddeen02@gmail.com','logout','2025-06-15 09:42:41'),(662,39,'Logged in to the system','login','2025-06-15 09:43:09'),(663,39,'Logged in to the system','login','2025-06-20 06:56:06'),(664,39,'Deleted user: inactiveuser (ID: 62)','user','2025-06-20 06:58:12'),(665,39,'Created new task: oya now (ID: 166) with 1 assignees','task','2025-06-20 07:00:29'),(667,39,'Deleted task: oya now (ID: 166)','task','2025-06-20 07:55:56'),(668,39,'Created new task: test1 (ID: 167) with 1 assignees','task','2025-06-20 07:57:41'),(669,39,'Deleted task: test1 (ID: 167)','task','2025-06-20 07:58:10'),(670,39,'Created new task: test 2 (ID: 168) with 1 assignees','task','2025-06-20 08:04:17'),(671,39,'Deleted task: test 2 (ID: 168)','task','2025-06-20 08:05:00'),(672,39,'Created new task: test 3 (ID: 169) with 1 assignees','task','2025-06-20 08:06:08'),(673,39,'Deleted task: test 3 (ID: 169)','task','2025-06-20 08:13:57'),(674,39,'Created new task: yeah (ID: 170) with 1 assignees','task','2025-06-20 08:55:55'),(675,39,'Deleted task: yeah (ID: 170)','task','2025-06-20 08:57:05'),(676,39,'Created new task: face2face (ID: 171) with 1 assignees','task','2025-06-20 10:51:42'),(677,39,'Created new task: face3face (ID: 172) with 1 assignees','task','2025-06-20 10:52:10'),(678,39,'Logged in to the system','login','2025-06-20 13:08:03'),(679,39,'Deleted task: face3face (ID: 172)','task','2025-06-20 15:10:52'),(680,39,'Deleted task: face2face (ID: 171)','task','2025-06-20 16:50:31'),(681,39,'Logged in to the system','login','2025-06-21 09:20:08'),(682,39,'Deleted user: mohannad124 (ID: 63)','user','2025-06-21 09:20:17'),(683,39,'Deleted user: mohannad1234 (ID: 64)','user','2025-06-21 09:20:20'),(684,39,'Logged out of the system','logout','2025-06-21 09:21:15'),(685,NULL,'Registered new account','user','2025-06-21 09:22:05'),(686,39,'Logged in to the system','login','2025-06-21 09:36:35'),(687,39,'Deleted user: saleemmz (ID: 65)','user','2025-06-21 09:37:02'),(688,39,'Logged out of the system','logout','2025-06-21 09:44:30'),(689,39,'Logged in to the system','login','2025-06-21 09:57:32'),(690,39,'Created new task: Code (ID: 173) with 1 assignees','task','2025-06-21 10:01:55'),(691,39,'Created new task: code 2  (ID: 174) with 1 assignees','task','2025-06-21 10:02:50'),(692,39,'Updated profile: First name changed from \'Admin\' to \'Manager\'','profile','2025-06-21 10:11:48'),(704,39,'Logged in to the system','login','2025-06-21 10:30:52'),(705,39,'Created new user: adam1234 (adam@gmail.com)','user','2025-06-21 10:33:14'),(706,39,'Logged out of the system','logout','2025-06-21 10:37:06'),(707,39,'Deleted user: adam1234 (ID: 66)','user','2025-06-21 11:05:46'),(708,39,'Deleted task: Code (ID: 173)','task','2025-06-21 11:16:25'),(709,39,'Deleted task: PSM2 (ID: 143)','task','2025-06-21 11:16:35'),(710,39,'Deleted task: deadline test (ID: 141)','task','2025-06-21 11:16:43'),(711,39,'Logged in to the system','login','2025-06-21 13:13:35'),(712,39,'Logged out of the system','logout','2025-06-21 13:14:55'),(716,39,'Created new task: ok (ID: 175) with 2 assignees','task','2025-06-21 13:35:26'),(717,39,'Deleted task: code 2  (ID: 174)','task','2025-06-21 13:36:12'),(718,39,'Created new task: Test1 (ID: 176) with 2 assignees','task','2025-06-21 13:37:59'),(739,39,'Deleted task: Test1 (ID: 176)','task','2025-06-21 14:07:40'),(740,39,'Deleted task: ok (ID: 175)','task','2025-06-21 14:07:53'),(741,39,'Created new task: wahala (ID: 177) with 2 assignees','task','2025-06-21 14:10:21'),(744,39,'Deleted user: olatech (ID: 61)','user','2025-06-21 14:35:15'),(745,39,'Created new user: testname (testname123@gmail.com)','user','2025-06-21 14:35:51'),(746,39,'Deleted user: testname (ID: 67)','user','2025-06-21 14:35:55'),(750,39,'Logged out of the system','logout','2025-06-21 15:11:16'),(751,39,'Logged in to the system','login','2025-06-21 15:25:42'),(752,39,'Logged out of the system','logout','2025-06-21 15:38:59'),(753,39,'Logged in to the system','login','2025-06-21 15:40:12'),(754,39,'Logged in to the system','login','2025-06-23 12:26:27'),(755,39,'Updated profile: First name changed from \'Manager\' to \'Admin\'','profile','2025-06-23 13:34:50'),(756,39,'Created new task: Design flyer (ID: 178) with 1 assignees','task','2025-06-23 13:37:06'),(757,NULL,'Failed email verification (invalid or expired code): saleemm1137@gmail.com','logout','2025-06-23 13:39:06'),(758,39,'Logged in to the system','login','2025-06-25 15:12:43'),(759,39,'Deleted task: wahala (ID: 177)','task','2025-06-25 15:13:43'),(761,39,'Deleted user: olastaff (ID: 68)','user','2025-06-25 17:46:26'),(763,39,'Deleted user: olatech (ID: 69)','user','2025-06-25 17:46:52'),(765,39,'Deleted user: olatech (ID: 70)','user','2025-06-25 18:17:31'),(767,39,'Created new task: test 1 (ID: 179) with 1 assignees','task','2025-06-25 18:19:37'),(768,39,'Deleted task: test 1 (ID: 179)','task','2025-06-25 18:21:20'),(769,39,'Created new task: test 2 (ID: 180) with 1 assignees','task','2025-06-25 18:21:38'),(772,39,'Created new task: test3 (ID: 181) with 1 assignees','task','2025-06-25 18:28:20'),(773,39,'Deleted task: test 2 (ID: 180)','task','2025-06-25 18:40:55'),(774,39,'Deleted task: Design flyer (ID: 178)','task','2025-06-25 18:41:03'),(775,39,'Deleted task: test3 (ID: 181)','task','2025-06-25 18:41:10'),(776,39,'Created new task: test 44 (ID: 182) with 1 assignees','task','2025-06-25 18:56:44'),(777,39,'Deleted task: Test Deadline Notification Task (ID: 183)','task','2025-06-25 19:08:11'),(778,39,'Created new task: test 99 (ID: 185) with 1 assignees','task','2025-06-25 19:10:46'),(779,39,'Deleted task: test 44 (ID: 182)','task','2025-06-25 19:17:34'),(780,39,'Deleted task: Test Deadline Notification Task (ID: 184)','task','2025-06-25 19:17:39'),(781,39,'Deleted task: test 99 (ID: 185)','task','2025-06-25 19:17:46'),(782,39,'Created new task: yes (ID: 186) with 1 assignees','task','2025-06-25 19:19:49'),(786,39,'Created new task: test due (ID: 187) with 1 assignees','task','2025-06-25 19:29:05'),(788,39,'Deleted task: test LOCK (ID: 136)','task','2025-06-25 19:32:23'),(789,39,'Downloaded file: Screenshot_2025-06-23_at_6.53.49_PM.png from task 186','file','2025-06-25 19:32:44'),(790,39,'Created new task: test 22 (ID: 188) with 1 assignees','task','2025-06-25 19:39:27'),(793,39,'Created new task: test 34 (ID: 189) with 1 assignees','task','2025-06-25 19:43:38'),(800,39,'Created new task: test 123 (ID: 190) with 1 assignees','task','2025-06-25 19:46:07'),(815,39,'Created new task: test Sahara (ID: 191) with 1 assignees','task','2025-06-25 19:51:34'),(824,39,'Created new task: trial again (ID: 192) with 1 assignees','task','2025-06-25 19:58:15'),(835,39,'Created new task: okolk (ID: 193) with 1 assignees','task','2025-06-25 20:02:36'),(848,39,'Created new task: last try (ID: 194) with 1 assignees','task','2025-06-25 20:14:20'),(853,39,'Deleted task: test 34 (ID: 189)','task','2025-06-25 20:19:10'),(854,39,'Deleted task: test Sahara (ID: 191)','task','2025-06-25 20:19:16'),(855,39,'Deleted task: test 123 (ID: 190)','task','2025-06-25 20:19:21'),(856,39,'Deleted task: last try (ID: 194)','task','2025-06-25 20:19:32'),(857,39,'Deleted task: trial again (ID: 192)','task','2025-06-25 20:19:42'),(858,39,'Deleted task: okolk (ID: 193)','task','2025-06-25 20:19:50'),(859,39,'Created new task: oya now (ID: 195) with 1 assignees','task','2025-06-25 20:20:20'),(867,39,'Logged in to the system','login','2025-06-26 08:40:18'),(868,39,'Created new task: trying (ID: 196) with 1 assignees','task','2025-06-26 08:41:00'),(875,39,'Created new task: fagbo (ID: 197) with 1 assignees','task','2025-06-26 08:53:27'),(882,39,'Deleted task: fagbo (ID: 197)','task','2025-06-26 09:01:03'),(883,39,'Deleted task: test 22 (ID: 188)','task','2025-06-26 09:01:09'),(884,39,'Deleted task: trying (ID: 196)','task','2025-06-26 09:01:15'),(885,39,'Created new task: trial n error (ID: 198) with 1 assignees','task','2025-06-26 09:01:40'),(890,39,'Created new task: GOOGLE (ID: 199) with 1 assignees','task','2025-06-26 09:14:55'),(891,39,'Created new task: New (ID: 200) with 1 assignees','task','2025-06-26 09:24:58'),(892,39,'Deleted task: GOOGLE (ID: 199)','task','2025-06-26 09:51:59'),(893,39,'Deleted task: New (ID: 200)','task','2025-06-26 09:52:05'),(894,39,'Deleted task: oya now (ID: 195)','task','2025-06-26 09:52:11'),(895,39,'Deleted task: trial n error (ID: 198)','task','2025-06-26 09:52:17'),(896,39,'Created new task: all test (ID: 201) with 1 assignees','task','2025-06-26 09:52:59'),(905,39,'Created new task: all test 2 (ID: 202) with 1 assignees','task','2025-06-26 10:02:04'),(924,39,'Created new task: all test 33 (ID: 203) with 1 assignees','task','2025-06-26 10:11:40'),(947,39,'Created new task: nexus (ID: 204) with 1 assignees','task','2025-06-26 10:27:41'),(948,39,'Deleted task: all test 33 (ID: 203)','task','2025-06-26 10:28:03'),(949,39,'Deleted task: all test (ID: 201)','task','2025-06-26 10:28:09'),(950,39,'Deleted task: all test 2 (ID: 202)','task','2025-06-26 10:28:15'),(961,39,'Created new task: okok (ID: 205) with 1 assignees','task','2025-06-26 10:40:49'),(966,39,'Created new task: nice (ID: 206) with 1 assignees','task','2025-06-26 10:47:01'),(973,39,'Created new task: MBW (ID: 207) with 1 assignees and 0 files','task','2025-06-26 10:53:54'),(974,39,'Created new task: NBA (ID: 208) with 1 assignees and 0 files','task','2025-06-26 10:55:17'),(975,39,'Created new task: passat (ID: 209) with 1 assignees and 0 files','task','2025-06-26 11:00:50'),(976,39,'Created new task: buggati (ID: 210) with 1 assignees','task','2025-06-26 11:03:29'),(977,39,'Created new task: too bad (ID: 211) with 0 assignees','task','2025-06-26 11:09:18'),(978,39,'Created new task: mummy  (ID: 212) with 1 assignees','task','2025-06-26 11:09:52'),(979,39,'Deleted task: nexus (ID: 204)','task','2025-06-26 11:10:16'),(980,39,'Deleted task: mummy  (ID: 212)','task','2025-06-26 11:10:23'),(981,39,'Deleted task: passat (ID: 209)','task','2025-06-26 11:10:30'),(982,39,'Deleted task: MBW (ID: 207)','task','2025-06-26 11:10:36'),(983,39,'Deleted task: buggati (ID: 210)','task','2025-06-26 11:10:42'),(984,39,'Deleted task: okok (ID: 205)','task','2025-06-26 11:10:47'),(985,39,'Deleted task: too bad (ID: 211)','task','2025-06-26 11:10:50'),(986,39,'Deleted task: nice (ID: 206)','task','2025-06-26 11:10:57'),(987,39,'Created new task: musa (ID: 213) with 1 assignees','task','2025-06-26 11:17:57'),(988,39,'Created new task: open yens (ID: 214) with 1 assignees','task','2025-06-26 11:26:25'),(989,39,'Created new task: nzdusd (ID: 215) with 1 assignees','task','2025-06-26 11:29:10'),(990,39,'Created new task: cads (ID: 216) with 1 assignees','task','2025-06-26 11:32:45'),(991,39,'Created new task: eh (ID: 217) with 1 assignees','task','2025-06-26 11:48:37'),(992,39,'Created new task: insane (ID: 218) with 1 assignees','task','2025-06-26 11:57:33'),(993,39,'Created new task: break (ID: 219) with 1 assignees','task','2025-06-26 12:14:05'),(994,39,'Created new task: break2 (ID: 220) with 1 assignees','task','2025-06-26 12:14:45'),(995,39,'Created new task: break3 (ID: 221) with 1 assignees','task','2025-06-26 12:17:01'),(996,39,'Deleted task: open yens (ID: 214)','task','2025-06-26 12:17:42'),(997,39,'Deleted task: nzdusd (ID: 215)','task','2025-06-26 12:17:48'),(998,39,'Deleted task: break2 (ID: 220)','task','2025-06-26 12:17:57'),(999,39,'Deleted task: break3 (ID: 221)','task','2025-06-26 12:18:03'),(1000,39,'Deleted task: break (ID: 219)','task','2025-06-26 12:18:10'),(1001,39,'Deleted task: eh (ID: 217)','task','2025-06-26 12:18:17'),(1002,39,'Deleted task: cads (ID: 216)','task','2025-06-26 12:18:23'),(1003,39,'Deleted task: NBA (ID: 208)','task','2025-06-26 12:18:29'),(1004,39,'Deleted task: insane (ID: 218)','task','2025-06-26 12:18:37'),(1005,39,'Created new task: 50K (ID: 222) with 1 assignees','task','2025-06-26 13:01:30'),(1006,39,'Created new task: lego (ID: 223) with 1 assignees','task','2025-06-26 13:06:52'),(1007,39,'Created new task: All test (ID: 224) with 1 assignees','task','2025-06-26 13:09:39'),(1008,39,'Deleted task: lego (ID: 223)','task','2025-06-26 13:09:52'),(1009,39,'Deleted task: musa (ID: 213)','task','2025-06-26 13:09:59'),(1010,39,'Deleted task: 50K (ID: 222)','task','2025-06-26 13:10:05'),(1021,39,'Deleted task: All test (ID: 224)','task','2025-06-26 13:15:08'),(1022,39,'Created new task: t bani (ID: 225) with 1 assignees','task','2025-06-26 13:17:22'),(1037,39,'Created new task: nexus (ID: 226) with 1 assignees','task','2025-06-26 13:46:31'),(1040,39,'Created new task: haha (ID: 227) with 1 assignees','task','2025-06-26 13:55:24'),(1058,39,'Created new task: manager (ID: 228) with 1 assignees','task','2025-06-26 16:45:22'),(1063,39,'Deleted task: manager (ID: 228)','task','2025-06-26 16:47:24'),(1064,39,'Deleted task: haha (ID: 227)','task','2025-06-26 16:47:29'),(1065,39,'Deleted task: nexus (ID: 226)','task','2025-06-26 16:47:34'),(1066,39,'Created new task: easy (ID: 229) with 1 assignees','task','2025-06-26 16:48:00'),(1073,39,'Created new task: puta (ID: 230) with 1 assignees','task','2025-06-26 17:08:45'),(1086,39,'Created new task: fila (ID: 231) with 1 assignees','task','2025-06-26 17:13:56'),(1093,39,'Created new task: loski (ID: 232) with 1 assignees','task','2025-06-26 17:21:57'),(1103,39,'Created new task: test final  (ID: 233) with 1 assignees','task','2025-06-26 17:28:19'),(1104,39,'Created new task: hope (ID: 234) with 1 assignees','task','2025-06-26 17:39:24'),(1109,39,'Deleted task: test final  (ID: 233)','task','2025-06-26 17:40:27'),(1110,39,'Deleted task: fila (ID: 231)','task','2025-06-26 17:40:32'),(1111,39,'Deleted task: t bani (ID: 225)','task','2025-06-26 17:40:38'),(1112,39,'Deleted task: easy (ID: 229)','task','2025-06-26 17:40:44'),(1113,39,'Deleted task: puta (ID: 230)','task','2025-06-26 17:40:50'),(1114,39,'Deleted task: loski (ID: 232)','task','2025-06-26 17:40:56'),(1115,39,'Created new task: Astagfirullah (ID: 235) with 1 assignees','task','2025-06-26 17:41:44'),(1120,39,'Created new task: non key (ID: 236) with 1 assignees','task','2025-06-26 17:44:02'),(1121,39,'Created new task: key (ID: 237) with 1 assignees','task','2025-06-26 17:44:21'),(1122,39,'Created new task: free (ID: 238) with 1 assignees','task','2025-06-26 17:44:40'),(1123,39,'Created new task: non key 2 (ID: 239) with 1 assignees','task','2025-06-26 17:47:42'),(1126,39,'Created new task: all test 33 (ID: 240) with 1 assignees','task','2025-06-26 17:49:00'),(1131,39,'Created new task: individual test (ID: 241) with 1 assignees','task','2025-06-26 17:54:12'),(1132,39,'Created new task: Jimena (ID: 242) with 1 assignees','task','2025-06-26 18:37:40'),(1133,39,'Created new task: WWW (ID: 243) with 1 assignees','task','2025-06-26 22:25:24'),(1134,39,'Deleted task: Astagfirullah (ID: 235)','task','2025-06-26 22:25:36'),(1135,39,'Deleted task: non key (ID: 236)','task','2025-06-26 22:25:42'),(1136,39,'Deleted task: key (ID: 237)','task','2025-06-26 22:25:49'),(1137,39,'Deleted task: free (ID: 238)','task','2025-06-26 22:25:54'),(1138,39,'Deleted task: non key 2 (ID: 239)','task','2025-06-26 22:26:01'),(1139,39,'Deleted task: all test 33 (ID: 240)','task','2025-06-26 22:26:07'),(1140,39,'Deleted task: individual test (ID: 241)','task','2025-06-26 22:26:21'),(1141,39,'Deleted task: Jimena (ID: 242)','task','2025-06-26 22:26:30'),(1142,39,'Deleted task: yes (ID: 186)','task','2025-06-26 22:26:45'),(1143,39,'Deleted task: hope (ID: 234)','task','2025-06-26 22:26:51'),(1148,39,'Downloaded file: FVG_1.png from task 243','file','2025-06-26 22:44:32'),(1150,39,'Logged out of the system','logout','2025-06-27 07:40:29'),(1152,39,'Logged in to the system','login','2025-06-27 07:43:16'),(1153,39,'Created new task: email (ID: 244) with 1 assignees','task','2025-06-27 08:45:13'),(1154,39,'Created new task: no email (ID: 245) with 1 assignees','task','2025-06-27 08:46:34'),(1155,39,'Deleted task: no email (ID: 245)','task','2025-06-27 08:48:37'),(1156,39,'Deleted task: email (ID: 244)','task','2025-06-27 08:48:40'),(1157,39,'Deleted task: test due (ID: 187)','task','2025-06-27 08:52:15'),(1161,39,'Updated profile avatar','profile','2025-06-27 09:11:17'),(1162,39,'Downloaded file: FVG_1.png from task 243','file','2025-06-27 09:11:29'),(1167,39,'Created new task: oya now (ID: 246) with 1 assignees','task','2025-06-27 09:28:22'),(1169,39,'Downloaded file: README.txt from task 246','file','2025-06-27 09:42:54'),(1172,39,'Logged out of the system','logout','2025-06-27 13:05:57'),(1173,39,'Logged in to the system','login','2025-06-27 13:06:19'),(1174,39,'Logged in to the system','login','2025-06-27 13:22:03'),(1175,39,'Logged in to the system','login','2025-06-27 13:26:00'),(1176,39,'Logged in to the system','login','2025-06-27 14:27:29'),(1177,39,'Deleted task: oya now (ID: 246)','task','2025-06-27 14:35:28'),(1178,39,'Created new task: Print (ID: 247) with 1 assignees','task','2025-06-27 14:36:07'),(1179,39,'Created new task: Flyer (ID: 248) with 1 assignees','task','2025-06-27 14:36:45'),(1180,39,'Created new task: Navigate (ID: 249) with 1 assignees','task','2025-06-27 14:37:32'),(1184,39,'Logged in to the system','login','2025-06-28 09:07:17'),(1185,39,'Logged in to the system','login','2025-06-28 15:39:30'),(1186,39,'Logged out of the system','logout','2025-06-28 15:41:15'),(1187,39,'Logged in to the system','login','2025-06-28 15:41:40'),(1188,39,'Logged out of the system','logout','2025-06-28 16:50:57'),(1192,39,'Logged in to the system','login','2025-06-28 17:00:33'),(1193,39,'Logged out of the system','logout','2025-06-28 17:26:50'),(1194,39,'Logged in to the system','login','2025-06-30 08:43:27'),(1195,39,'Created new task: worldwide (ID: 250) with 1 assignees','task','2025-06-30 11:24:09'),(1196,39,'Created new task: POLL (ID: 251) with 1 assignees','task','2025-06-30 11:46:40'),(1202,39,'Logged in to the system','login','2025-07-01 07:50:11'),(1203,39,'Updated user role: managerqcp (ID: 71)','user','2025-07-01 07:50:18'),(1206,39,'Updated user role: managerqcp (ID: 71)','user','2025-07-01 07:53:47'),(1207,39,'Updated user role: managerqcp (ID: 71)','user','2025-07-01 07:53:49'),(1208,39,'Updated user role: managerqcp (ID: 71)','user','2025-07-01 07:54:26'),(1209,39,'Updated user role: managerqcp (ID: 71)','user','2025-07-01 07:54:44'),(1210,39,'Updated user role: managerqcp (ID: 71)','user','2025-07-01 08:01:37'),(1211,39,'Updated user role: managerqcp (ID: 71)','user','2025-07-01 08:01:41'),(1217,39,'Logged in to the system','login','2025-07-02 04:58:47'),(1218,39,'Created new task: Print (ID: 252) with 1 assignees','task','2025-07-02 05:09:50'),(1219,39,'Deleted task: Print (ID: 247)','task','2025-07-02 05:10:13'),(1220,39,'Deleted task: WWW (ID: 243)','task','2025-07-02 05:10:17'),(1221,39,'Deleted task: Navigate (ID: 249)','task','2025-07-02 05:10:20'),(1226,39,'Created new task: Design (ID: 253) with 1 assignees','task','2025-07-02 07:16:46'),(1227,39,'Deleted user: inactive (ID: 72)','user','2025-07-02 07:20:05'),(1228,39,'Deleted user: managerqcp (ID: 71)','user','2025-07-02 07:20:24'),(1229,73,'Registered new account','user','2025-07-02 07:21:38'),(1230,39,'Logged in to the system','login','2025-07-02 08:51:49'),(1231,39,'Created new task: DELETE (ID: 254) with 1 assignees','task','2025-07-02 08:53:20'),(1236,39,'Deleted task: Design (ID: 253)','task','2025-07-02 11:17:49'),(1237,39,'Logged in to the system','login','2025-07-04 04:11:46'),(1238,39,'Updated profile: Phone changed from \'0187798035\' to \'None\'','profile','2025-07-04 04:37:56'),(1239,39,'Updated user role: managerqcp (ID: 73)','user','2025-07-04 07:32:03'),(1240,73,'Logged in to the system','login','2025-07-04 07:32:33'),(1241,NULL,'Failed email verification (invalid or expired code): osagede@graduate.utm.my','logout','2025-07-04 07:34:16'),(1242,73,'Logged in to the system','login','2025-07-04 07:34:31'),(1243,39,'Logged in to the system','login','2025-07-04 07:35:06'),(1244,39,'Deleted task: Print (ID: 252)','task','2025-07-04 07:35:43'),(1245,39,'Deleted task: DELETE (ID: 254)','task','2025-07-04 07:35:49'),(1246,39,'Deleted user: staffqcp (ID: 44)','user','2025-07-04 07:36:11'),(1247,74,'Registered new account','user','2025-07-04 07:41:08'),(1248,74,'Logged in to the system','login','2025-07-04 07:42:33'),(1249,39,'Logged in to the system','login','2025-07-04 07:43:08'),(1250,39,'Created new user: secure project (secure@gmail.com)','user','2025-07-04 07:44:16'),(1251,73,'Logged in to the system','login','2025-07-04 07:45:40'),(1252,73,'Created new task: Print (ID: 255) with 1 assignees','task','2025-07-04 07:47:27'),(1253,73,'Updated profile: Phone changed from \'\' to \'None\'','profile','2025-07-04 07:49:17'),(1254,74,'Requested decryption key email for task: Print','file','2025-07-04 07:52:02'),(1255,74,'Downloaded file: spt_activity_logs_2025-07-04.csv for task: Print','file','2025-07-04 07:52:39'),(1256,74,'submitted task: Print (ID: 255)','task','2025-07-04 07:53:46'),(1257,73,'Downloaded file: user_manual.docx from task 255','file','2025-07-04 07:55:14'),(1258,73,'Deleted task: Print (ID: 255)','task','2025-07-04 07:55:30'),(1259,39,'Logged in to the system','login','2025-07-04 14:58:26'),(1260,39,'Updated user role: managerqcp (ID: 73)','user','2025-07-04 14:58:32'),(1261,73,'Logged in to the system','login','2025-07-04 14:59:20'),(1262,39,'Updated user role: managerqcp (ID: 73)','user','2025-07-04 14:59:36'),(1263,39,'Updated user role: managerqcp (ID: 73)','user','2025-07-04 14:59:47'),(1264,73,'Logged in to the system','login','2025-07-04 15:00:38'),(1265,39,'Updated user role: managerqcp (ID: 73)','user','2025-07-04 15:00:55'),(1266,39,'Deleted user: secure project (ID: 75)','user','2025-07-04 15:00:59'),(1267,39,'Logged in to the system','login','2025-07-05 14:31:31');
/*!40000 ALTER TABLE `activities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('0f50e09157d4');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` int NOT NULL,
  `user_id` int NOT NULL,
  `comment_text` text NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `task_id` (`task_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_messages`
--

DROP TABLE IF EXISTS `contact_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `message` text NOT NULL,
  `ip_address` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `is_responded` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_messages`
--

LOCK TABLES `contact_messages` WRITE;
/*!40000 ALTER TABLE `contact_messages` DISABLE KEYS */;
INSERT INTO `contact_messages` VALUES (1,'saleemuddeen02@gmail.com','test support','127.0.0.1','2025-05-26 04:25:44',0),(2,'osagede@graduate.utm.my','Allahu Akbar!!','127.0.0.1','2025-06-13 11:23:18',0),(3,'saleemm1137@gmail.com','I HAVE PROBLEM','127.0.0.1','2025-06-21 09:59:18',0),(4,'osagede@graduate.utm.my','I am having issues with changing my password, please kindly help.','127.0.0.1','2025-07-02 07:39:45',0),(5,'saleemm1137@gmail.com','i have an issue with password recovery, please help,','127.0.0.1','2025-07-04 07:50:55',0);
/*!40000 ALTER TABLE `contact_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `feedback` text NOT NULL,
  `ip_address` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,'test','127.0.0.1','2025-05-26 04:25:32'),(2,'gjhgjgj','127.0.0.1','2025-05-29 07:56:48');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(255) NOT NULL,
  `file_path` varchar(512) NOT NULL,
  `is_encrypted` tinyint(1) NOT NULL,
  `task_id` int NOT NULL,
  `created_at` datetime NOT NULL,
  `uploaded_by` int NOT NULL,
  `file_size` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `task_id` (`task_id`),
  KEY `uploaded_by` (`uploaded_by`),
  CONSTRAINT `files_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`),
  CONSTRAINT `files_ibfk_2` FOREIGN KEY (`uploaded_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=299 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `key_holders`
--

DROP TABLE IF EXISTS `key_holders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `key_holders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `key_id` int NOT NULL,
  `assigned_at` datetime NOT NULL,
  `file_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `key_id` (`key_id`),
  KEY `file_id` (`file_id`),
  CONSTRAINT `key_holders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `key_holders_ibfk_2` FOREIGN KEY (`key_id`) REFERENCES `keys` (`id`),
  CONSTRAINT `key_holders_ibfk_3` FOREIGN KEY (`file_id`) REFERENCES `files` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `key_holders`
--

LOCK TABLES `key_holders` WRITE;
/*!40000 ALTER TABLE `key_holders` DISABLE KEYS */;
/*!40000 ALTER TABLE `key_holders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keys`
--

DROP TABLE IF EXISTS `keys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keys` (
  `id` int NOT NULL AUTO_INCREMENT,
  `encryption_key` varchar(256) NOT NULL,
  `task_id` int NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `task_id` (`task_id`),
  CONSTRAINT `keys_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keys`
--

LOCK TABLES `keys` WRITE;
/*!40000 ALTER TABLE `keys` DISABLE KEYS */;
/*!40000 ALTER TABLE `keys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(120) NOT NULL,
  `message` text NOT NULL,
  `notification_type` varchar(50) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `related_task_id` int DEFAULT NULL,
  `read_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `related_task_id` (`related_task_id`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`related_task_id`) REFERENCES `tasks` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=458 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (88,39,'Task Completed','Staff QCP has completed the task: \'test 3\'','task_completion',1,'2025-06-02 18:16:30',NULL,NULL),(90,39,'Task Completed','Staff QCP has completed the task: \'notify\'','task_completion',1,'2025-06-03 07:09:54',NULL,NULL),(91,39,'Task Completed','Staff QCP has completed the task: \'test non encrypted\'','task_completion',1,'2025-06-03 07:14:18',NULL,NULL),(116,39,'Task Completed','Staff QCP has completed the task: \'poll\'','task_completion',1,'2025-06-04 09:40:15',NULL,'2025-06-04 12:34:54'),(127,39,'Task Completed','Staff QCP has completed the task: \'manager notification \'','task_completion',1,'2025-06-05 09:42:14',NULL,NULL),(132,39,'Task Completed','Staff QCP has completed the task: \'sample\'','task_completion',1,'2025-06-05 10:39:51',NULL,NULL),(133,39,'Task Completed','Staff QCP has completed the task: \'deadline test\'','task_completion',1,'2025-06-05 12:08:41',NULL,NULL),(134,39,'Task Completed','Staff QCP has completed the task: \'test LOCK\'','task_completion',1,'2025-06-05 12:56:55',NULL,NULL),(136,39,'Task Completed','Staff QCP has completed the task: \'PSM2\'','task_completion',1,'2025-06-11 08:41:39',NULL,NULL),(137,39,'New User Registration','A new user has signed up: Test user (osagede@graduate.utm.my)','new_user',1,'2025-06-13 10:26:05',NULL,NULL),(138,39,'New User Registration','A new user has signed up: Test User (osagede@graduate.utm.my)','new_user',1,'2025-06-13 10:37:57',NULL,NULL),(139,39,'New Staff Registration','A new user has signed up: Signup Test (osagede@graduate.utm.my)','new_user',1,'2025-06-13 11:07:48',NULL,NULL),(140,39,'New Staff Registration','A new user has signed up: Ola Tech (osagede@graduate.utm.my)','new_user',1,'2025-06-13 11:15:23',NULL,NULL),(164,39,'New Staff Registration','A new user has signed up: Inactive User (inactive@gmail.com)','new_user',1,'2025-06-14 06:56:16',NULL,NULL),(177,39,'New Staff Registration','A new user has signed up: Saleem Abdul (kamel@graduate.utm.my)','new_user',1,'2025-06-21 09:22:00',NULL,NULL),(180,39,'Task Completed','Staff QCP has completed the task: \'Code\'','task_completion',1,'2025-06-21 10:21:00',NULL,NULL),(199,39,'New Staff Registration','A new user has signed up: Staff Ola (inactive@gmail.com)','new_user',1,'2025-06-25 16:14:34',NULL,NULL),(200,39,'New Staff Registration','A new user has signed up: Staff Qcp (inactive@gmail.com)','new_user',1,'2025-06-25 17:46:37',NULL,NULL),(201,39,'New Staff Registration','A new user has signed up: Staff Qcp (inactive@gmail.com)','new_user',1,'2025-06-25 17:49:15',NULL,NULL),(222,39,'Task Completed','Staff QCP has completed the task: \'yes\'','task_completion',1,'2025-06-25 19:23:38',NULL,NULL),(224,39,'Task Completed','Staff QCP has completed the task: \'test due\'','task_completion',1,'2025-06-25 19:32:10',NULL,NULL),(391,39,'Task Completed','Staff QCP has completed the task: \'WWW\'','task_completion',1,'2025-06-26 22:42:26',NULL,NULL),(392,39,'Notification Preferences Updated','Email notifications disabled','account_change',1,'2025-06-27 08:36:42',NULL,NULL),(406,39,'Task Completed','Staff QCP has completed the task: \'oya now\'','task_completion',1,'2025-06-27 09:42:31',NULL,NULL),(413,39,'Task Completed','Staff QCP has completed the task: \'Navigate\'','task_completion',1,'2025-06-27 16:13:30',NULL,NULL),(414,39,'Task Completed','Staff QCP has completed the task: \'Print\'','task_completion',1,'2025-06-27 16:13:41',NULL,NULL),(428,39,'New Staff Registration','A new user has signed up: Manager Qcp (osagede@graduate.utm.my)','new_user',1,'2025-07-01 07:46:27',NULL,NULL),(429,39,'New Staff Registration','A new user has signed up: Inactive User (inactive@gmail.com)','new_user',1,'2025-07-01 07:52:31',NULL,NULL),(440,39,'Task Completed','Staff QCP has completed the task: \'Print\'','task_completion',1,'2025-07-02 06:18:41',NULL,NULL),(444,39,'New Staff Registration','A new user has signed up: Manager Qcp (osagede@graduate.utm.my)','new_user',1,'2025-07-02 07:21:38',NULL,NULL),(447,39,'Task Completed','Staff QCP has completed the task: \'DELETE\'','task_completion',1,'2025-07-02 08:56:11',NULL,NULL),(453,39,'New Staff Registration','A new user has signed up: Staff Qcp (saleemm1137@gmail.com)','new_user',0,'2025-07-04 07:41:05',NULL,NULL),(454,73,'New Staff Registration','A new user has signed up: Staff Qcp (saleemm1137@gmail.com)','new_user',1,'2025-07-04 07:41:05',NULL,NULL),(455,74,'New Task Assigned','You have been assigned a new task: \'Print\'','task_assignment',1,'2025-07-04 07:47:25',NULL,'2025-07-04 07:51:17'),(456,73,'Task Completed','Staff Qcp has completed the task: \'Print\'','task_completion',1,'2025-07-04 07:53:46',NULL,NULL),(457,74,'Task Deleted','The task \'Print\' has been deleted by Manager Qcp','task_deletion',1,'2025-07-04 07:55:27',NULL,'2025-07-04 07:55:48');
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_assignees`
--

DROP TABLE IF EXISTS `task_assignees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_assignees` (
  `task_id` int NOT NULL,
  `user_id` int NOT NULL,
  `assigned_at` datetime NOT NULL,
  PRIMARY KEY (`task_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `task_assignees_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`),
  CONSTRAINT `task_assignees_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_assignees`
--

LOCK TABLES `task_assignees` WRITE;
/*!40000 ALTER TABLE `task_assignees` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_assignees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(120) NOT NULL,
  `description` text,
  `deadline` datetime NOT NULL,
  `priority` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `created_by` int NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=256 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_preferences`
--

DROP TABLE IF EXISTS `user_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_preferences` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `email_notifications` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_preferences_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_preferences`
--

LOCK TABLES `user_preferences` WRITE;
/*!40000 ALTER TABLE `user_preferences` DISABLE KEYS */;
INSERT INTO `user_preferences` VALUES (1,39,0,'2025-06-27 08:36:35','2025-06-27 08:36:42'),(6,73,1,'2025-07-02 07:21:38','2025-07-02 07:21:38'),(7,74,1,'2025-07-04 07:41:05','2025-07-04 07:41:05');
/*!40000 ALTER TABLE `user_preferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `username` varchar(80) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `password` varchar(256) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `updated_at` datetime NOT NULL,
  `role` varchar(20) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `first_name` varchar(60) NOT NULL,
  `last_name` varchar(60) NOT NULL,
  `bio` text,
  `position` varchar(60) DEFAULT NULL,
  `company_name` varchar(120) DEFAULT NULL,
  `avatar_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (39,'saleemuddeen02@gmail.com','adminqcp',NULL,'2025-04-16 07:15:56','pbkdf2:sha256:1000000$vO3vupxMwYQdp2J2$c78e9834f42531be0f5f4e07422054fcea56a3bcd229e7fe74f841cd4470ea60',1,'2025-07-05 14:31:31','admin','2025-07-05 14:31:31','Admin','Qcp','Network engineer','Admin','Quality Control Print','20250627171116_67E0C5E6-B0EE-4C58-9256-D061F321FAE8.jpeg'),(73,'osagede@graduate.utm.my','managerqcp',NULL,'2025-07-02 07:21:34','pbkdf2:sha256:1000000$SQR7mIn5pHU4IdEa$1d699da12b28857efd2e2822f44dcce9598cb9d16a0c1c2a99e3899ffab683bb',1,'2025-07-04 15:00:55','manager','2025-07-04 15:00:38','Manager','Qcp',NULL,'Manager',NULL,NULL),(74,'saleemm1137@gmail.com','staffqcp','','2025-07-04 07:41:02','pbkdf2:sha256:1000000$v2YsfbqSVMZ1UYP3$6a3ca3eec86d9ce1271f3a8915d7b3804347c80894bd43332627fc46f808d03f',1,'2025-07-04 07:42:33','staff','2025-07-04 07:42:33','Staff','Qcp',NULL,'Staff',NULL,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `verifications`
--

DROP TABLE IF EXISTS `verifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `verifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `code` varchar(6) NOT NULL,
  `method` varchar(20) NOT NULL,
  `expires_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  `attempts` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_user_method` (`user_id`,`method`),
  CONSTRAINT `verifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=261 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `verifications`
--

LOCK TABLES `verifications` WRITE;
/*!40000 ALTER TABLE `verifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `verifications` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-05 23:29:11
