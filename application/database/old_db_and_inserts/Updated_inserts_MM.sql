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
INSERT INTO activity(activity_name, activity_image_url, description, instructions)
VALUES
("Write in your journal", "images/journal_entry.jpeg", "Writing down the things that make us feel bad, can help us to thing of ways to overcome them and ask for help", "Write down the things that are making you feel the way you do in the form below. Or use the button to print off a page to write at home. When you have finished, show your entry to your grown-up so they can help you to feel better"),
("Dance Activity", "images/dance_activity.jpg", "Dancing releases happy hormones (called endorphins)", "Play your favourite song and dance! Ask your grown-up to dance too - that might make you laugh!"),
("Bubble Breathing Activity", "images/breathing_activity.jpg", "Special breathing exercises can calm down our minds and help make our mood better",  "Imagine you are creating a big bubble. Take a deep breath in, and then a long slow breath out to blow that giant bubble into the air"),
("54321 Sensory Activity", "images/54321_sensory_activity.jpg", "Sensory activities allow you to focus on things in front of you and calm your mood", "Name 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste"),
("Jungle Activity", "images/jungle_activity.jpg", "Pretending to be animals is fun and can make us feel happy when we are having a bad day", "Imagine you are a jungle animal, move around your room like you are that animal. Make the animal noises. Be loud! Ask your grown-up to join in and have fun!"),
("Space Activity", "images/space_activity.jpg", "Space is a very calm place, pretending to be in space can give us a break from the things that are not making us happy", "Imagine you are floating in space. Lie on the floor and close your eyes. Take deep breaths in and out, relax and imagine floating around, seeing the stars"),
("Superhero Activity", "superhero_activity.jpg", "Superheroes have magic powers that can help them to deal with their problems", "Imagine you are a superhero. What would your magic power be? Run around as your superhero using your magic power! Ask your grown-up to be a superhero too!");

SELECT * FROM activity;


-- INSERTED ACTIVITY AND MOOD TABLE WITH NO VALUES AT THIS STAGE
INSERT INTO mood_and_activity (mood_id, activity_id)
VALUES
(2, 2),
(2, 4),
(2, 5),
(2, 6),
(2, 7),
(3, 3),
(3, 4),
(3, 5),
(3, 6),
(3, 7),
(4, 3),
(4, 4),
(4, 5),
(4, 6),
(4, 7);

SELECT * FROM mood_and_activity;


INSERT INTO message (child_id, grown_up_id, message)
VALUES ();
