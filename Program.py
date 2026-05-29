import sys
import psycopg
from datetime import datetime


CONN = psycopg.connect(
        dbname="carrent",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432",
)

def getCursor():
    return CONN.cursor()


#prompts
def prompt_exit(message):
    #If types 'exit' the whole program exit 
    val = input(message).strip()
    if val.lower() == "exit":
        print("Exiting program...")
        cleanup_and_exit()
    return val


def prompt_int(message, allow_empty=False, min_value=None):
    while True:
    # Repeats until valid value 
        text = prompt_exit(message)
        #If allow_empty is True means that user can press Enter to return None
        if allow_empty and text == "":
            return None
        try:
            value = int(text)
        except ValueError:
            print("Invalid input. Please enter a valid integer or type 'exit'.")
            continue

        if (min_value is not None) and (value < min_value):
            print("Value must be greater than or equal to", min_value)
            continue
        return value


def prompt_date(message):
    while True:
        text = prompt_exit(message + " (YYYY-MM-DD): ")
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD or type 'exit'.")


def prompt_time(message):
    while True:
        text = prompt_exit(message + " (HH:MM, 24hour): ")
        try:
            datetime.strptime(text, "%H:%M")
            # Add :00 for seconds
            return text + ":00"
        except ValueError:
            print("Invalid time format. Please use HH:MM (for example 09:30) or type 'exit'.")



def run_query(query, params=None, fetch_one=False, fetch_all=False):
    #Run a SELECT query 
    cur = getCursor()
    try:
        cur.execute(query, params or ())
        # Fetch one or all rows
        if fetch_one:
            row = cur.fetchone()
        elif fetch_all:
            row = cur.fetchall()
        else:
            row = None
        return row
    except psycopg.Error as e:
        print("Database query error:", e)
        return None
    finally:
        cur.close()


def run_command(query, params=None):
    #Run INSERT-UPDATEDELETE command and commit
    cur = getCursor()
    try:
        cur.execute(query, params or ())
        CONN.commit()
        return True
    except psycopg.Error as e:
        CONN.rollback()
        print("Database command error:", e)
        return False
    finally:
        cur.close()


def list_available_cars():
    #Show all available cars with details
    print("\n--- Available Cars ---")
    rows = run_query(
        """
        SELECT carid, brand, model, platenumber, year, color, cartype,
               size, transmission, fueltype, seats, bags, dailyprice, status
        FROM cars
        WHERE status = 'Available'
        ORDER BY carid
        """,
        fetch_all=True,
    )
    if not rows:
        print("No available cars.")
        return

    for r in rows:
        print(
            "ID: {0} = {1} {2}  - Plate: {3}, Color: {4}, Type: {5}, "
            "Seats: {6}, Bags: {7}, Transmission: {8}, Fuel: {9}, Daily Price: {10}".format(
                r[0],  # carID
                r[1],  # brand
                r[2],  # model
                r[3],  # plateNumber
                r[5],  # color
                r[6],  # carType
                r[10],  # seats
                r[11],  # bags
                r[8],  # transmission
                r[9],  # fuelType
                r[12],  # dailyPrice
            )
        )


def register_customer():
    #Register new customer in customers table
    print("\n--- Register New Customer ---")
    print("Type 'exit' at any prompt to exit the whole program.")

    full_name = prompt_exit("Full name: ")
    email = prompt_exit("Email (must be unique): ")
    password = prompt_exit("Password (plain text): ")
    phone = prompt_exit("Phone number (can be empty): ")
    if phone == "":
        phone = None
    address = prompt_exit("Address (can be empty): ")
    if address == "":
        address = None

    comm = run_command(
        """
        INSERT INTO customers (fullname, email, password, phone, address)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (full_name, email, password, phone, address),
    )

    if comm:
        print("Customer registered successfully.")
    else:
        print("Customer registration failed. Please try again.")


def list_customers():
    #Show list of all customers
    print("\n--- Customers ---")
    rows = run_query(
        "SELECT userid, fullname, email, phone FROM customers ORDER BY userid",
        fetch_all=True,
    )
    if not rows:
        print("No customers found.")
        return

    for r in rows:
        print("ID: {0} | {1} | Email: {2} | Phone: {3}".format(r[0], r[1], r[2], r[3]))


def add_driver_details():
    # Add driver details for existing customer like license, expiry, ...
    print("\n--- Add Driver Details ---")
    print("Type 'exit' at any prompt to exit the whole program.")
    list_customers()

    user_id = prompt_int("Enter existing customer ID (userID): ", min_value=1)

    # Check that customer exists or not
    customer = run_query(
        "SELECT userid, fullname FROM customers WHERE userid = %s",
        (user_id,),
        fetch_one=True,
    )
    if not customer:
        print("Customer with this ID does not exist.")
        return

    print("Adding driver details for:", customer[1])

    license_number = prompt_exit("License number (must be unique): ")
    license_expiry = prompt_date("License expiry date:")
    national_id = prompt_exit("National ID (can be empty): ")
    if national_id == "":
        national_id = None
    passport_number = prompt_exit("Passport number (can be empty): ")
    if passport_number == "":
        passport_number = None
    date_of_birth = prompt_date("Date of birth")

    comm = run_command(
        """
        INSERT INTO driverdetails
            (userid, licensenumber, licenseexpiry, nationalid, passportnumber, dateofbirth)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user_id, license_number, license_expiry, national_id, passport_number, date_of_birth),
    )
    if comm:
        print("Driver details added successfully.")
    else:
        print("Failed to add driver details. Please check the error above and try again.")


