CREATE DATABASE mood_monsters;

USE mood_monsters;


CREATE TABLE family (
    family_id INT AUTO_INCREMENT PRIMARY KEY,
    shared_pin VARCHAR(255) NOT NULL
);

SELECT * FROM family;


CREATE TABLE grown_up (
    grown_up_id INT AUTO_INCREMENT PRIMARY KEY,
    family_id INT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    relationship_to_child VARCHAR(100) NOT NULL,
    FOREIGN KEY (family_id) REFERENCES family(family_id)
);

SELECT * FROM grown_up;


CREATE TABLE child (
    child_id INT AUTO_INCREMENT PRIMARY KEY,
    family_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    FOREIGN KEY (family_id) REFERENCES family(family_id)
);

SELECT * FROM child;


CREATE TABLE message (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    grown_up_id INT NOT NULL,
    message VARCHAR(255),
    date_sent DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES child(child_id),
    FOREIGN KEY (grown_up_id) REFERENCES grown_up(grown_up_id)
);

SELECT * FROM message;



CREATE TABLE mood (
    mood_id INT AUTO_INCREMENT PRIMARY KEY,
    mood_name ENUM('Happy', 'Sad', 'Worried', 'Ashamed', 'Angry', 'Lonely') NOT NULL,
    mood_image_url VARCHAR(255) Default null,
    mood_description TEXT
);

SELECT * FROM mood;


CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT,
    message_id INT,
    date_logged TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (child_id) REFERENCES child(child_id),
    FOREIGN KEY (message_id) REFERENCES message(message_id)
);

SELECT * FROM notifications;


CREATE TABLE mood_logged (
mood_logged_id INT AUTO_INCREMENT PRIMARY KEY,
mood_id INT NOT NULL,
child_id INT NOT NULL,
date_logged DATETIME DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (child_id) REFERENCES child(child_id),
FOREIGN KEY (mood_id) REFERENCES mood(mood_id)
);

SELECT * FROM mood_logged;


CREATE TABLE badge (
    badge_id INT AUTO_INCREMENT PRIMARY KEY,
    badge_name VARCHAR(255) NOT NULL,
    Badge_image_url  VARCHAR(255) Default null,
    badge_description TEXT,
    criteria TEXT
);

SELECT * FROM badge;



CREATE TABLE activity (
   activity_id INT AUTO_INCREMENT PRIMARY KEY,
   activity_name VARCHAR(255) NULL,
   activity_image_url VARCHAR(255) NULL,
   description VARCHAR(255) NULL,
   instructions VARCHAR(255) NULL
);

SELECT * FROM activity;


CREATE TABLE mood_and_activity (
    mood_and_activity_id INT AUTO_INCREMENT PRIMARY KEY,
    activity_id INT NOT NULL,
    mood_id INT NOT NULL,
    FOREIGN KEY (mood_id) REFERENCES mood(mood_id),
    FOREIGN KEY (activity_id) REFERENCES activity(activity_id)
);

SELECT * FROM mood_and_activity;


CREATE TABLE track_activity (
    	track_activity_id INT AUTO_INCREMENT PRIMARY KEY,
    	child_id INT NOT NULL,
    	mood_logged_id INT NOT NULL,
        mood_id INT NOT NULL,
        activity_id INT NOT NULL,
        journal_text TEXT DEFAULT NULL,
    	date_completed DATETIME DEFAULT CURRENT_TIMESTAMP,
    	FOREIGN KEY (child_id) REFERENCES child(child_id),
    	FOREIGN KEY (mood_logged_id) REFERENCES mood_logged(mood_logged_id),
        FOREIGN KEY (mood_id) REFERENCES mood(mood_id),
    	FOREIGN KEY (activity_id) REFERENCES activity(activity_id)
);


CREATE TABLE badge_criteria (
    criteria_id INT AUTO_INCREMENT PRIMARY KEY,
    badge_id INT NOT NULL,
    mood_id INT,
    activity_id INT,
    FOREIGN KEY (badge_id) REFERENCES badge(badge_id),
    FOREIGN KEY (mood_id) REFERENCES mood(mood_id),
    FOREIGN KEY (activity_id) REFERENCES activity(activity_id)
);

SELECT * FROM badge_criteria;


CREATE TABLE badge_progress (
    badge_progress_id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    badge_id INT NOT NULL,
    track_activity_id INT NOT NULL,
    date_completed DATETIME,
    award_badge BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (child_id) REFERENCES child(child_id),
    FOREIGN KEY (badge_id) REFERENCES badge(badge_id),
    FOREIGN KEY (track_activity_id) REFERENCES track_activity(track_activity_id)
);

SELECT * FROM badge_progress;

