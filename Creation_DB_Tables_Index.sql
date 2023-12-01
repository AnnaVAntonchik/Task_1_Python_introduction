-- Creation of database
CREATE DATABASE postgres;

-- Creation of table rooms
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    "name" varchar(50)
);

-- Creation of table students
CREATE TABLE students(
	id SERIAL PRIMARY KEY,
    "name" varchar(200),
    birthday timestamp,
    room int,
    sex varchar(1)
);

-- Creation of index for students(room) for increase of join speed
CREATE INDEX idx_students_room ON students(room);
