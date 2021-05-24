-- add some new cars to inventory
INSERT INTO Car (VIN, CarType, Make, Model, Year, NumAccidents, Seats, availability, hourlyRate)
VALUES
  ('123123', 'SE', 'Toyota', 'Corolla', '2018', '0', '5', 'true', 45),
  ('456456', 'SU', 'Ford', 'Escape', '2021', '0', '6', 'true', 75);

-- add a customer
INSERT INTO Customer (firstName, lastName, birthDate, street, city, state)
VALUES ('Bob', 'TheBuilder', '01-23-1234', 'Somewhere St', 'Elsewhere', 'WA');

-- add a rental record for Bob and the Sedan
INSERT INTO RentalRecord (CarID, CustomerID, carRented, expectedReturn, rentalNumber)
VALUES ((SELECT Car.ID FROM Car WHERE Car.VIN = '123123'),
	(SELECT Customer.ID FROM Customer
	WHERE Customer.firstName = 'Bob'
		AND Customer.lastName = 'TheBuilder'
		AND Customer.birthDate = '01-23-1234'), 
	CURRENT_TIMESTAMP, '2021-06-12 12:00:00', 'UU467HJ8G2D');
-- and set availability to false
UPDATE Car
SET availability = 'false'
WHERE Car.VIN = '123123';



-- Transacting a Rental --
-- update return date
UPDATE RentalRecord
SET carReturned = '2021-06-10 12:00:00'
WHERE CarID = (SELECT Car.ID FROM Car WHERE VIN = '123123');
-- Calculate the price
UPDATE RentalRecord
SET totalCost = (
  SELECT Car.hourlyRate * CEIL(EXTRACT(EPOCH FROM (RentalRecord.expectedReturn - RentalRecord.carRented)) / 3600) + CEIL(EXTRACT(EPOCH FROM (RentalRecord.carReturned - RentalRecord.expectedReturn))  / 3600) * 75 AS totalPrice
  FROM Car
    JOIN RentalRecord ON (RentalRecord.carID = Car.ID)
  WHERE Car.VIN = '123123' AND RentalRecord.totalCost IS NULL
)
WHERE rentalNumber = 'UU467HJ8G2D';
-- make car available
UPDATE Car
SET availability = 'true'
WHERE Car.ID = (SELECT Car.ID FROM Car WHERE VIN = '123123'); 
-- end --
-- update accidents
UPDATE Car
SET numAccidents = numAccidents + 1
WHERE VIN = '123123';

-- add rating record to the sedan
INSERT INTO RatingRecord (CarID, rentalNumber, rating)
VALUES ((SELECT Car.ID FROM Car WHERE Car.VIN = '123123'), 'UU467HJ8G2D' , '5');

-- find a car Toyota Sedan
SELECT Car.VIN, Car.CarType, Car.Make, Car.Model, Car.Year
FROM Car
  -- not all cars will have rating records
	LEFT JOIN RatingRecord ON (RatingRecord.carID = Car.id)
	JOIN CarType ON (CarType.type = Car.CarType)
WHERE CarType.Name = 'SUV' AND Car.Make = 'Ford'
	AND Car.hourlyRate <= '80' AND Car.availability = 'true';