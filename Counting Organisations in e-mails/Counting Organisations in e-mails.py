
##This application will read the mailbox data (mbox.txt) count up the number email messages per organization (i.e. domain name of the email address) using a database with the following schema to maintain the counts.

import sqlite3

conn = sqlite3.connect('Organisations_Count.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (count INTEGER, org TEXT)''')

fname = input('Enter file name: ')
### enter the following file name: mbox.txt
if ( len(fname) < 1 ) : fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: ') : continue
    pieces = line.split()
    ###splitting using "whitespace"
    email = pieces[1]
    domain = email.split("@")
    ### spliting using "@"
    org = domain[1]
    print ("Checking address in domain:", org)
    ###line above will print all domain names that will be included in the final database
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES ( ?, 1 )''', ( org, ) )
    else :
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
            (org, ))
    # Loop statements above will add domain names and their count to the database (date will be entered to the database after loop ends - see line below)
conn.commit()

sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
#selecting and ordering by domain count (top 10)

print ("Domain Name and Total Counts: ")
for row in cur.execute(sqlstr) :
    print (str(row[0]), row[1])
# printing results

cur.close()
