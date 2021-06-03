#!/usr/bin/python
import os
import psycopg2
import json # add as req
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from datetime import datetime, timedelta # add as req
import time # add as req
import random # add as req
# from dotenv import load_dotenv killed this line

# from config import config

app = Flask(__name__)
DATABASE_DEFAULT = 'postgres://bicmtliamldnxg:55b4e5a6811f775cadc10e35b162034ff07e4feffd8f6adda348b23ab147431f@ec2-18-215-111-67.compute-1.amazonaws.com:5432/d1v5bd4t1v3do'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', DATABASE_DEFAULT)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# conn = psycopg2.connect(DATABASE_DEFAULT)

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
        conn = psycopg2.connect(DATABASE_DEFAULT)

        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        # print('PostgreSQL database version:')
        # cur.execute('SELECT version()')
        cur.execute("""SELECT Car.VIN, CarType.Name, Car.Make, Car.Model, Car.Year, Car.NumAccidents, 
        Car.Seats, Car.HourlyRate, Car.Availability, Table1.Rating 
        FROM Car
            JOIN CarType ON (CarType.type = Car.CarType)
            LEFT JOIN (
                SELECT RatingRecord.carID, SUM(RatingRecord.rating) / COUNT(RatingRecord.rating) AS Rating
                FROM RatingRecord
                GROUP BY RatingRecord.carId) AS Table1 ON (Car.ID = Table1.CarID)
        WHERE Car.isDeleted = false;""") # FORMAT: (1) generate connection cursor, (2) execute query, (3) fetchall, (4) print

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
        rows = cur.fetchall() # take all rows from output
        print(rows)
        # Get the column names of the table
        cur.execute("""SELECT Car.VIN, CarType.Name, Car.Make, Car.Model, Car.Year, Car.NumAccidents, 
        Car.Seats, Car.HourlyRate, Car.Availability, Table1.Rating 
        FROM Car
            JOIN CarType ON (CarType.type = Car.CarType)
            LEFT JOIN (SELECT RatingRecord.carID, SUM(RatingRecord.rating) / COUNT(RatingRecord.rating) AS Rating
                FROM RatingRecord
                GROUP BY RatingRecord.carId) AS Table1 ON (Car.ID = Table1.CarID)
                 LIMIT 0;""")
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
                VALUES ((SELECT RentalRecord.carID FROM RentalRecord WHERE rentalNumber ILIKE %s), %s , %s);"""
    values = request.json
    # extract customer
    rental_record = values['rental_record']
    # and car objects from the json
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_DEFAULT)
        cur = conn.cursor()
        cur.execute(query, (rental_record['rental_number'], rental_record['rental_number'], values['rating'],))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        conn.close()
        if not hasattr(error, 'pgcode'):
            return MISC_ERROR_MSG
        if error.pgcode == '23502':
            return "The Rental Number does not seem to exist. Try Again."
        if error.pgcode == '23505':
            return "There is already a rating for this rental. You cannot rate more than once."
        if error.pgcode == '22P02':
            return "It seems some of your values are not valid. Please try again."
        print(error.pgcode)
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
    if values['rental_length'] <= 0:
        return "You cannot rent a car for less than one day", 500
    # First we must check that the car is available
    check_avail_query = """
        SELECT availability
        FROM Car
        WHERE Car.availability = 'true' AND Car.VIN ILIKE %s AND Car.isDeleted = false;
    """
    try:
        conn = psycopg2.connect(DATABASE_DEFAULT)
        cur = conn.cursor()
        cur.execute(check_avail_query, (car['vin'],))
        avail_car = cur.fetchall()
        # Ensure that the car is available
        if len(avail_car) != 1 or avail_car[0][0] is not True:
            conn.close()
            return "Car is not available", 500
    except (Exception, psycopg2.DatabaseError) as error:
        conn.close()
        if not hasattr(error, 'pgcode'):
            return MISC_ERROR_MSG
        print (error)
        return "Error", 500

    # Check if the customer has any current rentals
    customer_eligibility = """
        SELECT *
        FROM RentalRecord
        WHERE carReturned IS NULL AND customerID = (
            SELECT ID
            FROM Customer
            WHERE Customer.licenseID ILIKE %(license_id)s AND
            Customer.firstName ILIKE %(first_name)s AND 
            Customer.lastName ILIKE %(last_name)s AND 
            Customer.birthdate = %(birthdate)s
        );
    """
    try:
        cur.execute(customer_eligibility, {
            'license_id': customer['license_id'],
            'first_name': customer['first_name'],
            'last_name': customer['last_name'],
            'birthdate': customer['birthdate']
        })
        outgoing_rental = cur.fetchall()
        if len(outgoing_rental) > 0:
            conn.close()
            return "The customer already has an outgoing rental. Please request the car's return before renting them another one.", 500
    except(Exception, psycopg2.DatabaseError) as error:
        conn.close()
        if not hasattr(error, 'pgcode'):
            return MISC_ERROR_MSG, 500
        if error.pgcode == "23502":
            return "The customer has not yet been registered into the database.", 500
        print(error)
        return "Error", 500
    # Second, we must create a rental record and a rental number
    rent_query = """
        INSERT INTO RentalRecord (CarID, CustomerID, carRented, expectedReturn, rentalNumber)
        VALUES ((SELECT Car.ID FROM Car WHERE Car.VIN = %(car_vin)s AND Car.isDeleted = false),
        (SELECT Customer.ID FROM Customer
        WHERE Customer.licenseID ILIKE %(license_id)s AND
            Customer.firstName ILIKE %(first_name)s AND 
            Customer.lastName ILIKE %(last_name)s AND
            Customer.birthdate = %(birthdate)s), 
        %(todays_date)s, %(expected_ret)s, %(rental_num)s);
        """
    rental_num = _generate_number(16)
    try:
        cur.execute(rent_query, {
            'car_vin': car['vin'],
            'todays_date': str(today),
            'license_id': customer['license_id'],
            'first_name': customer['first_name'],
            'last_name': customer['last_name'],   
            'birthdate': customer['birthdate'],    # rental_length must be in days
            'expected_ret': str(today + timedelta(days=values['rental_length'])),
            'rental_num': rental_num
        })
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        conn.close()
        if not hasattr(error, 'pgcode'):
            return MISC_ERROR_MSG, 500
        if error.pgcode == "23502":
            return "The customer has not yet been registered into the database.", 500
        print(error)
        return "Error", 500

    # Finally, we must update the availability of the car
    update_avail = """
        UPDATE Car
        SET availability = 'false'
        WHERE Car.VIN ILIKE %s And Car.isDeleted = false;
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
    return render_template('rentalSuccess.html',
                            rental_num=rental_num,
                            customer_name=customer['first_name'] + " " + customer['last_name']
                        ), 201

