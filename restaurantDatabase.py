## 

import mysql.connector
from mysql.connector import Error

class RestaurantDatabase:
    def __init__(self,
                 host="localhost",
                 port="3306",
                 database="restaurants_reservations",
                 user='root',
                 password='monkey1234'):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password)
            
            if self.connection.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            print("Error while connecting to MySQL", e)

    def addReservation(self, customerId, reservationTime, numberOfGuests, specialRequests):
        ''' Method to insert a new reservation into the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            # Add reservation
            query = "INSERT INTO reservations (customerId, reservationTime, numberOfGuests, specialRequests) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (customerId, reservationTime, numberOfGuests, specialRequests))
            self.connection.commit()
            print("Reservation added successfully")
            return

    def getAllReservations(self):
        ''' Method to get all reservations from the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = """
            SELECT r.reservationId, c.customerName, c.contactInfo, r.reservationTime, r.numberOfGuests, r.specialRequests
            FROM reservations r
            JOIN customers c ON r.customerId = c.customerId
            """
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def deleteReservation(self, reservation_id):
        ''' Method to delete a reservation from the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "DELETE FROM reservations WHERE reservationId = %s"
            self.cursor.execute(query, (reservation_id,))
            self.connection.commit()
            print("Reservation deleted successfully")

if __name__ == "__main__":
    db = RestaurantDatabase()
    # Example usage
    db.addReservation("John Doe", "555-1234", "2024-05-25 19:00", 4, "Window seat")
    reservations = db.getAllReservations()
    for reservation in reservations:
        print(reservation)
