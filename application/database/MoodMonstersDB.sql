CREATE DATABASE mood_monsters;

USE mood_monsters;

CREATE TABLE family (
    family_id INT AUTO_INCREMENT PRIMARY KEY,
    shared_pin VARCHAR(255) NOT NULL
);

--SELECT * FROM family;

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

--SELECT * FROM grown_up;


CREATE TABLE child (
    child_id INT AUTO_INCREMENT PRIMARY KEY,
    family_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    FOREIGN KEY (family_id) REFERENCES family(family_id)
);

--SELECT * FROM child;

CREATE TABLE Message (
    Message_ID INT AUTO_INCREMENT PRIMARY KEY,
    Receiver_ID INT NOT NULL,
    Sender_ID INT NOT NULL,
    Message VARCHAR(255),
    Date_Sent DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Receiver_ID) REFERENCES Child(Child_ID),
    FOREIGN KEY (Sender_ID) REFERENCES Grown_Up(Grown_Up_ID)
);

CREATE TABLE Badge (
    Badge_ID INT AUTO_INCREMENT PRIMARY KEY,
    Child_ID INT NOT NULL,
    Badge_Name VARCHAR(255) NOT NULL,
    Badge_Description TEXT,
    Date_Awarded DATETIME DEFAULT CURRENT_TIMESTAMP,
    Criteria TEXT,
    FOREIGN KEY (Child_ID) REFERENCES Child(Child_ID)
);

CREATE TABLE Mood (
    Mood_ID INT AUTO_INCREMENT PRIMARY KEY,
    Child_ID INT NOT NULL,
    Mood ENUM('Happy', 'Sad', 'Worried', 'Excited', 'Frustrated', 'Surprised', 'Scared') NOT NULL,
    Date_Logged DATETIME DEFAULT CURRENT_TIMESTAMP,
    Describe_Emotion TEXT,
    FOREIGN KEY (Child_ID) REFERENCES Child(Child_ID)
);

--INSERT INTO Person
--VALUES
--(1, 'John', 'Smith', 'jsmith', 1234, '2'),
--(2, 'Emily', 'Smith', 'emilys', NULL, '1'),
--(3, 'Michael', 'Johnson', 'mjohnson', 2222, '2'),
--(4, 'Sarah', 'Johnson', 'sarahj', NULL, '1'),
--(5, 'David', 'Brown', 'dbrown', 2001, '2'),
--(6, 'Olivia', 'Brown', 'oliviab', NULL, '1'),
--(7, 'Jane', 'Davis', 'jdavis', 5678, '2'),
--(8, 'Jacob', 'Davis', 'jacobd', NULL, '1'),
--(9, 'Emma', 'Wilson', 'ewilson', 2561, '2'),
--(10, 'William', 'Wilson', 'wwilson', NULL, '1'),
--(11, 'Ava', 'Martinez', 'avam', 1122, '2'),
--(12, 'Alexander', 'Martinez', 'alexm', NULL, '1'),
--(13, 'Vanessa', 'Martinez', 'vanm', NULL, '1');
--
--INSERT INTO Child (Firstname, Lastname, Parent_ID, Age, School_Year)
--VALUES
--('Emily', 'Smith', 1, 6, 1),
--('Sarah', 'Johnson', 3, 8, 4),
--('Olivia', 'Brown', 5, 7, 3),
--('Jane', 'Davis', 7, 8, 3),
--('Emma', 'Wilson', 9, 6, 1),
--('Alexander', 'Martinez', 11, 6, 1),
--('Vanessa', 'Martinez', 11, 8, 4);
--
--INSERT INTO Grown_up (Person_ID, Relationship_to_Child, Email)
--VALUES
--(1, 'Dad', 'jsmith@hotmail.com'),
--(3, 'Brother', 'mjohnson@gmail.com'),
--(5, 'Teacher', 'dbrown@hotmail.co.uk'),
--(7, 'Mum', 'jdavis@yahoo.co.uk'),
--(9, 'Teacher', 'ewilson@hotmail.com'),
--(11, 'Mum', 'alexm@hotmail.co.uk');


