CREATE TABLE Cars (
  carID SERIAL PRIMARY KEY,
  brand VARCHAR(50) NOT NULL,
  model VARCHAR(50) NOT NULL,
  plateNumber VARCHAR(15) UNIQUE NOT NULL,
  year INTEGER,
  color VARCHAR(20),
  carType VARCHAR(30),
  size VARCHAR(20),
  transmission VARCHAR(20),
  fuelType VARCHAR(20),
  seats INTEGER,
  bags INTEGER,
  status VARCHAR(20) DEFAULT 'Available',
  dailyPrice INTEGER,
  information TEXT
);

CREATE TABLE customers (
  userID SERIAL PRIMARY KEY,
  fullName VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  phone VARCHAR(20) UNIQUE,
  address VARCHAR(255)
);

CREATE TABLE driverDetails (
  driverID SERIAL PRIMARY KEY,
  userID INTEGER REFERENCES customers(userID) ON DELETE CASCADE,
  licenseNumber VARCHAR(30) UNIQUE NOT NULL,
  licenseExpiry DATE, 
  nationalID VARCHAR(20),
  passportNumber VARCHAR(20),
  dateOfBirth DATE
);

CREATE TABLE locations (
  locationID SERIAL PRIMARY KEY,
  locationName VARCHAR(100) NOT NULL,
  address VARCHAR(255),
  city VARCHAR(50)
);

CREATE TABLE rentals (
  bookingID SERIAL PRIMARY KEY,
  userID INTEGER REFERENCES customers(userID),
  carID INTEGER REFERENCES Cars(carID),
  pickUpLocationID INTEGER REFERENCES locations(locationID),
  dropOffLocationID INTEGER REFERENCES locations(locationID),
  pickupDate DATE NOT NULL,
  pickupTime TIME NOT NULL,
  dropoffDate DATE NOT NULL,
  dropoffTime TIME NOT NULL,
  totalAmount INTEGER,
  bookingStatus VARCHAR(20) DEFAULT 'Pending'
);

CREATE TABLE Payments (
  paymentID SERIAL PRIMARY KEY,
  bookingID INTEGER REFERENCES rentals(bookingID),
  paymentDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  paymentMethod VARCHAR(50),
  amountPaid INTEGER
);

CREATE TABLE damage (
  damageID SERIAL PRIMARY KEY,
  carID INTEGER REFERENCES Cars(carID),
  reportDate DATE DEFAULT CURRENT_DATE,
  description TEXT,
  repairCost INTEGER
);


INSERT INTO Cars (brand, model, plateNumber, year, color, carType, size, transmission, fuelType, seats, bags, dailyPrice) 
  VALUES
    ('Toyota', 'Camry', '45A123', 2023, 'Silver', 'Sedan', 'Medium', 'Automatic', 'Gasoline', 5, 2, 50),
    ('Tesla', 'Model 3', '12B789', 2022, 'White', 'Electric', 'Medium', 'Automatic', 'Electric', 5, 1, 120),
    ('Ford', 'Explorer', '88C456', 2021, 'Black', 'SUV', 'Large', 'Automatic', 'Gasoline', 7, 3, 90),
    ('Hyundai', 'i10', '33D111', 2023, 'Blue', 'Economy', 'Small', 'Manual', 'Gasoline', 4, 1, 35);


INSERT INTO customers (fullName, email, password, phone, address) 
  VALUES
    ('John Smith', 'john@example.com', 'hashed_pw_1', '+1202555011', '123 Maple St, NY'),
    ('Sarah Miller', 'sarah.m@test.com', 'hashed_pw_2', '+1202555022', '456 Oak Ave, LA'),
    ('Mike Ross', 'm.ross@law.com', 'hashed_pw_3', '+1202555033', '789 Pine Rd, Chicago'),
    ('Emma Wilson', 'emma.w@mail.com', 'hashed_pw_4', '+1202555044', '101 Cedar Ln, Miami');


INSERT INTO driverDetails (userID, licenseNumber, licenseExpiry, nationalID, dateOfBirth) 
  VALUES
    (1, 'DL-998877', '2028-05-20', 'N-554433', '1990-01-15'),
    (2, 'DL-112233', '2026-11-10', 'N-112233', '1985-06-25'),
    (3, 'DL-445566', '2030-01-01', 'N-445566', '1995-12-12'),
    (4, 'DL-778899', '2027-08-15', 'N-778899', '1992-03-30');


INSERT INTO locations (locationName, city, address) 
  VALUES
    ('JFK Airport', 'New York', 'Terminal 4 Arrival'),
    ('Downtown Branch', 'Los Angeles', '222 Sunset Blvd'),
    ('Central Station', 'Chicago', 'Suite 10, Main Hall'),
    ('Miami Beach', 'Miami', '55 Ocean Drive');


INSERT INTO rentals (userID, carID, pickUpLocationID, dropOffLocationID, pickupDate, pickupTime, dropoffDate, dropoffTime, totalAmount, bookingStatus) 
  VALUES
    (1, 1, 1, 1, '2024-01-10', '10:00:00', '2024-01-13', '10:00:00', 150, 'Completed'),
    (2, 2, 2, 2, '2024-02-15', '09:00:00', '2024-02-18', '09:00:00', 360, 'Confirmed'),
    (3, 3, 3, 3, '2024-03-01', '14:00:00', '2024-03-06', '12:00:00', 450, 'Active'),
    (4, 4, 1, 4, '2024-03-10', '11:00:00', '2024-03-13', '11:00:00', 105, 'Pending');


INSERT INTO Payments (bookingID, paymentDate, paymentMethod, amountPaid) 
  VALUES
    (1, '2024-01-10 09:30:00', 'Credit Card', 150),
    (2, '2024-02-14 14:00:00', 'PayPal', 360),
    (3, '2024-03-01 10:15:00', 'Debit Card', 450),
    (4, '2024-03-10 11:00:00', 'Cash', 105);


INSERT INTO damage (carID, reportDate, description, repairCost) 
  VALUES
    (4, '2024-02-01', 'Small scratch on rear bumper', 150),
    (3, '2024-03-15', 'Cracked side mirror', 80);