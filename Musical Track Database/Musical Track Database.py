#This application will read an iTunes export file in XML and produce a properly normalized database

import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('trackDB.sqlite')
#creates new .sqlite file (if not exists already)
cur = conn.cursor()

###Below: creating tables for further processing
##Rows named with "id" in the end will be used for the making conntections between tables
cur.executescript("""
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;


CREATE TABLE Artist (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Genre (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    artist_id INTEGER
);

CREATE TABLE Track (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    genre_id INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);

""")

file_name = input("Enter file name: ")
if (len(file_name) , 1) : file_name = "Library.xml"

#Below: defining function that will be used to gather interesing data

def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == "key" and child.text == key :
            found = True
    return None

stuff = ET.parse(file_name)
# parsing xml file
all = stuff.findall("dict/dict/dict")
print (("Dict count:"), len (all))
for entry in all:
    if (lookup(entry, "Track ID") is None) : continue
    name = lookup(entry, "Name")
    artist = lookup(entry, "Artist")
    genre = lookup(entry, "Genre")
    album = lookup(entry, "Album")
    count = lookup(entry, "Play Count")
    rating = lookup(entry, "Rating")
    length = lookup(entry, "Total Time")

    if name is None or artist is None or genre is None or album is None :
        continue

    print (name, artist, genre, album, count, rating, length)
    ### prinitng requested info about each found track

    cur.execute("""INSERT OR IGNORE INTO Artist (name) VALUES (?)""", (artist, ))
    cur.execute("SELECT id FROM Artist WHERE name = ?", (artist, ))
    artist_id = cur.fetchone()[0]
    ### inserting and fetching gathered info to the tables

    cur.execute("""INSERT OR IGNORE INTO Genre (name) VALUES (?)""", (genre, ))
    cur.execute("SELECT id FROM Genre WHERE name = ?", (genre, ))
    genre_id = cur.fetchone()[0]


    cur.execute("""INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)""", (album, artist_id))

    cur.execute("SELECT id FROM Album WHERE title = ?", (album, ))
    album_id = cur.fetchone()[0]

    cur.execute("""INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count) VALUES (?, ?, ?, ?, ?, ?)""",
    (name, album_id, genre_id, length, rating, count))

    cur.execute("SELECT Track.title, Artist.name, Album.title, Genre.name FROM Track JOIN Genre JOIN Album JOIN Artist ON Track.genre_id = Genre.id AND Track.album_id = Album.id AND Album.artist_id = Artist.id ORDER BY Artist.name, Track.title LIMIT 3")
    ### Joining tables using naming convention (with "_id") used in the beginning. Also displays 3 top Artists (this commend has to be copied and pasted in DB Browser to check Assignment result)
    conn.commit()
