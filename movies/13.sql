SELECT name FROM people WHERE NOT name = 'Kevin Bacon' AND id in
(SELECT DISTINCT person_id FROM stars WHERE movie_id IN
(SELECT movie_id FROM stars WHERE person_id IN
(SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = '1958'
)));