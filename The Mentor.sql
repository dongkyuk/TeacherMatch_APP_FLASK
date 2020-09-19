CREATE TABLE `login` (
  `userID` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL
);

CREATE TABLE `user` (
  `id` varchar(255) UNIQUE PRIMARY KEY,
  `name` varchar(255) NOT NULL,
  `type` ENUM ('student', 'mentor', 'admin') NOT NULL,
  `phone` varchar(255) NOT NULL,
  `birthday` datetime NOT NULL,
  `location` varchar(255) NOT NULL,
  `data` json NOT NULL
);

CREATE TABLE `hashtag_following` (
  `userID` varchar(255) NOT NULL,
  `hashtag_id` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL
);

CREATE TABLE `hashtag_user` (
  `userID` varchar(255) NOT NULL,
  `hashtag_id` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL
);

CREATE TABLE `heart` (
  `id` varchar(255) UNIQUE PRIMARY KEY,
  `userID` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `used` boolean NOT NULL
);

CREATE TABLE `unlocked_profile` (
  `heartID` varchar(255) NOT NULL,
  `studentID` varchar(255) NOT NULL,
  `mentorID` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL
);

CREATE TABLE `match_request` (
  `id` varchar(255) UNIQUE PRIMARY KEY,
  `heartID` varchar(255) NOT NULL,
  `studentID` varchar(255) NOT NULL,
  `mentorID` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `fulfilled` boolean NOT NULL
);

CREATE TABLE `mock_class_request` (
  `matchID` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `fulfilled` boolean NOT NULL
);

ALTER TABLE `user` ADD FOREIGN KEY (`id`) REFERENCES `login` (`userID`);

ALTER TABLE `user` ADD FOREIGN KEY (`id`) REFERENCES `hashtag_following` (`userID`);

ALTER TABLE `user` ADD FOREIGN KEY (`id`) REFERENCES `hashtag_user` (`userID`);

ALTER TABLE `user` ADD FOREIGN KEY (`id`) REFERENCES `match_request` (`studentID`);

ALTER TABLE `user` ADD FOREIGN KEY (`id`) REFERENCES `match_request` (`mentorID`);

ALTER TABLE `user` ADD FOREIGN KEY (`id`) REFERENCES `unlocked_profile` (`studentID`);

ALTER TABLE `user` ADD FOREIGN KEY (`id`) REFERENCES `unlocked_profile` (`mentorID`);

ALTER TABLE `user` ADD FOREIGN KEY (`id`) REFERENCES `heart` (`userID`);

ALTER TABLE `heart` ADD FOREIGN KEY (`id`) REFERENCES `match_request` (`heartID`);

ALTER TABLE `heart` ADD FOREIGN KEY (`id`) REFERENCES `unlocked_profile` (`heartID`);

ALTER TABLE `match_request` ADD FOREIGN KEY (`id`) REFERENCES `mock_class_request` (`matchID`);
