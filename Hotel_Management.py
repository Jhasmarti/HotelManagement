import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",      
            password="***********",  
            database="hotelManagement"
        )
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

class Customer:
    def __init__(self, db):
        self.db = db
        self.id = None
        self.name = ""
        self.address = ""
        self.checkin = None
        self.checkout = None

    def register(self):
        print("\n--- Register Customer ---")
        self.name = input("Enter your name: ")
        self.address = input("Enter your address: ")
        in_date = input("Enter check-in date (dd/mm/yyyy): ")
        out_date = input("Enter check-out date (dd/mm/yyyy): ")

        try:
            self.checkin = datetime.strptime(in_date, "%d/%m/%Y").date()
            self.checkout = datetime.strptime(out_date, "%d/%m/%Y").date()
        except ValueError:
            print("Invalid date format, please use dd/mm/yyyy.")
            return False

        sql = "INSERT INTO customers (name, address, checkin, checkout) VALUES (%s, %s, %s, %s)"
        val = (self.name, self.address, self.checkin, self.checkout)
        self.db.cursor.execute(sql, val)
        self.db.commit()
        self.id = self.db.cursor.lastrowid
        print("\nCustomer registered successfully with ID:", self.id)
        return True

class Room:
    def __init__(self, db, customer_id):
        self.db = db
        self.customer_id = customer_id
        self.rent = 0

    def calculate_rent(self):
        print("\nAvailable Room Types:")
        print("1. Type A --> ₹1000 per night")
        print("2. Type B --> ₹2000 per night")
        print("3. Type C --> ₹3000 per night")
        print("4. Type D --> ₹4000 per night")

        try:
            choice = int(input("Choose your room type (1-4): "))
            nights = int(input("How many nights will you stay?: "))
        except ValueError:
            print("Invalid input.")
            return False

        rent_per_night = {1: 1000, 2: 2000, 3: 3000, 4: 4000}
        if choice not in rent_per_night:
            print("Invalid room type choice.")
            return False

        self.rent = rent_per_night[choice] * nights
        room_type = f"Type {chr(64+choice)}" 

        sql = "INSERT INTO rooms (customer_id, room_type, nights, rent) VALUES (%s, %s, %s, %s)"
        val = (self.customer_id, room_type, nights, self.rent)
        self.db.cursor.execute(sql, val)
        self.db.commit()

        print(f"Room booked: {room_type} for {nights} nights. Rent: ₹{self.rent}\n")
        return True

class Restaurant:
    menu = {
        1: ("Tea", 10),
        2: ("Coffee", 10),
        3: ("Colddrink", 20),
        4: ("Samosa", 10),
        5: ("Sandwich", 50),
        6: ("Dhokla", 30),
        7: ("Kachori", 10),
        8: ("Milk", 20),
        9: ("Noodles", 50),
        10: ("Pasta", 50),
        11: ("Pizza", 80),
        12: ("Burger", 50)
    }

    def __init__(self, db, customer_id):
        self.db = db
        self.customer_id = customer_id
        self.total_bill = 0

    def take_order(self):
        print("\n--- Restaurant Menu ---")
        for item_no, (name, amount) in self.menu.items():
            print(f"{item_no}. {name} - ₹{amount}")

        while True:
            choice = input("Enter your choice from the menu (or '0' to finish): ")
            if choice == '0':
                break

            if not choice.isdigit() or int(choice) not in self.menu:
                print("Invalid choice. Try again.")
                continue

            quantity = input("Enter quantity: ")
            if not quantity.isdigit():
                print("Invalid quantity. Try again.")
                continue

            choice = int(choice)
            quantity = int(quantity)

            item_name, item_price = self.menu[choice]
            cost = item_price * quantity
            self.total_bill += cost

            # Corrected SQL insert to match your table column names
            sql = "INSERT INTO orders (customer_id, item, quatity, amount) VALUES (%s, %s, %s, %s)"
            val = (self.customer_id, item_name, quantity, cost)
            self.db.cursor.execute(sql, val)
            self.db.commit()

            print(f"Added {quantity} {item_name}(s) - ₹{cost}")

        print(f"Total Restaurant Bill: ₹{self.total_bill}\n")

class Laundry:
    def __init__(self, db, customer_id):
        self.db = db
        self.customer_id = customer_id
        self.bill = 0

    def calculate_bill(self):
        print("Laundry charges ₹10 per cloth.")
        try:
            clothes = int(input("Enter number of clothes: "))
        except ValueError:
            print("Invalid input.")
            return False

        self.bill = clothes * 10

        sql = "INSERT INTO laundry (customer_id, clothes_count, amount) VALUES (%s, %s, %s)"
        val = (self.customer_id, clothes, self.bill)
        self.db.cursor.execute(sql, val)
        self.db.commit()

        print(f"Laundry Bill: ₹{self.bill}\n")
        return True

class Hotel:
    def __init__(self):
        self.db = Database()
        self.customer = None
        self.room = None
        self.restaurant = None
        self.laundry = None

    def total_bill(self):
        # Calculate total from DB for the customer
        cust_id = self.customer.id

        self.db.cursor.execute("SELECT rent FROM rooms WHERE customer_id = %s", (cust_id,))
        room_rent = sum(r[0] for r in self.db.cursor.fetchall())

        self.db.cursor.execute("SELECT amount FROM orders WHERE customer_id = %s", (cust_id,))
        rest_bill = sum(r[0] for r in self.db.cursor.fetchall())

        self.db.cursor.execute("SELECT amount  FROM laundry WHERE customer_id = %s", (cust_id,))
        laundry_bill = sum(r[0] for r in self.db.cursor.fetchall())

        total = room_rent + rest_bill + laundry_bill

        print("\n----- Final Bill Summary -----")
        print(f"Customer Name: {self.customer.name}")
        print(f"Room Rent: ₹{room_rent}")
        print(f"Restaurant Bill: ₹{rest_bill}")
        print(f"Laundry Bill: ₹{laundry_bill}")
        print(f"Total Amount to Pay: ₹{total}")
        print("--------------------------------\n")

    def menu(self):
        while True:
            print("===== HOTEL MENU =====")
            print("1. Register Customer and Book Room")
            print("2. Order Food")
            print("3. Laundry Bill")
            print("4. Checkout and View Bill")
            print("5. Exit")
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.customer = Customer(self.db)
                if self.customer.register():
                    self.room = Room(self.db, self.customer.id)
                    self.room.calculate_rent()
                    self.restaurant = Restaurant(self.db, self.customer.id)
                    self.laundry = Laundry(self.db, self.customer.id)
                else:
                    self.customer = None
            elif choice == '2':
                if self.customer:
                    self.restaurant.take_order()
                else:
                    print("Please register customer first!\n")
            elif choice == '3':
                if self.customer:
                    self.laundry.calculate_bill()
                else:
                    print("Please register customer first!\n")
            elif choice == '4':
                if self.customer:
                    self.total_bill()
                    # Reset for next customer
                    self.customer = None
                    self.room = None
                    self.restaurant = None
                    self.laundry = None
                else:
                    print("No active customer to checkout.\n")
            elif choice == '5':
                print("Thank you for using our hotel service!")
                self.db.close()
                break
            else:
                print("Invalid choice! Please try again.\n")

if __name__ == "__main__":
    hotel = Hotel()
    hotel.menu()
