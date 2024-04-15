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


INSERT INTO badge (badge_name, badge_image_url, badge_description, criteria)
VALUES
("First Feelings Finder", "images/badge_first_feelings_finder.jpg", "Awarded for logging your mood for the first time.", "Child logs their mood in the app for the first time." ),
("Week of Wonders", "images/badge_week_of_wonders.jpg", "Celebrates a week of consistent mood logging.", "Child logs their mood every day for 5 consecutive days." ),
("Emotional Explorer", "images/badge_emotional_explorer.jpg", "Given for identifying and logging 2 different mood monsters in the app.", "Child has identified and logged 2 types of mood."),
("Chatter Champion", "images/badge_chatter_champion.jpg", "Rewards engaging with the app's coping strategies and communication activities.", "Child completes 1 communication activity "),
("Mood Master", "images/badge_mood_master.jpg", "Mastering mood identification skills.", "Child logs their mood 3 times."),
("Joyful Journalling", "images/badge_joyful_journalling.jpg", "Given for sharing feelings in the journal.", "Child uses the app to explore their feelings in the journal."),
("Happy Helper", "images/badge_happy_helper.jpg", "Celebrates using a suggested coping strategy to move from a negative to a positive mood.", "Child logs a negative mood, uses a suggested coping strategy, and subsequently logs a positive mood."),
("Brave Battler", "images/badge_brave_battler.jpg", "Awarded for logging feelings of worry and confronting them.", "Child logs feeling scared or worried and completes an activity to address these feelings.");

SELECT * FROM badge;


INSERT INTO activity (activity_name, mood_id)
VALUES
('Log Mood', NULL),
('Journal Entry', NULL),
('Communication Activity', NULL),
('Breathing Activity', NULL),
('Dance Activity', NULL);

SELECT * FROM activity;

INSERT INTO message (child_id, grown_up_id, message)
VALUES ();
