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
    }).then(async (res) => {
        if (res.status === 201) {
            document.querySelector('html').innerHTML = await res.text();
            return "Success";
        }
        return res.text();
    });

    alert(response);
    return response;
}

/** For the FIRST time this button is clicked, a customer is "returning" a car that was rented. 
 * This triggers the query to set NOW as the timestamp in which the car is returned.
 * It also returns the total cost of the rental to the user. 
 * For SUBSEQUENT calls, it only returns the total cost of the rental to the user. 
 **/
async function getRentalCost() {
    // extract all the input values
    const rentalNum = document.getElementById('rental-num1').value;
    // ensure they all have a value
    if (!rentalNum)
        return "You cannot have null values.";
    const options = {
        rental_record: {
            'rental_number': rentalNum,
        },
    };
    const response = await fetch('/get_rental_cost', {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(options)
    }).then((res) => {
        //if (res.status === 201)
        //    return res.text();
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

async function queryRental() {
    // extract all the input values
    const rentalNum = document.getElementById('rental-num').value;
    // ensure they all have a value
    if (!rentalNum)
        return "You cannot have null values.";
    const options = {
        rental_record: {
            'rental_number': rentalNum,
        },
    };
    const response = await fetch('/get_rental_info?search=' + encodeURIComponent(JSON.stringify(options)), {
    }).then((res) => {
        return res.text()
    });
    document.querySelector('html').innerHTML = response;
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
    const availability = document.getElementById('availability').checked;

    const options = {
        car: {
            vin, cartype, make, model, year, numaccidents, seats, hourlyrate, availability
        }
    };

    // checks for valid data
    if (vin.lenth > 17) {
        alert("VIN number is too long");
        return "VIN number is too long";
    } else if (vin.length < 11) {
        alert("VIN number is too short");
        return "VIN number is too short";
    }

    if (numaccidents < 0) { // num accidents > 0
        alert("Number of accidents can't be less than 0");
        return "Number of accidents can't be less than 0";
    }

    if (seats < 1) { // number of seats > 1
        alert("Car can't have less than 1 seat");
        return "Car can't have less than 1 seat";
    }

    if (hourlyrate < 0) { // hourly rate > 1
        alert("Car can't be less than $0/hr");
        return "Car can't be less than $0/hr";
    }

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
        body: JSON.stringify(customerInfo)
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
    let stat = 'True'
    if (availabilityStatus == 'unavailable') {
        stat = 'False'
    }
    const options = {
        vin: carvin,
        status: stat
    };

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

async function queryCars() {
    let vin = document.getElementById('car_vin').value;
    let name = document.getElementById('car_name').value;
    let make = document.getElementById('car_make').value;
    let model = document.getElementById('car_model').value;
    let year = document.getElementById('car_year').value;
    let acc = document.getElementById('car_acc').value;
    let seats = document.getElementById('car_seats').value;
    let price = document.getElementById('car_price').value;
    let avail = document.getElementById('car_avail').value;
    let rate = document.getElementById('car_rate').value;

    if (!vin) vin = ''
    if (!name) name = ''
    if (!make) make = ''
    if (!model) model = ''
    if (!year) year = ''
    if (!acc) acc = ''
    if (!seats) seats = ''
    if (!price) price = ''
    if (!avail) avail = ''
    if (!rate) rate = ''
    const options = {
        filter: {
            vin, name, make, model, year, acc, seats, price, avail, rate
        }
    };

    const response = await fetch('/queryCars?search=' + encodeURIComponent(JSON.stringify(options)), {
    }).then((res) => {
        return res.text()
    });
    document.querySelector('html').innerHTML = response;
}
