# CarRentalSystem

Final project for CSS475
- Leonardo
- Danny
- Kenneth
- Max
- Landon
---
## Project Description 

Final project for CSS 475 Database Systems class. This project is built to simulate a car rental company.

This website acts as a tool for a car rental agent to use. The agents are capable of:
+ Registering Customers into the database
+ Adding Cars to their inventory
+ Removing Cars from the inventory
+ Renting out cars to customer
+ Charging customers once the car is returned
+ Asking the customer for a rating
+ Viewing the Car Inventory
---
## Setting up the Project and Environment

### Python Setup
The project has been tested to work on Python 3.7+. Using other versions of Python may yield different results.
This project also requires the Python package manager `pip` to be able to successfully install the packes.

The project requires the following two packes to be installed through `pip` in order for CarRentalSystem to work:
1. Flask - Hosts a web server where the user can then navigate the website
2. Psycopg2 - Library that helps connect to PostgreSQL

To install Flask, run `pip install Flask`
To install Psycopg2, run `pip install psycopg2` 

### Database Setup
To setup the database, navigate to your PostgreSQL CLI. Once in the command line, run our `initDatabase.sql` file to create the `carrentaldatabase`.
Run the file by inputting:
```
\i initDatabase.sql
```

### Final Setup
In order for the webserver to properly run, you must create a `keys.json` file at the root of the app directory. The `keys.json` file must follow the following format:
```
{
  "dbname": "<database>",
  "user": "<username>",
  "password": "<password>"
}
```
+ `<database>` must be replaced with the name of the database. If you have followed along, the database for this project would be `carrentaldb`
+ `<username>` must be replaced with your PostgreSQL username.
+ `<password>` must be replaced with the password associated with the PostgreSQL username you specified earlier.

Once run, you can now start running your own rental company.
---
## Running the Webserver
After completing all previous steps, you are now ready to start running your own rental company. To do so, run the following in a command line:
```
python3 server.py
```
If you have left Flask in its default setting, you can navigate to either `127.0.0.1:5000` or `localhost:5000`
You have now setup your car rental company.
