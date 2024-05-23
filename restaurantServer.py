from http.server import HTTPServer, BaseHTTPRequestHandler
from restaurantDatabase import RestaurantDatabase
from urllib.parse import parse_qs

class RestaurantPortalHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        self.database = RestaurantDatabase()
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        try:
            if self.path == '/addReservation':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                form = parse_qs(post_data.decode('utf-8'))


                
                try:
                    
                    customerId = int(form["customerId"][0])
                    reservationTime = form["reservationTime"][0]
                    numberOfGuests = int(form["numberOfGuests"][0])
                    specialRequests = form.get("specialRequests", [""])[0]

               
                
                
                    self.database.addReservation(customerId, reservationTime, numberOfGuests, specialRequests)
                    print("Reservation added for customer:", customerId)
                
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"<html><head><title>Add Reservation</title></head>")
                    self.wfile.write(b"<body>")
                    self.wfile.write(b"<a href='/'>Home</a><br>")
                    self.wfile.write(b"<a href='/addReservation'>Add Another Reservation</a><br>")
                    self.wfile.write(b"<a href='/viewReservations'>View Reservations</a></center>")
                    self.wfile.write(b"Thank You, Reservation Added")
                    self.wfile.write(b"</body></html>")
                
                    return
        
                except KeyError as e:

                    print(f"Missing data: {e}")

                    self.send_error(400, 'Missing value')

        except Exception as e:

            print(f"Error: {e}")

            self.send_error(500, 'Server error: {}'.format(str(e)))
                
     
    def do_GET(self):
        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addReservation'>Add Reservation</a>|\
                                  <a href='/deleteReservation'>Delete Reservation</a>|\
                                  <a href='/viewReservations'>View Reservations</a></div>")
                self.wfile.write(b"<hr><h2>All Reservations</h2>")
                self.wfile.write(b"<table border=2> \
                                    <tr><th> Reservation ID </th>\
                                        <th> Customer Name </th>\
                                        <th> Contact Info </th>\
                                        <th> Reservation Time </th>\
                                        <th> Number of Guests </th>\
                                        <th> Special Requests </th></tr>")
                records = self.database.getAllReservations()
                for row in records:
                    self.wfile.write(b' <tr> <td>')
                    self.wfile.write(str(row[0]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[1]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[2]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[3]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[4]).encode())
                    self.wfile.write(b'</td><td>')
                    self.wfile.write(str(row[5]).encode())
                    self.wfile.write(b'</td></tr>')
                
                self.wfile.write(b"</table></center>")
                self.wfile.write(b"</body></html>")
                return

            elif self.path == '/addReservation':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(b"<html><head><title>Add Reservation</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h2>Add Reservation</h2>")
                self.wfile.write(b"<form method='post' action='/addReservation'>")
                self.wfile.write(b"<label>CustomerId: </label>")
                self.wfile.write(b"<input type='text' name='customerId' required><br>")
                self.wfile.write(b"<label>Reservation Time: </label>")
                self.wfile.write(b"<input type='datetime-local' name='reservationTime' required><br>")
                self.wfile.write(b"<label>Number of Guests: </label>")
                self.wfile.write(b"<input type='text' name='numberOfGuests' required><br>")
                self.wfile.write(b"<label>Special Requests: </label>")
                self.wfile.write(b"<input type='text' name='specialRequests'><br>")
                self.wfile.write(b"<input type='submit' value='Add Reservation'>")
                self.wfile.write(b"</form>")
                self.wfile.write(b"</center></body></html>")
                return

            elif self.path == '/deleteReservation':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                self.wfile.write(b"<html><head><title>Delete Reservation</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h2>Delete Reservation</h2>")
                self.wfile.write(b"<form method='post' action='/deleteReservation'>")
                self.wfile.write(b"<label>Reservation ID to delete: </label>")
                self.wfile.write(b"<input type='text' name='reservation_id' required><br>")
                self.wfile.write(b"<input type='submit' value='Delete'>")
                self.wfile.write(b"</form>")
                self.wfile.write(b"</center></body></html>")
                return

            elif self.path == '/viewReservations':
                reservations = self.database.getAllReservations()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                self.wfile.write(b"<html><head><title>View Reservations</title></head>")
                self.wfile.write(b"<body>")
                self.wfile.write(b"<center><h1>View Reservations</h1>")
                self.wfile.write(b"<hr>")
                self.wfile.write(b"<div> <a href='/'>Home</a>| \
                                 <a href='/addReservation'>Add Reservation</a>|\
                                  <a href='/deleteReservation'>Delete Reservation</a>|\
                                  <a href='/viewReservations'>View Reservations</a></div>")
                self.wfile.write(b"<hr><h2>All Reservations</h2>")
                self.wfile.write(b"<table border=1>")
                self.wfile.write(b"<tr><th>Reservation ID</th><th>Customer Name</th><th>Contact Info</th><th>Reservation Time</th><th>Number of Guests</th><th>Special Requests</th></tr>")
                
                for row in reservations:
                    self.wfile.write(b"<tr>")
                    for item in row:
                        self.wfile.write(b"<td>")
                        self.wfile.write(str(item).encode())
                        self.wfile.write(b"</td>")
                    self.wfile.write(b"</tr>")
                    
                self.wfile.write(b"</table>")
                self.wfile.write(b"</center></body></html>")
                return
            
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

def run(server_class=HTTPServer, handler_class=RestaurantPortalHandler, port=8000):
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

run()
