/**
 * Gathers the information of the input values and creates a POST request to the server
 * If the server errors, returns the status text. Otherwise, returns 'Successfully rented'
 * @returns Returns 'successfully rented' if the car was successfully rented.
 * Otherwise, returns the error status text.
 */
async function rentCar() {
  // extract all the input values
  const firstName = document.getElementById('cust-fname').value;
  const lastName = document.getElementById('cust-lname').value;
  const birthdate = document.getElementById('cust-bday').value;
  const carVin = document.getElementById('car-vin').value;
  const rentalLength = document.getElementById('rental-length').value;
  // ensure they all have a value
  if (!firstName || !lastName || !birthdate || !carVin || !rentalLength)
    return "You cannot have null values.";
  const options = {
    customer: {
      'first_name': firstName,
      'last_name': lastName,
      birthdate,
    },
    car: {
      vin: carVin
    },
    rental_length: parseInt(rentalLength)
  };
  const response = await fetch('/create_rental', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(options)
  }).then((res) => {
    if (res.status === 201)
      return "Successfully Rented";
    return res.text();
  });

  alert(response);
  return response;
}

/**
 * Rates a car using the vin number and rental number provided. Returns 'Successfully Rated'
 * on a successful rating. Otherwise, returns the status error.
 * @returns Returns Successfully Rated on a successful rating. Otherwise, returns the error status
 * code.
 */
async function rateRental() {
  const rating = document.getElementById('rating').value;
  const rentalNumber = document.getElementById('rental-number').value;
  const carVIN = document.getElementById('car-vin').value;

  const isRatingValid = rating == undefined || rating < 0 || rating > 5;
  if (isRatingValid || !rentalNumber || !carVIN) {
    alert("You cannot have null values");
    return "You cannot have null values";
  }

  const options = {
    car: {
      vin: carVIN
    },
    rental_record: {
      rental_number: rentalNumber
    },
    rating
  };

  const response = await fetch('/add_rating', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(options)
  }).then((res) => {
    if (res.status === 201)
      return "Successfully Rated";
    return res.text();
  });

  alert(response);
  return response;
}

async function addCar() {
  const vin = document.getElementById('vin').value;
  const cartype = document.getElementById('cartype').value;
  const make = document.getElementById('make').value;
  const model = document.getElementById('model').value;
  const year = document.getElementById('year').value;
  const numaccidents = document.getElementById('numaccidents').value;
  const seats = document.getElementById('seats').value;
  const hourlyrate = document.getElementById('hourlyrate').value;
  const availability = document.getElementById('availability').value;

  const isValidAvilability = availability == 'true' || availability == 'false';
  const isValidYear = year < 2022 || year > 1950;  // arbitrary values

  if (!isValidAvilability) {
    alert("Avialability has to be true or false");
    return "You cannot have nuAvialability";
  }

  if (!isValidYear) {
    alert("Year is either too old or not valid");
    return "Year is either too old or not valid";
  }

  const options = {
    car: {
      vin, cartype, make, model, year, numaccidents, seats, hourlyrate, availability
    }
  };

  const response = await fetch('/add_car', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(options)
  }).then((res) => {
    if (res.status === 201)
      return "Successfully Added Car";
    return res.text();
  });
  alert(response);
}

async function removeCar() {
  const vin = document.getElementById('r-vin').value;

  const options = {
    car: {
      vin
    }
  };

  const response = await fetch('/remove_car', {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(options)
  }).then((res) => {
    if (res.status === 200)
      return "Successfully Removed Car";
    return res.text();
  });
  alert(response);
}  