def list_locations():
    # Show all rental locations
    print("\n--- Locations ---")
    rows = run_query(
        "SELECT locationid, locationname, city, address FROM locations ORDER BY locationid",
        fetch_all=True,
    )
    if not rows:
        print("No locations found.")
        return

    for r in rows:
        print("ID: {0} | {1} | {2} | {3}".format(r[0], r[1], r[2], r[3]))


def create_rental():
    # Create a new rental booking.
    # Steps: Select customer - Select car - Select pick-up and drop-off locations -
    # Enter pick-up and drop-off dates and times - Calculate total price based on daily price -
    # Insert into rentals table
    print("\n--- Create New Rental ---")
    print("Type 'exit' at any prompt to exit the whole program.")

    # Choose customer
    list_customers()
    user_id = prompt_int("Enter customer ID (userID): ", min_value=1)
    customer = run_query(
        "SELECT userid, fullname FROM customers WHERE userid = %s",
        (user_id,),
        fetch_one=True,
    )
    if not customer:
        print("Customer not found.")
        return

    # Choose car
    list_available_cars()
    car_id = prompt_int("Enter car ID to rent (carID): ", min_value=1)
    car = run_query(
        "SELECT carid, dailyprice, status FROM cars WHERE carid = %s",
        (car_id,),
        fetch_one=True,
    )
    if not car:
        print("Car not found.")
        return
    if car[2] != "Available":
        print("This car is not available for rental.")
        return

    daily_price = car[1]

    # Choose locations
    list_locations()
    pick_location_id = prompt_int("Enter pickup location ID: ", min_value=1)
    drop_location_id = prompt_int("Enter drop-off location ID: ", min_value=1)

    pickup_date = prompt_date("Pickup date")
    pickup_time = prompt_time("Pickup time")
    dropoff_date = prompt_date("Drop-off date")
    dropoff_time = prompt_time("Drop-off time")


    # Calculate days
    try:
        d1 = datetime.strptime(pickup_date, "%Y-%m-%d")
        d2 = datetime.strptime(dropoff_date, "%Y-%m-%d")
        days = (d2 - d1).days
        if days <= 0:
            print("Drop-off date must be after pickup date.")
            return
    except ValueError:
        print("Internal error in date calculation. Please try again.")
        return

    total_amount = days * daily_price

    print("Calculated rental days:", days)
    print("Daily price:", daily_price)
    print("Total amount:", total_amount)

    ok = run_command(
        """
        INSERT INTO rentals
            (userid, carid, pickuplocationid, dropofflocationid,
             pickupdate, pickuptime, dropoffdate, dropofftime,
             totalamount, bookingstatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
        """,
        (
            user_id,
            car_id,
            pick_location_id,
            drop_location_id,
            pickup_date,
            pickup_time,
            dropoff_date,
            dropoff_time,
            total_amount,
        ),
    )

    if ok:
        print("Rental created successfully with status 'Pending'.")
        # Optionally mark car as not available
        run_command(
            "UPDATE cars SET status = 'Rented' WHERE carid = %s",
            (car_id,),
        )
    else:
        print("Failed to create rental.")


def list_rentals_for_customer():
    # Show all rentals for customer
    print("\n--- Rentals For Customer ---")
    list_customers()
    user_id = prompt_int("Enter customer ID (userID): ", min_value=1)

    rows = run_query(
        """
        SELECT rentals.bookingid,
               rentals.userid,
               customers.fullname,
               rentals.carid,
               cars.brand,
               cars.model,
               rentals.pickupdate,
               rentals.dropoffdate,
               rentals.totalamount,
               rentals.bookingstatus
        FROM rentals JOIN customers ON rentals.userid = customers.userid
        JOIN cars ON rentals.carid = cars.carid
        WHERE rentals.userid = %s
        ORDER BY rentals.bookingid
        """,
        (user_id,),
        fetch_all=True,
    )

    if not rows:
        print("No rentals found for this customer.")
        return

    for r in rows:
        print(
            "BookingID: {0} | Customer: {1} | Car: {2} ,{3} (ID: {4}) | "
            "From {5} to {6} | Amount: {7} | Status: {8}".format(
                r[0],  # bookingID
                r[2],  # fullName
                r[4],  # brand
                r[5],  # model
                r[3],  # carID
                r[6],  # pickupDate
                r[7],  # dropoffDate
                r[8],  # totalAmount
                r[9],  # bookingStatus
            )
        )


