from http.server import HTTPServer, BaseHTTPRequestHandler
from validate import validate_date, validate_phone, validate_email, validate_time, validate_number_of_guests, serialize_datetime
from authenticate import JWTHandler, hash_password, verify_password, SECRET
import json
import mysql.connector
import os 

SECRET_KEY = SECRET

# Establish connection to MySQL
db_connection = mysql.connector.connect(
    user=os.getenv('MYSQL_USER'), 
    password=os.getenv('MYSQL_ROOT_PASSWORD'), 
    host=os.getenv('_HOST'),
    port=3306,
    database=os.getenv('MYSQL_DATABASE'))
print("DB connected")

cursor = db_connection.cursor()

# Pseudo-code for setting headers
headers = {
    'Content-type': 'application/json',
    'Access-Control-Allow-Origin': 'http://localhost:3000',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Credentials': 'true',
}

class RequestHandler(BaseHTTPRequestHandler):
           
    def do_OPTIONS(self):
        self.send_response(200)
        for header, value in headers.items():
            self.send_header(header, value)
        self.send_header('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')
        self.end_headers()

    
    # Set the HTTP response status and header
    def set_Response(self, status_code, message):
        self.send_response(status_code)
        for header, value in headers.items():
            self.send_header(header, value)
        self.end_headers()
        data = json.dumps(message)
        print(data)
        self.wfile.write(data.encode())
    
    def verify_user(self):
        header = self.headers.get('Authorization')
        if header:
            parts = header.split(' ')
            token = parts[1] if len(parts) == 2 else header
            value = JWTHandler.verify_token(token)
            if value.get("message"):
                self.set_Response(401, value)
                return False
            else:
                return value
        else:
            self.set_Response(401, {'message': 'unauthorized, no authorization header provided'})
            return False
        
    def authenticate(self, email, password):
        query = "SELECT password_hash FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        if user:
            if verify_password(password, user[0]):
                return user
            else:
                return {"message": "invalid password"}
        else:
            return {"message": "user not found"}
        
    
    '''
        # HTTP REQUEST METHODS
        
        GET     /login                  authenticates a user
        GET     /users                  returns all users
        GET     /profile                returns your profile info
        GET     /reservations           returns all reservations
        GET     /reservations/:id       returns a specific reservation
        GET     /reservations/due       returns all reservations due today
        
        POST     /register              creates a new user
        POST     /reservations          creates a new reservation
        
        PUT     /profile                updates your profile
        PUT     /reservations/:id       updates a specific reservation
        
        DELETE  /reservations/:id       deletes a specific reservation
        
    '''
    
    # HTTP routes and endpoints
    
    def do_GET(self):
        paths = self.path.split('/')
            
        if len(paths) > 2 and paths[1] == 'api':
            if paths[2] == 'users':
                self.return_all_users()
            elif paths[2] == 'profile':
                self.return_profile_info()
            elif paths[2] == 'reservations':
                if len(paths) > 3:
                    if paths[3] == 'due':
                        self.return_reservations_due_today()
                    else:
                        self.return_specific_reservation(paths[3])
                else:
                    self.return_all_reservations()
            else:
                self.send_error(404, 'Not Found')
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        paths = self.path.split('/')
        
        if len(paths) > 2 and paths[1] == 'api':
            if paths[2] == 'login':
                self.authenticate_user()
            elif paths[2] == 'register':
                self.create_new_user()
            elif paths[2] == 'reservations':
                self.create_new_reservation()
            else:
                self.send_error(404, 'Not Found')
        else:
            self.send_error(404, 'Not Found')

    def do_PUT(self):
        paths = self.path.split('/')
        
        if len(paths) > 2 and paths[1] == 'api':
            if paths[2] == 'profile':
                self.update_profile()
            elif paths[2] == 'reservations' and len(paths) == 4:
                self.update_specific_reservation(paths[3])
            else:
                self.send_error(404, 'Not Found')
        else:
            self.send_error(404, 'Not Found')
        
    def do_DELETE(self):
        paths = self.path.split('/')
    
        if len(paths) > 2 and paths[1] == 'api':
            if paths[2] == 'reservations' and len(paths) == 4:
                self.delete_specific_reservation(paths[3])
            else:
                self.send_error(404, 'Not Found')
        else:
            self.send_error(404, 'Not Found')

        
    
    #####
    # FUNCTIONALITIES
    #####
    
    def authenticate_user(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        email = data.get('username')
        password = data.get('password')
        
        if email and password:
            user = self.authenticate(email, password)
            if 'message' in user:
                self.set_Response(401, user)
            else:
                token = JWTHandler.generate_token({'email': email})
                self.set_Response(200, {'message': 'login successful', 'token': token})
        else:
            self.set_Response(400, {'message': 'Username or password not provided'})


    def create_new_user(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        user_type = int(data.get('type_id'))
        fullname = data.get('fullname', '')
        phone = data.get('phone', '')
        email = data.get('email', '')
        password = data.get('password', '')
        print(user_type, fullname, phone, email, password)
        
        if email and password and phone and fullname and user_type:
            if validate_email(email) and validate_phone(phone):
                query = "INSERT INTO users (type_id, email, fullname, phone, password_hash) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (user_type, email, fullname, phone, hash_password(password)))
                db_connection.commit()
                self.set_Response(201, {'message': 'User created successfully'})
            else:
                self.set_Response(400, {'message': 'Email or phone number is invalid'})
        else:
            self.set_Response(400, {'message': 'Bad Request'})


    def return_all_users(self):
        query = "SELECT * FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        if users:
            self.set_Response(200, users)
        else:
            self.set_Response(404, {'message': 'No users found'})


    def return_profile_info(self):
        user = self.verify_user()
        if user:
            query = "SELECT fullname, phone, email FROM users WHERE email = %s"
            cursor.execute(query, (user["email"],))
            profile = cursor.fetchone()
            prof = {
                    'fullname': profile[0],  
                    'phone': profile[1],   
                    'email': profile[2]      
                }
            self.set_Response(200, prof)
        else:
            self.set_Response(401, {'message': 'Unauthorized'})


    def return_all_reservations(self):
        payload = self.verify_user()
        if payload:
            query = "SELECT type_id, user_id FROM users WHERE email = %s"
            cursor.execute(query, (payload['email'],))
            user = cursor.fetchone()
            if user and user[0] == 2:
                query = "SELECT u.fullname, r.reservation_id, r.reservation_date, r.reservation_time, r.number_of_guests, r.created_at FROM reservations r JOIN users u ON r.user_id = u.user_id"
                cursor.execute(query)
                reservations = cursor.fetchall()
                if reservations:
                    reserve = [
                        {
                            'fullname': reservation[0],
                            'reservation_id': reservation[1],
                            'reservation_date': serialize_datetime(reservation[2]) if reservation[2] else None,
                            'reservation_time': serialize_datetime(reservation[3]) if reservation[3] else None,
                            'number_of_guests': reservation[4],
                            'created_at': serialize_datetime(reservation[5]) if reservation[5] else None,
                        } for reservation in reservations
                    ]
                    self.set_Response(200, reserve)
                else:
                    self.set_Response(404, {'message': 'No reservations found'})
            else:
                query = "SELECT reservation_id, reservation_date, reservation_time, number_of_guests, created_at FROM reservations WHERE user_id = %s"
                cursor.execute(query, (user[1],))
                reservations = cursor.fetchall()
                if reservations:
                    reserve = [
                        {
                            'reservation_id': reservation[0],
                            'reservation_date': serialize_datetime(reservation[1]) if reservation[1] else None,
                            'reservation_time': serialize_datetime(reservation[2]) if reservation[2] else None,
                            'number_of_guests': reservation[3],
                            'created_at': serialize_datetime(reservation[4]) if reservation[4] else None,
                        } for reservation in reservations
                    ]
                    self.set_Response(200, reserve)
                else:
                    self.set_Response(404, {'message': 'No reservations found for the user'})
        else:
            self.set_Response(401, {'message': 'Unauthorized'})


    def return_specific_reservation(self, reservation_id):
        query = "SELECT user_id, reservation_id, reservation_date, reservation_time, number_of_guests, created_at FROM reservations WHERE reservation_id = %s"
        cursor.execute(query, (reservation_id,))
        reservation = cursor.fetchone()
        
        if reservation:
            reserve = {
                'user_id': reservation[0],
                'reservation_id': reservation[1],
                'reservation_date': serialize_datetime(reservation[2]) if reservation[2] else None,
                'reservation_time': serialize_datetime(reservation[3]) if reservation[3] else None,
                'number_of_guests': reservation[4],
                'created_at': serialize_datetime(reservation[5]) if reservation[5] else None,
            }
            self.set_Response(200, reserve)
        else:
            self.set_Response(404, {'message': 'Reservation not found'})


    def return_reservations_due_today(self):
        query = "SELECT user_id, reservation_id, reservation_date, reservation_time, number_of_guests, created_at FROM reservations WHERE reservation_date = CURDATE()"
        cursor.execute(query)
        reservations = cursor.fetchall()
        if reservations:
            reserve = [
                {
                    'user_id': reservation[0],
                    'reservation_id': reservation[1],
                    'reservation_date': serialize_datetime(reservation[2]) if reservation[2] else None,
                    'reservation_time': serialize_datetime(reservation[3]) if reservation[3] else None,
                    'number_of_guests': reservation[4],
                    'created_at': serialize_datetime(reservation[5]) if reservation[5] else None,
                } for reservation in reservations
            ]
            self.set_Response(200, reserve)
        else:
            self.set_Response(404, {'message': 'No due reservations'})


    def create_new_reservation(self):
        user = self.verify_user()
        if user:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            reservation_date = data.get('reservation_date')
            reservation_time = data.get('reservation_time')
            number_of_guests = int(data.get('number_of_guests'))
            
            if reservation_date and reservation_time and number_of_guests:
                if validate_date(reservation_date) and validate_time(reservation_time) and validate_number_of_guests(number_of_guests):
                    query = "SELECT user_id FROM users WHERE email = %s"
                    cursor.execute(query, (user['email'],))
                    user_id = cursor.fetchone()
                    query = "INSERT INTO reservations (user_id, reservation_date, reservation_time, number_of_guests) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (user_id[0], reservation_date, reservation_time, number_of_guests))
                    db_connection.commit()
                    self.set_Response(201, {'message': 'Reservation created successfully'})
                else:
                    self.set_Response(400, {'message': 'Guest cannot be less than 1 or greater than 8, and date and time must be in the future'})
        else:
            self.set_Response(401, {'message': 'Unauthorized'})


    def update_profile(self):
        user = self.verify_user()
        if user:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            phone = data.get('phone')
            fullname = data.get('fullname')
            
            if phone and fullname:
                if validate_phone(phone):
                    query = "SELECT user_id FROM users WHERE email = %s"
                    cursor.execute(query, (user['email'],))
                    user_id = cursor.fetchone()
                    query = "UPDATE users SET email = %s, fullname = %s, phone = %s WHERE user_id = %s"
                    cursor.execute(query, (user['email'], fullname, phone, user_id[0]))
                    db_connection.commit()
                    self.set_Response(200, {'message': 'Profile updated successfully'})
                else:
                    self.set_Response(400, {'message': 'Phone number is invalid, format: 123xxxxxxx'})
            else:
                self.set_Response(400, {'message': 'Form data incomplete'})
        else:
            self.set_Response(401, {'message': 'Unauthorized'})


    def update_specific_reservation(self, reservation_id):
        user = self.verify_user()
        if user:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            reservation_date = data.get('reservation_date')
            reservation_time = data.get('reservation_time')
            number_of_guests = int(data.get('number_of_guests'))
            
            if reservation_date and reservation_time and number_of_guests:
                if validate_date(reservation_date) and validate_time(reservation_time) and validate_number_of_guests(number_of_guests):
                    query = "SELECT user_id FROM users WHERE email = %s"
                    cursor.execute(query, (user['email'],))
                    user_id_result = cursor.fetchone()
                    
                    if user_id_result is not None:
                        user_id = user_id_result[0]
                        query = "UPDATE reservations SET reservation_date = %s, reservation_time = %s, number_of_guests = %s WHERE reservation_id = %s AND user_id = %s"
                        cursor.execute(query, (reservation_date, reservation_time, number_of_guests, reservation_id, user_id))
                        db_connection.commit()
                        self.set_Response(200, {'message': 'Reservation updated successfully'})
                    else:
                        self.set_Response(404, {'message': 'User not found'})
                else:
                    self.set_Response(400, {'message': 'Number of guests must be between 1 and 8, and date and time must be in the future'})
        else:
            self.set_Response(401, {'message': 'Unauthorized'})
  
          
    def delete_specific_reservation(self, reservation_id):
        user = self.verify_user()
        if user:
            query = "SELECT user_id FROM users WHERE email = %s"
            cursor.execute(query, (user['email'],))
            user_id_result = cursor.fetchone()
            
            if user_id_result:
                user_id = user_id_result[0]
                check_query = "SELECT * FROM reservations WHERE reservation_id = %s AND user_id = %s"
                cursor.execute(check_query, (reservation_id, user_id))
                reservation = cursor.fetchone()
                
                if reservation:
                    delete_query = "DELETE FROM reservations WHERE reservation_id = %s AND user_id = %s"
                    cursor.execute(delete_query, (reservation_id, user_id))
                    db_connection.commit()
                    
                    if cursor.rowcount > 0:
                        self.set_Response(200, {'message': 'Reservation deleted successfully'})
                    else:
                        # In case the delete operation did not affect any rows
                        self.set_Response(404, {'message': 'No reservation found to delete'})
                else:
                    self.set_Response(404, {'message': 'Reservation not found'})
            else:
                self.set_Response(401, {'message': 'User not found'})
        else:
            self.set_Response(401, {'message': 'Unauthorized'})



def run(serverClass=HTTPServer, handlerClass=RequestHandler, port=8080):
    serverAddress = ('', port)
    httpd = HTTPServer(serverAddress, RequestHandler)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd server..')
    # close the mySQL connection
    cursor.close()
    db_connection.close()

if __name__ == '__main__':
    run()    