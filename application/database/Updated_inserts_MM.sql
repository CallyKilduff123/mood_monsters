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
(4, "Rose", "O Brien", "Ro Ro", '2017-12-01'),
(5, "Emma", "McBroom", "Em", '2017-09-12'),
(5, "Gus", "McBroom", "Gus", '2018-01-01');

SELECT * FROM child;

INSERT INTO badge (badge_id, badge_image, badge_name, badge_description, criteria)
VALUES
(1, "images/badge_first_feelings_finder.jpg", "First Feelings Finder", " Awarded for logging your mood for the first time.", "Child logs their mood in the app for the first time." ),
(2, "images/badge_week_of_wonders.jpg", "Week of Wonders", "Celebrates a week of consistent mood logging.", "Child logs their mood every day for 5 consecutive days." ),
(3, "images/badge_emotional_explorer.jpg", "Emotional Explorer", "Given for identifying and logging 2 different mood monsters in the app.", "Child has identified and logged 2 types of mood."),
(4, "images/badge_chatter_champion.jpg", "Chatter Champion", "Rewards engaging with the app's coping strategies and communication activities.", "Child completes 1 communication activity "),
(5, "images/badge_mood_master.jpg", "Mood Master", "Mastering mood identification skills.", "Child logs their mood 3 times."),
(6, "images/badge_joyful_journalling.jpg", "Joyful Journalling", "Given for sharing feelings in the journal.", "Child uses the app to explore their feelings in the journal."),
(7, "images/badge_happy_helper.jpg", "Happy Helper", "Celebrates using a suggested coping strategy to move from a negative to a positive mood.", "Child logs a negative mood, uses a suggested coping strategy, and subsequently logs a positive mood."),
(8, "images/badge_brave_battler.jpg", "Brave Battler", "Awarded for logging feelings of worry and confronting them.", "Child logs feeling scared or worried and completes an activity to address these feelings.");


SELECT * FROM badge;


INSERT INTO mood (mood_id, mood_image, mood, describe_emotion) 
VALUES 
(1, "images/1_happy_monster.jpeg", "Happy", "Being happy is like having a big smile because something really awesome happened, making you feel super excited and full of joy!"), 
(2, "images/2_sad_monster.jpeg", "Sad", "Feeling sad is like having a little raincloud over your head because something made you feel a bit down or upset."),
(3, "images/3_angry_monster.jpeg", "Angry", "Feeling angry is like having a big fire inside because something made you feel really frustrated or mad."),
(4, "images/4_worried_monster.jpeg", "Worried", "Feeling worried is like having butterflies in your tummy because you're thinking about something that makes you feel a little scared or unsure."), 
(5, "images/5_mood_monster_frustrated.jpeg", "Frustrated", "Feeling frustrated is like having a knot in your tummy because something is not going the way you want it to, and it makes you feel a bit annoyed or upset."),
(6, "images/6_mood_monster_lonely.jpeg", "Lonely", "Feeling lonely is like feeling sad because you miss having someone to play or talk with." );

SELECT * from mood;

