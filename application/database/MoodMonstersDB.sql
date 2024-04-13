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


CREATE TABLE badge (
    badge_id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    badge_name VARCHAR(255) NOT NULL,
    badge_description TEXT,
    date_awarded DATETIME DEFAULT CURRENT_TIMESTAMP,
    criteria TEXT,
    FOREIGN KEY (child_ID) REFERENCES child(child_ID)
);

SELECT * FROM badge;


CREATE TABLE mood (
    mood_id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    mood ENUM('Happy', 'Sad', 'Worried', 'Excited', 'Frustrated', 'Surprised', 'Scared') NOT NULL,
    date_logged DATETIME DEFAULT CURRENT_TIMESTAMP,
    describe_emotion TEXT,
    FOREIGN KEY (Child_ID) REFERENCES Child(Child_ID)
);

SELECT * FROM mood;


CREATE TABLE activity (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    activity_type ENUM('Coping Strategy', 'Communication', 'Journal Entry', 'Other') NOT NULL,
    date_completed DATETIME DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (child_id) REFERENCES child(child_id)
);




