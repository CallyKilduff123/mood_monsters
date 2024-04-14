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
    mood_name ENUM('Happy', 'Sad', 'Worried', 'Excited', 'Frustrated', 'Surprised', 'Scared') NOT NULL,
    mood_image_url VARCHAR(255) Default null,
    mood_description TEXT
);

SELECT * FROM mood;



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
   activity_name ENUM('Log Mood', 'Journal Entry’, ‘Communication Activity’, ‘Breathing Activity’, ‘Dance Activity') NOT NULL,
);

SELECT * FROM activity;



CREATE TABLE track_activity (
    track_activity_id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    activity_id INT NOT NULL,
    mood_id INT DEFAULT NULL,
    date_completed DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES child(child_id),
    FOREIGN KEY (activity_id) REFERENCES action(activity_id),
    FOREIGN KEY (mood_id) REFERENCES mood(mood_id)
);

SELECT * FROM track_activity;



CREATE TABLE badge_progress (
    progress_id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    badge_id INT NOT NULL,
    activity_id INT DEFAULT NULL,  -- Links to specific activities that contribute to this badge
    track_activity_id INT DEFAULT NULL,  -- New addition: Links to specific actions directly related to badge criteria
    is_completed BOOLEAN DEFAULT FALSE,
    date_completed DATETIME,
    FOREIGN KEY (child_id) REFERENCES child(child_id),
    FOREIGN KEY (badge_id) REFERENCES badge(badge_id),
    FOREIGN KEY (activity_id) REFERENCES activity(activity_id),  -- Link to the activity that contributes to badge earning
    FOREIGN KEY (track_activity_id) REFERENCES action(track_activity_id)  -- Link to the specific action that contributes to badge earning
);

SELECT * FROM badge_progress;

