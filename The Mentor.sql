CREATE TABLE `user` (
  `id` varchar(255) UNIQUE PRIMARY KEY,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `userType` ENUM ('student', 'mentor', 'admin') NOT NULL,
  `phone` varchar(255) NOT NULL,
  `birthday` datetime NOT NULL,
  `location` varchar(255) NOT NULL,
  `data` json NOT NULL
);

CREATE TABLE `hashtag_following` (
  `user_id` varchar(255) NOT NULL,
  `hashtag_id` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL,
   FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE `hashtag_user` (
  `user_id` varchar(255) NOT NULL,
  `hashtag_id` varchar(255) NOT NULL,
  `content` varchar(255) NOT NULL,
   FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE `heart` (
  `id` varchar(255) UNIQUE PRIMARY KEY,
  `user_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `used` boolean NOT NULL
);

CREATE TABLE `unlocked_profile` (
  `heart_id` varchar(255) NOT NULL,
  `student_id` varchar(255) NOT NULL,
  `mentor_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  FOREIGN KEY(student_id) REFERENCES user(id),
  FOREIGN KEY(mentor_id) REFERENCES user(id),
  FOREIGN KEY(heart_id) REFERENCES heart(id)
);

CREATE TABLE `match` (
  `id` varchar(255) UNIQUE PRIMARY KEY,
  `heart_id` varchar(255) NOT NULL,
  `student_id` varchar(255) NOT NULL,
  `mentor_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `fulfilled` boolean NOT NULL,
  FOREIGN KEY(student_id) REFERENCES user(id),
  FOREIGN KEY(mentor_id) REFERENCES user(id),
  FOREIGN KEY(heart_id) REFERENCES heart(id)
);

CREATE TABLE `mock_class_request` (
  `match_id` varchar(255) NOT NULL,
  `timestamp` datetime NOT NULL,
  `fulfilled` boolean NOT NULL,
  FOREIGN KEY(match_id) REFERENCES match(id)
);