def list_rentals():
    # List all rentals
    print("\n--- All Rentals ---")
    rows = run_query(
        """
        SELECT bookingid, userid, carid, pickupdate, dropoffdate,
               totalamount, bookingstatus
        FROM rentals
        ORDER BY bookingid
        """,
        fetch_all=True,
    )
    if not rows:
        print("No rentals found.")
        return

    for r in rows:
        print(
            "BookingID: {0} | UserID: {1} | CarID: {2} | {3} to {4} | "
            "Amount: {5} | Status: {6}".format(
                r[0], r[1], r[2], r[3], r[4], r[5], r[6]
            )
        )


def record_payment():
    # Record a payment for an existing booking
    print("\n--- Record Payment ---")
    print("Type 'exit' at any prompt to exit the whole program.")

    list_rentals()
    booking_id = prompt_int("Enter booking ID to pay for: ", min_value=1)

    rental = run_query(
        "SELECT bookingid, totalamount, bookingstatus FROM rentals WHERE bookingid = %s",
        (booking_id,),
        fetch_one=True,
    )
    if not rental:
        print("Booking not found.")
        return

    print("Booking status:", rental[2])
    print("Total amount:", rental[1])

    amount = prompt_int("Enter amount to pay (integer): ", min_value=1)
    method = prompt_exit("Payment method (for example Cash, Card): ")

    ok = run_command(
        """
        INSERT INTO payments (bookingid, paymentmethod, amountpaid)
        VALUES (%s, %s, %s)
        """,
        (booking_id, method, amount),
    )

    if ok:
        print("Payment recorded successfully.")
        # Mark booking status as Confirmed if paid in full
        total_paid = run_query(
            "SELECT COALESCE(SUM(amountpaid), 0) FROM payments WHERE bookingid = %s",
            (booking_id,),
            fetch_one=True,
        )[0]
        if total_paid >= rental[1]:
            run_command(
                "UPDATE rentals SET bookingstatus = 'Confirmed' WHERE bookingid = %s",
                (booking_id,),
            )
            print("Booking is now marked as 'Confirmed'.")
    else:
        print("Failed to record payment.")


def report_damage():
    # Report damage for a car
    print("\n--- Report Car Damage ---")
    print("Type 'exit' at any prompt to exit the whole program.")

    # Show all cars to help user choose
    print("Existing cars:")
    rows = run_query(
        "SELECT carid, brand, model, platenumber FROM cars ORDER BY carid",
        fetch_all=True,
    )
    if not rows:
        print("No cars in the system.")
        return

    for r in rows:
        print("CarID: {0} | {1} {2} | Plate: {3}".format(r[0], r[1], r[2], r[3]))

    car_id = prompt_int("Enter car ID to report damage for: ", min_value=1)
    description = prompt_exit("Description of damage: ")
    repair_cost = prompt_int("Estimated repair cost (integer): ", min_value=0)


    ok = run_command(
        """
        INSERT INTO damage (carid, description, repaircost)
        VALUES (%s, %s, %s)
        """,
        (car_id, description, repair_cost),
    )

    if ok:
        print("Damage report saved successfully.")
    else:
        print("Failed to save damage report.")


def main_loop():
    # Main loop that show menu, read user choice, call appropriate function
    while True:
        print("\n----------------------------------------------------")
        print("\t\t Car Rental System ")
        print("----------------------------------------------------")
        print("Type 'exit' at any time to close the program.")
        print("Please choose an option by number:")
        print("1) Register new customer")
        print("2) Add driver details for a customer")
        print("3) List available cars")
        print("4) Create new rental booking")
        print("5) Record payment")
        print("6) Report car damage")
        print("7) List rentals for a customer")
        print("8) List all rentals")
        print("9) Exit program")

        ch = prompt_exit("\nPlease enter your choice: ")
        try:
            choice = int(ch)
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 9 or type 'exit'.")
            continue

        if choice == 1:
            register_customer()
        elif choice == 2:
            add_driver_details()
        elif choice == 3:
            list_available_cars()
        elif choice == 4:
            create_rental()
        elif choice == 5:
            record_payment()
        elif choice == 6:
            report_damage()
        elif choice == 7:
            list_rentals_for_customer()
        elif choice == 8:
            list_rentals()
        elif choice == 9:
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.")


def cleanup_and_exit():
    # Close database and exit program
    try:
        if CONN is not None:
            CONN.close()
    except Exception:
        pass
    sys.exit(0)

def program():
    try:
        main_loop()
    finally:
        cleanup_and_exit()

program()