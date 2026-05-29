# 🚗 Car Rental System

A simple terminal-based car rental management system built with Python and PostgreSQL.
This project allows users to manage customers, rentals, payments, car availability, and damage reports directly from the command line.

The main focus of this project was practicing database design, SQL relationships, and backend logic using Python.
Some minor styling/formatting ideas and cleanup were improved with AI assistance during development.

---

## ✨ Features

Register new customers

Add driver/license details

View available cars

Create rental bookings

Record customer payments

Track rental status

Report car damages

View rentals for specific customers

PostgreSQL database integration

Input validation and error handling

---

## 🛠️ Technologies Used

Python
PostgreSQL
psycopg
SQL

---

### 📂 Project Structure

Program.py # Main application logic
carrent.sql # Database schema + sample data

---

## 🗄️ Database Design

The database includes multiple related tables such as:

Cars

Customers

DriverDetails

Rentals

Payments

Locations

Damage Reports

Relationships are handled using foreign keys to keep the data connected and consistent.

---

## ⚙️ Setup & Installation

1. Clone the repository

2. Install dependencies
   pip install psycopg

3. Create the PostgreSQL database
   Create a database named:
   carrent

4. Run the SQL file
   Import the database schema and sample data:
   psql -U postgres -d carrent -f carrent.sql

5. Configure database connection
   Inside Program.py, update the connection settings if needed:
   CONN = psycopg.connect( dbname="carrent", user="postgres", password="postgres", host="localhost", port="5432", )

6. Run the program
   python Program.py

---

## 🖥️ Example Menu

1. Register new customer 2) Add driver details 3) List available cars 4) Create rental booking 5) Record payment 6) Report car damage 7) List rentals for a customer 8) List all rentals 9) Exit

---

## 📌 What I Practiced In This Project

Writing SQL queries

Database normalization

Working with PostgreSQL using Python

CRUD operations

Handling user input safely

Structuring a larger terminal application

Error handling and validation

---

## 🚧 Possible Future Improvements

Build a Django web version

Add authentication & password hashing

Improve rental date conflict checking

Add admin/user roles

Create a GUI or REST API

Docker support

Better reporting system

---

### 📄 Notes

This project was created mainly for learning and practicing backend development concepts and database management.
The code is intentionally written in a clear and beginner-friendly style for easier understanding and maintenance.

---

### 👨‍💻 Author

Created by Afrooz Behrooznick
