#!/usr/bin/env python2.7
# PYTHON 2
#
# Database access functions for the web analysis log
#

import psycopg2

# Creates txt file
f = []
f = open("logreader.txt", "a")


def dbConnect():
    # Database connection
    DBNAME = "news"
    try:
        db = psycopg2.connect(database=DBNAME)
    except:
        print "I am unable to connect to database"
    return db


def Q1():
    db = dbConnect()
    cur = db.cursor()
    cur.execute("""

SELECT articles.title,
       Count(*) AS views
FROM   articles,
       log
WHERE  log.path = Concat('/article/', articles.slug)
GROUP  BY articles.title
ORDER  BY views DESC
LIMIT  3;

     """)
    rows = cur.fetchall()
    print "\n What are the most popular three articles of all time? \n"
    f.write("\n What are the most popular three articles of all time? \n")
    for row in rows:
        print '"' + row[0] + '"' + " - " + str(row[1]) + " views"
        f.write('"' + row[0] + '"' + " - " + str(row[1]) + " views\n")
    db.close()


def Q2():
    db = dbConnect()
    cur = db.cursor()
    cur.execute("""

SELECT authors.NAME,
           Count(*) AS views
FROM   authors,
       articles,
       log
WHERE  articles.author = authors.id
       AND log.path = Concat('/article/', articles.slug)
GROUP  BY authors.NAME
ORDER  BY views DESC;

    """)
    rows = cur.fetchall()
    print "\n Who are the most popular article authors of all time? \n"
    f.write("\n Who are the most popular article authors of all time? \n")
    for row in rows:
        print str(row[0]) + " - " + str(row[1]) + " views"
        f.write(str(row[0]) + " - " + str(row[1]) + " views\n")
    db.close()


def Q3():
    db = dbConnect()
    cur = db.cursor()
    cur.execute('''

SELECT success.date, ((Cast(failure.count AS FLOAT) / (success.count +
        failure.count)) *
    100.0)
FROM
    (SELECT to_char(TIME, 'Mon DD, YYYY') AS date,
        Count(TIME) AS COUNT FROM log WHERE status = '200 OK'
        GROUP BY date)  AS success
JOIN
    (SELECT to_char(TIME, 'Mon DD, YYYY') AS date,
        Count(TIME) AS COUNT FROM log WHERE status != '200 OK'
        GROUP BY date) AS failure
        ON success.date = failure.date
WHERE((Cast(failure.count AS FLOAT) / (success.count + failure.count)) *
        100.0) > 1.0

    ''')
    rows = cur.fetchall()
    print "\n On which days did more than 1% of requests lead to errors?\n"
    f.write("\n On which days did more than 1% of requests lead to errors?\n")
    for row in rows:
        print str(row[0]) + " - " + str(round(row[1], 2)) + "%" + " errors"
        f.write(str(row[0]) + " - " +
                str(round(row[1], 2)) + "%" + " errors\n")
    db.close()


Q1()
Q2()
Q3()
f.close()# Closes text file
