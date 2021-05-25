#!/usr/bin/python
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
        cur.execute('SELECT * FROM car;') # FORMAT: (1) generate connection cursor, (2) execute query, (3) fetchall, (4) print

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
        rows = cur.fetchall() # take all rows from output
        print(rows)
        # Get the column names of the table
        cur.execute("SELECT * FROM car LIMIT 0;")
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

@app.route('/rate', methods=['GET'])
def rate_form():
    return render_template('rate.html')

@app.route('/add_rating', methods=['POST'])
def add_rating():
    """
        Values received must be a JSON containing Car information, RentalRecord information, and rating.
        Creates rating associated with the rental and car being reviewed.
    """
    query = """ INSERT INTO RatingRecord (CarID, rentalNumber, rating)
                VALUES ((SELECT Car.ID FROM Car WHERE Car.VIN = %s), %s , %s);"""
    values = request.json
    # extract customer
    rental_record = values['rental_record']
    # and car objects from the json
    car = values['car']
    conn = None
    try:
        conn = psycopg2.connect(
                    dbname=options['dbname'],
                    user=options['user'],
                    password=options['password'])
        cur = conn.cursor()
        cur.execute(query, (car['vin'], rental_record['rental_number'], values['rating'],))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Error", 500
    if conn is not None:
        conn.close()
    return "Successfully rated", 201

@app.route('/rent', methods=['GET'])
def rental_form():
    return render_template('rent.html')

@app.route('/create_rental', methods=['POST'])
def create_rental():
    """
        Creates a rental record associated with the Customer and the Car.
        If the car is not available, returns false. Otherwise, creates the rental
        record, and updates the availability of the car.
    """
    # Get the current date for which the customer is starting the rent
    today = datetime.now()
    values = request.json
    # extract customer
    customer = values['customer']
    # and car objects from the json
    car = values['car']
    conn = None
    cur = None
    # First we must check that the car is available
    check_avail_query = """
        SELECT availability
        FROM Car
        WHERE Car.availability = 'true' AND Car.VIN = %s;
    """
    try:
        conn = psycopg2.connect(
                    dbname=options['dbname'],
                    user=options['user'],
                    password=options['password'])
        cur = conn.cursor()
        cur.execute(check_avail_query, (car['vin'],))
        avail_car = cur.fetchall()
        # Ensure that the car is available
        if len(avail_car) != 1 or avail_car[0][0] is not True:
            return "Car is not available", 500
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Error", 500

    # Second, we must create a rental record and a rental number
    rent_query = """
        INSERT INTO RentalRecord (CarID, CustomerID, carRented, expectedReturn, rentalNumber)
        VALUES ((SELECT Car.ID FROM Car WHERE Car.VIN = %(car_vin)s),
        (SELECT Customer.ID FROM Customer
        WHERE Customer.firstName = %(f_name)s
            AND Customer.lastName = %(l_name)s
            AND Customer.birthDate = %(b_day)s), 
        %(todays_date)s, %(expected_ret)s, %(rental_num)s);
        """
    try:
        cur.execute(rent_query, {
            'car_vin': car['vin'],
            'f_name': customer['first_name'], 
            'l_name': customer['last_name'],
            'b_day': customer['birthdate'],
            'todays_date': str(today),
            # rental_length must be in days
            'expected_ret': str(today + timedelta(days=values['rental_length'])),
            'rental_num': _generate_number(16)
        })
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Error", 500

    # Finally, we must update the availability of the car
    update_avail = """
        UPDATE Car
        SET availability = 'false'
        WHERE Car.VIN = %s;
        """
    try:
        # update the availability of the car to be unavialable
        cur.execute(update_avail, (car['vin'],))
        conn.commit()
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Error", 500
    return "SUCCESS", 201

"""
    Generates a random number containing both numbers and letters of size length. 
"""
def _generate_number(length):
    # Turn string to list to allow inserting at the front
    new_ren_num = list(str(int(time.time())))[::-1]
    # ensure the length is greater than the timestamp length
    if (length < len(new_ren_num)):
        raise ValueError("Invalid length")
    # determine the amount of alpha characters to add to the number
    alpha_size = length - len(new_ren_num)
    alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # add alpha characters to the front of the string
    for i in range(alpha_size):
        new_ren_num.insert(0, alpha[random.randint(0, len(alpha) - 1)])
    # convert the list back to a string
    new_ren_num = ''.join(new_ren_num)

    rental_query = """
        SELECT rentalNumber
        FROM RentalRecord;
    """
    try:
        conn = psycopg2.connect(
                    dbname=options['dbname'],
                    user=options['user'],
                    password=options['password'])
        cur = conn.cursor()
        cur.execute(rental_query)
        rental_records = cur.fetchall()
        # go through every rental records rental number to ensure we have a unique number
        for rental_record in rental_records:
            for rental_number in rental_record:
                # if the new rental number is not unique, shuffle the number until it is unique
                while rental_number == new_ren_num:
                    new_ren_num = ''.join(random.sample(new_ren_num, len(new_ren_num)))
        conn.close()
        # if the number is unique, return it
        return new_ren_num
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return None

@app.route('/add_customer', methods=["POST"])
def add_customer():
    values = request.json
    addCustomerQuery = """
        INSERT INTO Customer (firstname, lastname, birthdate, street, city, state)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    conn = None
    try:
        conn = psycopg2.connect(
                    dbname=options['dbname'],
                    user=options['user'],
                    password=options['password'])
        cur = conn.cursor()
        cur.execute(addCustomerQuery, (values['fName'], values['lName'], values['bDay'], values['street'], values['city'], values['state'],))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Error", 500
    return "success", 201

@app.route('/customer', methods=["GET"])
def renderCustomer():
    return render_template("addCustomer.html")

@app.route('/update_availability_status', methods=["PUT"])
def update_availability_status():
    values = request.json
    updateStatusQuery = """
        UPDATE Car
        SET availability = %s
        WHERE vin = %s;
    """
    check_car_exists = """
        SELECT vin 
        FROM Car 
        WHERE vin = %s;
    """
    conn = None
    try:
        conn = psycopg2.connect(
                    dbname=options['dbname'],
                    user=options['user'],
                    password=options['password'])
        
        cur = conn.cursor()
        cur.execute(check_car_exists, (values['vin'],))
        isAvail = cur.fetchall()
        print(isAvail)
        if len(isAvail) == 1:
            cur.execute(updateStatusQuery, (values['status'],values['vin']))
            conn.commit()
        else:
            return "Car does not exist"
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Error", 500
    return "success", 201

@app.route('/updateAvailability', methods=["GET"])
def renderAvailabiliity():
    return render_template("updateAvailabilityStatus.html")

if __name__ == '__main__':
    app.run()
    # add_customer()
    # connect()