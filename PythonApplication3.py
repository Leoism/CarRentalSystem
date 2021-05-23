#!/usr/bin/python
import file1
import psycopg2
import threading
import requests
from flask import Flask, render_template, request
# from config import config

app = Flask(__name__, template_folder='templates')

@app.route("/")
def connect():
    tempy = ''
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(dbname="db01", user="postgres", password="password")

        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        # print('PostgreSQL database version:')
        # cur.execute('SELECT version()')
        cur.execute('SELECT * FROM EMPLOYEE;') # FORMAT: (1) generate connection cursor, (2) execute query, (3) fetchall, (4) print

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
        tempy = cur.fetchall() # take all rows from output
        print(tempy)
       
	    # close the communication with the PostgreSQL
        cur.close()
        # connect to HTML page
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Errored"
    if conn is not None:     
       print('Database connection closed.')
       conn.close()
       return render_template("index.html", tempy = tempy) # this is a bad idea.

@app.route('/employeeQ')
def employeeQ():
    e_name = request.args.get('name', default = '')
    tempy = ''
    conn = None
    try:
        conn = psycopg2.connect(dbname="db01", user="postgres", password="password")
        cur = conn.cursor()
        if e_name == '':
            print(e_name)
            print('AAAAAAA')
            cur.execute('SELECT * FROM EMPLOYEE;') # SELECT * FROM EMPLOYEE WHERE NAME = ""
        else:
            print(e_name)
            print('BBBBBBB')
            cur.execute('SELECT * FROM EMPLOYEE WHERE NAME = \'' + e_name + '\';')
        tempy = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Errored"
    if conn is not None:
        conn.close()
        return render_template("index.html", tempy = tempy)

@app.route('/meetingQ')
def meetingQ():
    tempy = ''
    conn = None
    try:
        conn = psycopg2.connect(dbname="db01", user="postgres", password="password")
        cur = conn.cursor()
        cur.execute('SELECT * FROM MEETING;')
        tempy = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Errored"
    if conn is not None:
        conn.close()
        return render_template("index.html", tempy = tempy)

@app.route('/attendeesQ')
def attendeesQ():
    tempy = ''
    conn = None
    try:
        conn = psycopg2.connect(dbname="db01", user="postgres", password="password")
        cur = conn.cursor()
        cur.execute('SELECT * FROM ATTENDEES;')
        tempy = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Errored"
    if conn is not None:
        conn.close()
        return render_template("index.html", tempy = tempy)


if __name__ == '__main__':
    threading.Thread(target=app.run).start()
    # connect()