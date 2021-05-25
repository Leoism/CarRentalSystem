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
  console.log("didn't work")
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

  const response = await fetch('/add_rating', { // add rating is the endpoint
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(options) // all of the stuff we want sent over to the endpoint which is addrating in this case
  }).then((res) => {
    if (res.status === 201)
      return "Successfully Rated";
    return res.text();
  });

  alert(response);
  return response;
}

async function addCustomer() {
  const fname = document.getElementById('cust-fname').value
  const lname = document.getElementById('cust-lname').value
  const bday = document.getElementById('cust-bday').value
  const streetField = document.getElementById('cust-street').value
  const cityField = document.getElementById('cust-city').value
  const stateField = document.getElementById('cust-state').value

  if (!fname || !lname || !bday || !streetField || !cityField || !stateField) {
    console.log("you cannot have null values")
  }

  const customerInfo = {
    fName: fname,
    lName: lname,
    bDay: bday,
    street: streetField,
    city: cityField,
    state: stateField
  };

  const response = await fetch('/add_customer', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(customerInfo2)
  }).then((res) => {
    if (res.status == 201)
      return "successfully Added Customer"
      return res.text()
  });

  alert(response);
  return response;

}

async function updateAvailability(availabilityStatus) {
  const carvin = document.getElementById('car-vin').value
  stat = 'True'
  if (availabilityStatus == 'unavailable') {
    stat = 'False'
  }
  const options = {
    vin: carvin,
    status: stat}

  const response = await fetch('/update_availability_status', { 
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(options)
  }).then((res) => {
    if (res.status == 201) 
    return "Successfully Updated Availability Status"
    return res.text()
  });

  alert(response);
  return response;

}