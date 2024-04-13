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