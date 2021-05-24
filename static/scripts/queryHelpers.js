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