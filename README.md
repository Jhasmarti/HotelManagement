# Hotel Management System

A simple console-based Hotel Management System built in Python using MySQL for database management.  
The system allows registering customers, booking rooms, ordering food, managing laundry bills, and generating the final bill summary.

---

## Features

- **Customer Registration:** Input customer details and check-in/check-out dates.
- **Room Booking:** Choose room types and calculate rent based on stay duration.
- **Restaurant Ordering:** Select items from the menu, specify quantity, and calculate restaurant bills.
- **Laundry Service:** Calculate laundry charges based on the number of clothes.
- **Billing:** Generate and display a detailed bill summary including room rent, restaurant orders, and laundry charges.
- **Database Integration:** All data stored and managed using MySQL.

---

## Technologies Used

- Python 3
- MySQL Database
- `mysql-connector-python` for Python-MySQL connectivity
- `datetime` module for date handling

---

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/hotel-management-system.git
    cd hotel-management-system
    ```

2. **Install required Python package:**
    ```bash
    pip install mysql-connector-python
    ```

3. **Set up MySQL database:**

   - Create a database named `hotelManagement`.
   - Create tables (`customers`, `rooms`, `orders`, `laundry`) with appropriate columns.  
   
   Example SQL to create tables:
   ```sql
   CREATE DATABASE hotelManagement;
   USE hotelManagement;

   CREATE TABLE customers (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255),
       address VARCHAR(255),
       checkin DATE,
       checkout DATE
   );

   CREATE TABLE rooms (
       id INT AUTO_INCREMENT PRIMARY KEY,
       customer_id INT,
       room_type VARCHAR(50),
       nights INT,
       rent INT,
       FOREIGN KEY (customer_id) REFERENCES customers(id)
   );

   CREATE TABLE orders (
       id INT AUTO_INCREMENT PRIMARY KEY,
       customer_id INT,
       item VARCHAR(255),
       quatity INT,
       amount INT,
       FOREIGN KEY (customer_id) REFERENCES customers(id)
   );

   CREATE TABLE laundry (
       id INT AUTO_INCREMENT PRIMARY KEY,
       customer_id INT,
       clothes_count INT,
       amount INT,
       FOREIGN KEY (customer_id) REFERENCES customers(id)
   );
