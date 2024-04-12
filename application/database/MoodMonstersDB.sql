CREATE TABLE Person (
    Person_ID INT AUTO_INCREMENT PRIMARY KEY,
    Firstname VARCHAR(255) NOT NULL,
    Lastname VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL,
    PIN INT
);

CREATE TABLE Grown_up (
    Grown_Up_ID INT AUTO_INCREMENT PRIMARY KEY,
    Person_ID INT NOT NULL,
    Firstname VARCHAR(255) NOT NULL,
    Lastname VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL,
    Relationship_to_Child VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    FOREIGN KEY (Person_ID) REFERENCES Person(Person_ID)
);


CREATE TABLE Child (
    Child_ID INT AUTO_INCREMENT PRIMARY KEY,
    Person_ID INT NOT NULL,
    Firstname VARCHAR(255) NOT NULL,
    Lastname VARCHAR(255) NOT NULL,
    Username VARCHAR(255) NOT NULL,
    Grown_Up_ID INT NOT NULL,
    Age INT NOT NULL,
    SCHOOL_YEAR INT NOT NULL,
    FOREIGN KEY (Person_ID) REFERENCES Person(Person_ID)
    FOREIGN KEY (Grown_Up_ID_ID) REFERENCES Grown_Up(Grown_Up_ID)
);



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

INSERT INTO Person 
VALUES 
(1, 'John', 'Smith', 'jsmith', 1234), 
(2, 'Emily', 'Smith', 'emilys', 1234),
(3, 'Michael', 'Johnson', 'mjohnson', 2312),
(4, 'Sarah', 'Johnson', 'sarahj', 2312),
(5, 'David', 'Brown', 'dbrown', 5678),
(6, 'Olivia', 'Brown', 'oliviab', 5678),
(7, 'Jane', 'Davis', 'jdavis', 2345),
(8, 'Jacob', 'Davis', 'jacobd', 2345),
(9, 'Emma', 'Wilson', 'ewilson', 2376),
(10, 'William', 'Wilson', 'wwilson', 2376),
(11, 'Ava', 'Martinez', 'avam', 4444),
(12, 'Alexander', 'Martinez', 'alexm', 4444);

INSERT INTO Child (Firstname, Lastname, Parent_ID, Age, School_Year)
VALUES 
('Emily', 'Smith', 1, 6, 1),
('Sarah', 'Johnson', 3, 8, 4),
('Olivia', 'Brown', 5, 7, 3),
('Jane', 'Davis', 7, 8, 3),
('Emma', 'Wilson', 9, 6, 1),
('Alexander', 'Martinez', 11, 6, 1),
('Vanessa', 'Martinez', 11, 8, 4);

INSERT INTO Grown_up (Person_ID, Relationship_to_Child, Email)
VALUES 
(1, 'Dad', 'jsmith@hotmail.com'),
(3, 'Brother', 'mjohnson@gmail.com'),
(5, 'Teacher', 'dbrown@hotmail.co.uk'),
(7, 'Mum', 'jdavis@yahoo.co.uk'),
(9, 'Teacher', 'ewilson@hotmail.com'),
(11, 'Mum', 'alexm@hotmail.co.uk');