@app.route('/get_rental_cost', methods=['PUT'])
def get_rental_cost():
    printHelper = ""
    values = request.json
    rental_record = values['rental_record']
    returnQuery = """
        UPDATE RentalRecord
        SET carReturned = CURRENT_TIMESTAMP
        WHERE rentalNumber ILIKE %s AND carReturned IS NULL;
    """
    availabilityQuery = """
        UPDATE Car
        SET availability = 't'
        WHERE Car.id = (SELECT RentalRecord.carid FROM RentalRecord WHERE rentalNumber ILIKE %s AND carreturned IS NULL);
    """
    updateStatusQuery = """
        UPDATE RentalRecord
        SET totalCost = (SELECT (T1.initCost + T2.overtime)::numeric(8, 2) AS finalCost
        FROM (SELECT CASE
        WHEN Temp.overtime < 0 THEN COALESCE(Temp.overtime - Temp.overtime, 0)
        WHEN Temp.overtime >= 0 THEN Temp.overtime
        END AS overtime
        FROM (SELECT EXTRACT(EPOCH FROM (RentalRecord.carReturned - RentalRecord.expectedReturn)/3600 * 75)::float AS overtime
        FROM RentalRecord
        WHERE RentalRecord.RentalNumber ILIKE %s) AS Temp
        GROUP BY Temp.overtime) AS T2
        JOIN (SELECT Tempy.initCost
        FROM (SELECT EXTRACT(EPOCH FROM (RentalRecord.carRented - RentalRecord.carReturned)/3600 * Car.hourlyRate * -1)::float AS initCost
        FROM RentalRecord
        JOIN Car on (RentalRecord.carID = Car.ID)
        WHERE RentalRecord.RentalNumber ILIKE %s) AS Tempy
        GROUP BY Tempy.initCost) AS T1 ON TRUE)
        WHERE RentalRecord.RentalNumber ILIKE %s
        RETURNING totalCost;
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_DEFAULT)
        
        cur = conn.cursor()
        #cur.execute(check_car_exists, (values['vin'],))
        #isAvail = cur.fetchall()
        #print(isAvail)
        cur.execute(availabilityQuery, (rental_record['rental_number'],))
        cur.execute(returnQuery, (rental_record['rental_number'],))
        cur.execute(updateStatusQuery, (rental_record['rental_number'],rental_record['rental_number'],rental_record['rental_number'],))
        checkExec = cur.fetchall()
        if len(checkExec) != 0:
            conn.commit()
        else:
            return "user inputted rental number doesn't exist in the db", 500
        printHelper = "Success, total cost is: " + str(checkExec[0][0])
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Error", 500
    return str(printHelper), 201

@app.route('/get_rental_info')
def query_rental():
    car = None
    rows = ''
    column_names = None
    values = request.args.get('search', default = '')
    #print(values) # aaaaaaa
    #rental_record = values['rental_number']
    rental_record = json.loads(values)['rental_record']
    #print(rental_record) # aaaaaa
    rentalInfoQuery = """
            SELECT Customer.firstname, Customer.lastname, RentalRecord.carRented, RentalRecord.carReturned,
	        RentalRecord.expectedReturn, RentalRecord.rentalNumber, RentalRecord.totalCost, Car.carType, 
	        Car.Make, Car.Model, Car.Year, Car.hourlyRate
            FROM RentalRecord
	        JOIN Customer ON (Customer.id = RentalRecord.Customerid)
	        JOIN Car ON (Car.id = RentalRecord.Carid)
            WHERE RentalRecord.RentalNumber ILIKE %s;
            """      
    try:
        conn = psycopg2.connect(DATABASE_DEFAULT)
        cur = conn.cursor()
        cur.execute(rentalInfoQuery, (rental_record['rental_number'],)) # (rental_record['rental_number'],))
        #conn.commit()
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Error", 500
    if conn is not None:
        conn.close()
    return render_template("rent.html", rows=rows, column_names=column_names)

@app.route('/add_car', methods=['POST'])
def add_car():

    query = """ INSERT INTO Car (VIN, carType, make, model, year, numaccidents, seats, hourlyrate, availability) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'true');"""
    is_deleted_query = """
        SELECT ID 
        FROM CAR
        WHERE vin = %s AND isDeleted = true;
    """
    re_add_car = """
        UPDATE Car
        SET isDeleted = false
        WHERE vin = %s
    """
    values = request.json

    car = values['car']

    vin = car['vin']
    carType = car['cartype']
    make = car['make']
    model = car['model']
    year = car['year']
    numaccidents = car['numaccidents']
    seats = car['seats']
    hourlyrate = car['hourlyrate']

    conn = None

    try: 
        conn = psycopg2.connect(DATABASE_DEFAULT)
        cur = conn.cursor()
        cur.execute(is_deleted_query, (vin,))
        deleted_entries = cur.fetchall()
        if (len(deleted_entries) > 0):
            cur.execute(re_add_car, (vin,))
            conn.commit()
            cur.close()
            return "Successfully added a car.", 201

        cur.execute(query, (vin, carType, make, model, year, numaccidents, seats, hourlyrate))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Car could not be added because that VIN number is already used", 500
    if conn is not None:
        conn.close()
    return "Successfuly Added a Car", 201

@app.route('/remove_car', methods=['DELETE'])
def remove_car():
    query = """DELETE FROM Car
               WHERE vin ILIKE %s"""
    is_deleted_query = """
        SELECT ID
        FROM CAR 
        WHERE vin ILIKE %s AND Car.isDeleted = true;
    """

    values = request.json
    
    car = values['car']
    vin = car['vin']

    conn = None

    try: 
        conn = psycopg2.connect(DATABASE_DEFAULT)
        cur = conn.cursor()
        cur.execute(is_deleted_query, (vin,))
        deleted_entries = cur.fetchall();
        if (len(deleted_entries) > 0):
            return "That car does not exist", 500
        cur.execute(query, (vin,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "That car is not in the database", 500
    if conn is not None:
        conn.close()
    return "Successfuly Removed a Car", 200

@app.route('/car', methods=['GET'])
def return_car():
    return render_template('car.html')



@app.route('/update_accidents', methods=['PUT'])
def update_accidents():
    """
        Update amount of accidents on a car. Increments numAccidents by one, as it is impossible to ethically undo an accident.
    """
    values = request.json
     # Update the accidents of the car
    update_acid = """
        UPDATE Car
        SET numAccidents = numAccidents + 1
        WHERE VIN ILIKE %(car_vin)s AND isDeleted = false;
        """
    try: 
        conn = psycopg2.connect(DATABASE_DEFAULT)
        cur = conn.cursor()
        cur.execute(update_acid, {
            'car_vin': values['vin']
        })
        retval = cur.rowcount #apparently compares the values to make sure there is a match in the database
        if retval == 0:
            return "That Car Does Not Exist", 500
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "A car with that VIN was not found", 500
    if conn is not None:
        conn.close()
    return "Successfully Added an Incident to a Car", 200


@app.route('/queryCars')
def query_cars():
    car = None
    rows = ''
    column_names = None
    values = request.args.get('search', default = '')
    filter = json.loads(values)['filter']
    #no * to avoid showing ID
    show_car_query = """
        SELECT Car.VIN, CarType.Name, Car.Make, Car.Model, Car.Year, Car.NumAccidents, 
        Car.Seats, Car.HourlyRate, Car.Availability, Table1.Rating 
        FROM Car
            JOIN CarType ON (CarType.type = Car.CarType)
            LEFT JOIN (SELECT RatingRecord.carID, SUM(RatingRecord.rating) / COUNT(RatingRecord.rating) AS Rating
                FROM RatingRecord
                GROUP BY RatingRecord.carId) AS Table1 ON (Car.ID = Table1.CarID)
            WHERE 
            """
    #force a number for first where
    if filter['acc'] != '': 
        show_car_query += 'Car.NumAccidents <= %(car_acc)s'
    else:
        show_car_query += 'Car.NumAccidents >= 0 '
    if filter['vin'] != '': 
        show_car_query += 'AND Car.VIN ILIKE  %(car_vin)s '
    if filter['name'] != '': 
        show_car_query += 'AND CarType.Name ILIKE %(car_name)s '
    if filter['make'] != '': 
        show_car_query += 'AND Car.Make ILIKE %(car_make)s '
    if filter['model'] != '': 
        show_car_query += 'AND Car.Model ILIKE %(car_model)s '
    if filter['year'] != '': 
        show_car_query += 'AND Car.Year = %(car_year)s '
    if filter['seats'] != '': 
        show_car_query += 'AND Car.Seats = %(car_seats)s '    
    if filter['price'] != '': 
        show_car_query += 'AND Car.HourlyRate <= %(car_price)s '  
    if filter['avail'] != '': 
        show_car_query += 'AND Car.Availability = %(car_avail)s '       
    if filter['rate'] != '': 
        show_car_query += 'AND Table1.Rating >= %(car_rate)s '       
             
    #show_car_query += 'GROUP BY ratingrecord.carid,Car.ID, Car.VIN, Car.CarType, Car.Make, Car.Model, Car.Year;' 
    show_car_query += 'AND Car.isDeleted = false;'
    try:
        conn = psycopg2.connect(DATABASE_DEFAULT)
        cur = conn.cursor()
        cur.execute(show_car_query, { #implementation type1
            'car_vin': filter['vin'],
            'car_name': filter['name'], 
            'car_make': filter['make'],
            'car_model': filter['model'],
            'car_year': filter['year'],
            'car_acc': filter['acc'],
            'car_seats': filter['seats'],
            'car_price': filter['price'],
            'car_avail': filter['avail'],
            'car_rate': filter['rate']
        })
        #conn.commit()
        rows = cur.fetchall()
        cur.execute(""" SELECT Car.VIN, CarType.Name, Car.Make, Car.Model, Car.Year, Car.NumAccidents, 
        Car.Seats, Car.HourlyRate, Car.Availability, Table1.Rating 
        FROM Car
            JOIN CarType ON (CarType.type = Car.CarType)
            LEFT JOIN (SELECT RatingRecord.carID, SUM(RatingRecord.rating) / COUNT(RatingRecord.rating) AS Rating
                FROM RatingRecord
                GROUP BY RatingRecord.carId) AS Table1 ON (Car.ID = Table1.CarID)
             LIMIT 0;""")
        column_names = [desc[0] for desc in cur.description]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "An error was found on Python's end", 500
    if conn is not None:
        conn.close()
    return render_template("index.html", rows=rows, column_names=column_names)
    
    
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
        conn = psycopg2.connect(DATABASE_DEFAULT)
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
        INSERT INTO Customer (firstname, lastname, licenseID, birthdate, street, city, state)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    conn = None
    try:
        conn = psycopg2.connect(DATABASE_DEFAULT)
        cur = conn.cursor()
        cur.execute(addCustomerQuery, (values['first_name'], values['last_name'], values['license_id'], values['birthdate'], values['street'], values['city'], values['state'],))
        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Error: a customer with that information may already be added.", 500
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
        WHERE vin ILIKE %s AND Car.isDeleted = false;
    """
    check_car_exists = """
        SELECT vin 
        FROM Car 
        WHERE vin ILIKE %s AND Car.isDeleted = false;
    """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_DEFAULT)
        
        cur = conn.cursor()
        cur.execute(check_car_exists, (values['vin'],))
        isAvail = cur.fetchall()
        print(isAvail)
        if len(isAvail) == 1:
            cur.execute(updateStatusQuery, (values['status'],values['vin']))
            conn.commit()
        else:
            return "Car does not exist"
            conn.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.close()
        return "Error", 500
    return "success", 201

@app.route('/updateAvailability', methods=["GET"])
def renderAvailabiliity():
    return render_template("updateAvailabilityStatus.html")

@app.route('/agent', methods=["GET"])
def agent_template():
    return render_template("AgentPage.html")

@app.route('/login', methods=["GET"])
def login_template():
    return render_template("LoginPage.html")

if __name__ == '__main__':
    app.run()
    # add_customer()
    # connect()
