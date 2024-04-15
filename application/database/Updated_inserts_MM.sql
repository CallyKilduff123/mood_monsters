USE mood_monsters;

INSERT INTO family (shared_pin)
VALUES
(1234),
(2345),
(3456),
(4567),
(5678);

SELECT * FROM family;


INSERT INTO grown_up (family_id, first_name, last_name, username, email, relationship_to_child)
VALUES
(1, "Thomas", "Leith", "drtomo", "tl@gmail.com", "father"),
(2, "Nicholas", "Kilduff", "Nick", "nk@gmail.com", "father"),
(3, "Sophie", "Gray", "Duffy", "sg@hotmail.com", "mother"),
(4, "Jess", "O Brien", "jessob", "job@yahoo.com", "mother"),
(5, "Jess", "Muller", "mullz", "jm@outlook.co.uk", "teacher");

SELECT * FROM grown_up;


INSERT INTO child (family_id, first_name, last_name, username, date_of_birth)
VALUES
(1, "Evelyn", "Leith-Kilduff", "Elvie", '2017-10-11'),
(2, "Margaux", "Kilduff", "Gargoz", '2017-10-30'),
(3, "Louie", "Gray", "Poobear", '2018-01-08'),
(4, "Rose", "O Brien", "Rosie", '2017-12-01'),
(5, "Emma", "McBroom", "Em", '2017-09-12');


SELECT * FROM child;


INSERT INTO mood (mood_name, mood_image_url, mood_description)
VALUES
("Happy", "images/1_happy_monster.jpeg", "Being happy is like having a big smile because something really awesome happened, making you feel super excited and full of joy!"),
("Sad", "images/2_sad_monster.jpeg", "Feeling sad is like having a little raincloud over your head because something made you feel a bit down or upset."),
("Angry", "images/3_angry_monster.jpeg", "Feeling angry is like having a big fire inside because something made you feel really frustrated or mad."),
("Worried", "images/4_worried_monster.jpeg", "Feeling worried is like having butterflies in your tummy because you're thinking about something that makes you feel a little scared or unsure."),
("Ashamed", "images/5_mood_monster_ashamed.jpeg", "Feeling ashamed is like carrying a heavy backpack that no one else can see, because you think you did something wrong."),
("Lonely", "images/6_mood_monster_lonely.jpeg", "Feeling lonely is like floating alone on a little boat in a big lake. You see other boats around, but they seem too far away." );

SELECT * from mood;

-- CHANGED TO NEW BADGES  
INSERT INTO badge (badge_name, badge_image_url, badge_description, criteria)
VALUES
("Angry Author", "images/Angry_author_badge.jpg", "CONGRATULATIONS! You have completed a journal entry to address feeling angry.", "Awarded for completing a journal entry when feeling angry." ),
("Sad Scribbler", "images/Sad_scribbler_badge.jpg", "WELL DONE! You have completed a journal entry to address feeling sad.", "Awarded for completing a journal entry when feeling sad." ),
("Worried Wordsmith", "images/Worried_wordsmith.jpg", "AWESOME! You have completed a journal entry to address feeling worried.", "Awarded for completing a journal entry when feeling worried."),
("Angry Air Breather", "images/Angry_air_breather_badge.jpg", "FANTASTIC! You have completed the breathing activity to combat feeling angry.", "Awarded for doing a breathing activity when feeling angry."),
("Sad Steps Dancer", "images/Sad_steps_dancer_badge.jpg", "HURRAY! You have completed the dance activity to combat feeling sad.", "Awarded for participating in a dance activity when feeling sad."),
("Worried Warrior’s 5-4-3-2-1", "images/Worried_warrior_54321_badge.jpg", "BRILLIANT! You have completed the 5-4-3-2-1 sensory activity to combat feeling angry.", "Awarded for engaging in a 5-4-3-2-1 sensory activity when feeling worried.");

SELECT * FROM badge;

-- UPDATED ACTIVITY TABLE  
INSERT INTO activity (activity_name)
VALUES
('Log Mood'),
('Journal Entry'),
('54321 Activity'),
('Breathing Activity'),
('Dance Activity');

SELECT * FROM activity;

-- INSERTED ACTIVITY AND MOOD TABLE WITH NO VALUES AT THIS STAGE
INSERT INTO activity_and_mood(activity_id, mood_id)
VALUES();


INSERT INTO message (child_id, grown_up_id, message)
VALUES ();
