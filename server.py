#!/usr/bin/python
from hashlib import new
import psycopg2
import json
from flask import Flask, render_template, request
from datetime import datetime, timedelta
import time
import random

# from config import config

app = Flask(__name__, template_folder='templates')
# Allows us to not have to restart Flask on every change
# Flask will automatically restart
app.debug = True
f = open('./keys.json')
options = json.load(f)
f.close()

@app.route("/")
def connect():
    rows = ''
    """ Connect to the PostgreSQL database server """
    conn = None
    column_names = None
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(dbname=options['dbname'], user=options['user'], password=options['password'])

        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        # print('PostgreSQL database version:')
        # cur.execute('SELECT version()')
        cur.execute('SELECT * FROM EMPLOYEE;') # FORMAT: (1) generate connection cursor, (2) execute query, (3) fetchall, (4) print

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
        rows = cur.fetchall() # take all rows from output
        print(rows)
        # Get the column names of the table
        cur.execute("SELECT * FROM EMPLOYEE LIMIT 0;")
        column_names = [desc[0] for desc in cur.description]
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
       return render_template("index.html", rows=rows, column_names=column_names) # this is a bad idea.

@app.route('/employeeQ')
def employeeQ():
    e_name = request.args.get('name', default = '')
    rows = ''
    conn = None
    column_names = None
    try:
        conn = psycopg2.connect(dbname=options['dbname'], user=options['user'], password=options['password'])
        cur = conn.cursor()
        if e_name == '':
            print(e_name)
            print('AAAAAAA')
            cur.execute('SELECT * FROM EMPLOYEE;') # SELECT * FROM EMPLOYEE WHERE NAME = ""
        else:
            print(e_name)
            print('BBBBBBB')
            cur.execute('SELECT * FROM EMPLOYEE WHERE NAME = \'' + e_name + '\';')
        rows = cur.fetchall()
        cur.execute("SELECT * FROM EMPLOYEE LIMIT 0;")
        column_names = [desc[0] for desc in cur.description]

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Errored"
    if conn is not None:
        conn.close()
        return render_template("index.html", rows=rows, column_names=column_names)

@app.route('/meetingQ')
def meetingQ():
    rows = ''
    conn = None
    column_names = None
    try:
        conn = psycopg2.connect(dbname=options['dbname'], user=options['user'], password=options['password'])
        cur = conn.cursor()
        cur.execute('SELECT * FROM MEETING;')
        rows = cur.fetchall()
        cur.execute("SELECT * FROM MEETING LIMIT 0;")
        column_names = [desc[0] for desc in cur.description]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Errored"
    if conn is not None:
        conn.close()
        return render_template("index.html", rows=rows, column_names=column_names)

@app.route('/attendeesQ')
def attendeesQ():
    rows = ''
    conn = None
    column_names = None
    try:
        conn = psycopg2.connect(dbname=options['dbname'], user=options['user'], password=options['password'])
        cur = conn.cursor()
        cur.execute('SELECT * FROM ATTENDEES;')
        rows = cur.fetchall()
        cur.execute("SELECT * FROM ATTENDEES LIMIT 0;")
        column_names = [desc[0] for desc in cur.description]

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Errored"
    if conn is not None:
        conn.close()
        return render_template("index.html", rows=rows, column_names=column_names)

@app.route('/add_rating', methods=['POST'])
def add_rating():
    query = """ INSERT INTO RatingRecord (CarID, rentalNumber, rating)
                VALUES ((SELECT Car.ID FROM Car WHERE Car.VIN = %s), %s , %s);"""
    values = request.json
    conn = None
    try:
        conn = psycopg2.connect(
                    dbname=options['dbname'],
                    user=options['user'],
                    password=options['password'])
        cur = conn.cursor()
        cur.execute(query, (values['carVIN'], values['rentalNumber'], values['rating'],))
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Error"
    if conn is None:
        conn.close()
    return "Successfully rented"

if __name__ == '__main__':
    app.run()
    # connect()