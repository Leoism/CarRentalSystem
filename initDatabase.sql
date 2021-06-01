-- create the database
DROP DATABASE IF EXISTS CarRentalDB;
CREATE DATABASE CarRentalDB;

-- switch to the database
\c carrentaldb

-- creating tables
-- sources: https://www.postgresqltutorial.com/postgresql-create-table/
CREATE TABLE States (
  ID    VARCHAR(2)    PRIMARY KEY,
  name  VARCHAR(32)   NOT NULL
);

CREATE TABLE Customer (
  ID        SERIAL        PRIMARY KEY,
  firstName VARCHAR(64)   NOT NULL,
  lastName  VARCHAR(64)   NOT NULL,
  licenseID VARCHAR(32)   NOT NULL UNIQUE,
  birthdate DATE      NOT NULL,
  street    VARCHAR(128)  NOT NULL,
  city      VARCHAR(128)  NOT NULL,
  state     VARCHAR(2)    NOT NULL,

  FOREIGN KEY (state) REFERENCES States(ID)
);

CREATE TABLE CarType (
  type  VARCHAR(2)    PRIMARY KEY,
  name  VARCHAR(32)   NOT NULL
);

CREATE TABLE Car (
  ID            SERIAL        PRIMARY KEY,
  VIN           VARCHAR(17)   UNIQUE NOT NULL,
  carType       VARCHAR(2)    NOT NULL,
  make          VARCHAR(32)   NOT NULL,
  model         VARCHAR(32)   NOT NULL,
  year          INT           NOT NULL,
  numAccidents  INT           NOT NULL,
  seats         INT           NOT NULL,
  hourlyRate    numeric(5,2)  NOT NULL,
  availability  BOOLEAN       NOT NULL,

  FOREIGN KEY(carType) REFERENCES CarType(type)
);

CREATE TABLE RentalRecord (
  carID           INT         NOT NULL,
  customerID      INT         NOT NULL,
  carRented       TIMESTAMP   NOT NULL,
  carReturned     TIMESTAMP,
  expectedReturn  TIMESTAMP   NOT NULL,
  rentalNumber    VARCHAR(16) UNIQUE NOT NULL,
  totalCost       numeric(10,2),

  PRIMARY KEY (rentalNumber),
  FOREIGN KEY (carID) REFERENCES Car(ID),
  FOREIGN KEY (customerID) REFERENCES Customer(ID)
);

CREATE TABLE RatingRecord (
  carID         INT         NOT NULL,
  rentalNumber  VARCHAR(16) NOT NULL,
  rating        INT         NOT NULL,

  PRIMARY KEY (carID, rentalNumber),
  FOREIGN KEY(carID) REFERENCES Car(ID),
  FOREIGN KEY(rentalNumber) REFERENCES RentalRecord(rentalNumber)
);

-- Set up the domain table values
-- init the domain tables
INSERT INTO CarType(Type, Name)
VALUES
  ('SU', 'SUV'),
  ('SE', 'Sedan'),
  ('CO', 'Coupe'),
  ('MV', 'Minivan');
INSERT INTO States(name, ID)
VALUES
  ('Alabama',	'AL'),
  ('Alaska',	'AK'),
  ('Arizona',	'AZ'),
  ('Arkansas',	'AR'),
  ('California',	'CA'),
  ('Colorado',	'CO'),
  ('Connecticut',	'CT'),
  ('Delaware',	'DE'),
  ('Florida',	'FL'),
  ('Georgia',	'GA'),
  ('Hawaii',	'HI'),
  ('Idaho',	'ID'),
  ('Illinois',	'IL'),
  ('Indiana',	'IN'),
  ('Iowa',	'IA'),
  ('Kansas',	'KS'),
  ('Kentucky',	'KY'),
  ('Louisiana',	'LA'),
  ('Maine',	'ME'),
  ('Maryland',	'MD'),
  ('Massachusetts',	'MA'),
  ('Michigan',	'MI'),
  ('Minnesota',	'MN'),
  ('Mississippi',	'MS'),
  ('Missouri',	'MO'),
  ('Montana',	'MT'),
  ('Nebraska',	'NE'),
  ('Nevada',	'NV'),
  ('New Hampshire',	'NH'),
  ('New Jersey', 'NJ'),
  ('New Mexico', 'NM'),
  ('New York', 'NY'),
  ('North Carolina', 'NC'),
  ('North Dakota', 'ND'),
  ('Ohio',	'OH'),
  ('Oklahoma',	'OK'),
  ('Oregon',	'OR'),
  ('Pennsylvania',	'PA'),
  ('Rhode Island',	'RI'),
  ('South Carolina',	'SC'),
  ('South Dakota',	'SD'),
  ('Tennessee',	'TN'),
  ('Texas',	'TX'),
  ('Utah',	'UT'),
  ('Vermont',	'VT'),
  ('Virginia',	'VA'),
  ('Washington',	'WA'),
  ('West Virginia',	'WV'),
  ('Wisconsin',	'WI'),
  ('Wyoming',	'WY');
