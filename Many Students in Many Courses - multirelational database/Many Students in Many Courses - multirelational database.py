###This application will read roster data in JSON format, parse the file,
#and then produce an SQLite database that contains a User, Course, and Member table and populate the tables from the data file.
# It's also the assignment for course "Using Databases with Python - week 4"

import json
import sqlite3

conn = sqlite3.connect("rosterDB.sqlite")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE
);

CREATE TABLE Member(
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id, course_id)
)
""")

file_name = input("Enter file name: ")
if (len(file_name) < 1) : file_name = "roster_data.json"

string_data = open(file_name).read()
json_data = json.loads(string_data)

for entry in json_data:
    name = entry[0];
    title = entry[1];
    role = entry[2];

    print(name, title, role)

    cur.execute("""INSERT OR IGNORE INTO User (name) VALUES (?)""", (name, ))
    cur.execute("SELECT id FROM User Where name = ?", (name, ))
    user_id = cur.fetchone()[0]

    cur.execute("""INSERT OR IGNORE INTO Course (title) VALUES (?)""", (title, ))
    cur.execute("SELECT id FROM Course WHERE title = ?", (title, ))
    course_id = cur.fetchone()[0]

    cur.execute("""INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES (?, ?, ?)""", (user_id, course_id, role))

cur.execute("SELECT User.name, Course.title FROM User JOIN Course JOIN Member ON Member.user_id = User.id AND Member.course_id = Course.id ORDER BY Course.title, Member.role DESC, User.name")

###Run below command in DB BRowser to get final records for the assignment
#   SELECT hex(User.name || Course.title || Member.role) AS X FROM User JOIN Member JOIN Course ON User.id = Member.user_id AND Member.course_id = Course.id ORDER BY X

conn.commit()
