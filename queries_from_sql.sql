CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER REFERENCES status (id) ON DELETE CASCADE ON UPDATE CASCADE,
    user_id INTEGER REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
);

select * from users;
SELECT * 
FROM tasks 
WHERE user_id = 1;
select name = 'In Progress'  from status;
select * from tasks;
UPDATE tasks
SET status_id = 3
WHERE id = 1;
SELECT u.id, u.fullname, u.email
FROM users u
WHERE u.id NOT IN (
    SELECT t.user_id
    FROM tasks t
    WHERE t.user_id IS NOT NULL
);
INSERT INTO tasks (title, description, status_id, user_id)
VALUES ('New task', 'This is a description for the new task', 1, 10);
SELECT * 
FROM tasks 
WHERE status_id = (
    SELECT id 
    FROM status 
    WHERE name = 'new'
); -- changed
delete from tasks where id = '1'; -- changed
SELECT * 
FROM tasks 
WHERE status_id != (
    SELECT id 
    FROM status 
    WHERE name = 'completed'
); -- added
SELECT * 
FROM tasks 
WHERE description IS NULL; -- added
select email, id, fullname
from users
where email like '%wmeyer%'
;
UPDATE users
SET fullname = 'Vasyl'
WHERE id = 5;
select COUNT(id)
from tasks
group by status_id;

SELECT t.*
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.net%';
select *
from tasks
where id is null;

select u.*
from users u
inner join tasks t on u.id = t.user_id
where status_id = '2';

SELECT u.id, u.fullname, COUNT(t.id) AS task_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id, u.fullname;