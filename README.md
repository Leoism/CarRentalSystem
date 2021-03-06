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
Before proceeding any further, ensure that you are in the root directory of the app.

### Python Setup
The project has been tested to work on Python 3.7+. Using other versions of Python may yield different results.
This project also requires the Python package manager `pip` to be able to successfully install the packages.

The project requires many packages to be installed through `pip` in order for CarRentalSystem to work.
To ease the installation process, we have provided a `requirements.txt` file. To install the packages run:
```
pip3 install -r requirements.txt
```

### Database Setup
To setup the database, navigate to your PostgreSQL CLI. In other words, open up psql. Once in the postgres command line, run our `initDatabase.sql` file to create the `carrentaldb`.
Run the file by inputting:
```
\i initDatabase.sql
```

### Final Setup
In order for the webserver to properly run, you must create a `.env` file at the root of the app directory. The `.env` file must follow the following format:
```
USERNAME=<username>
PASSWORD=<password>
ADDRESS=<address>
DATABASE=<database>
```
+ `<username>` must be replaced with your PostgreSQL username.
+ `<password>` must be replaced with the password associated with the PostgreSQL username you specified earlier.
+ `<address>` must be replaces with the address your database is located at. When running locally, this will usually be `localhost` or `127.0.0.1` 
+ `<database>` must be replaced with the name of the database. If you have followed along, the database for this project would be `carrentaldb`

Once run, you can now start running your own rental company.

---
## Running the Webserver
After completing all previous steps, you are now ready to start running your own rental company. To do so, ensure that you are in the root directory of the app and run the following in a command line:
```
python3 server.py
```
If you have left Flask in its default setting, you can navigate to either `127.0.0.1:5000` or `localhost:5000`
You have now setup your car rental company.
