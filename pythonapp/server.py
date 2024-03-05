from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
import bcrypt 
import json
import mysql.connector
import os 
import jwt

load_dotenv('./.env')


#replace the secret key with yours
SECRET_KEY = os.getenv('SECRET_KEY')

# Establish connection to MySQL
db_connection = mysql.connector.connect(
    user=os.getenv('MYSQL_USER'), 
    password=os.getenv('MYSQL_ROOT_PASSWORD'), 
    host=os.getenv('_HOST'),
    port=3306,
    database=os.getenv('MYSQL_DATABASE'))
print("DB connected")

cursor = db_connection.cursor()

class JWTHandler:
    @staticmethod
    def generate_token(data):
        token = jwt.encode(data, SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return {"message": "token expired. pls log in again."}
        except jwt.InvalidTokenError:
            return {"message": "invalid token. pls log in again."}

class RequestHandler(BaseHTTPRequestHandler):
    
    # Set the HTTP response status and header
    def set_Response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(message).encode())
    
    def verify_user(self):
        token = self.headers.get('Authorization')
        if token:
            value = JWTHandler.verify_token(token)
            if type(value) is not 'dict':
                return value
            else:
                self.set_Response(401, value)
                return False
        else:
            self.set_Response(401, {'message': 'unauthorized'})
            return False
    
    '''
        # HTTP REQUEST METHODS
        
        GET     /register               creates a new user
        GET     /login                  authenticates a user
        GET     /profile                returns your profile info
        GET     /healthcare             returns all healthcare providers
        GET     /healthcare/me          returns the user's healthcare provider
        
        GET     /health_records         returns all health rec
        GET     /health_records/:id     returns a specific health rec
        GET     /permissions            returns all the permissions
        
        GET     /reminders              returns all reminders
        GET     /reminders/due          returns all due reminders
        GET     /reminders/:id          returns a specific reminder
        
        POST    /health_records         creates a new health rec
        POST    /reminders              creates a new reminder
        POST    /healthcare             creates a new healthcare provider
        
        PUT     /profile                updates your profile
        PUT     /health_records/:id     updates a specific health rec
        PUT     /reminders/:id          updates a specific reminder
        PUT     /permissions/:id1/:id2  updates a specific permission
        
        DELETE  /health_records/:id     deletes a specific health rec
        DELETE  /reminders/:id          deletes a specific reminder
        DELETE  /users/:id              deletes a specific user
        
    '''
    
    # HTTP routes and endpoints
    
    def do_GET(self):
        paths = self.path.split('/')
        
        if paths[1] == 'register':
            self.create_new_user()
        elif paths[1] == 'login':
            self.authenticate_user()
        elif paths[1] == 'profile':
            self.get_profile_info()
        elif paths[1] == 'healthcare':
            if paths[2] == 'me':
                self.get_user_healthcare_provider()
            else:
                self.get_all_healthcare_providers()
        elif paths[1] == 'health_records':
            if len(paths) == 2:
                self.get_all_health_records()
            else:
                record_id = paths[2]
                self.get_specific_health_record(record_id)
        elif paths[1] == 'permissions':
            self.get_all_permissions()
        elif paths[1] == 'reminders':
            if len(paths) == 2:
                self.get_all_reminders()
            elif paths[2] == 'due':
                self.get_due_reminders()
            else:
                reminder_id = paths[2]
                self.get_specific_reminder(reminder_id)

    def do_POST(self):
        paths = self.path.split('/')
        
        if paths[1] == 'health_records':
            self.create_new_health_record()
        elif paths[1] == 'reminders':
            self.create_new_reminder()
        elif paths[1] == 'healthcare':
            self.create_new_healthcare_provider()

    def do_PUT(self):
        paths = self.path.split('/')
        
        if paths[1] == 'profile':
            self.update_profile()
        elif paths[1] == 'health_records':
            record_id = paths[2]
            self.update_health_record(record_id)
        elif paths[1] == 'reminders':
            reminder_id = paths[2]
            self.update_reminder(reminder_id)
        elif paths[1] == 'permissions':
            id1 = paths[2]
            id2 = paths[3]
            self.update_permission(id1, id2)

    def do_DELETE(self):
        paths = self.path.split('/')
        
        if paths[1] == 'health_records':
            record_id = paths[2]
            self.delete_health_record(record_id)
        elif paths[1] == 'reminders':
            reminder_id = paths[2]
            self.delete_reminder(reminder_id)
        elif paths[1] == 'users':
            user_id = paths[2]
            self.delete_user(user_id)

    
    # FUNCTIONALITIES
    
    def create_new_user(self):
        
        content_len = int(self.headers['Content-Length'])
        data_rec = self.rfile.read(content_len)
        data = json.loads(data_rec.decode())
        user_type = data.get('type_id', '')
        fullname = data.get('fullname', '')
        contact = data.get('contact', '')
        email = data.get('email', '')
        password = data.get('password', '')

        if user_type and fullname and contact and email and password:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                self.set_Response(400, {'message': 'user already exists'})
                return

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_password_utf8 = hashed_password.decode('utf-8')
            cursor.execute("INSERT INTO users (type_id, fullname, contact, email, password_hash) VALUES (%s, %s, %s, %s, %s)", 
                           (user_type, fullname, contact, email, hashed_password_utf8))
            db_connection.commit()
            token = JWTHandler.generate_token({'email': email})
            self.set_Response(200, {'message': 'user created successfully', 'token': token})
        else:
            self.set_Response(400, {'message': 'bad request'})
    
    
    def authenticate_user(self):
        
        content_len = int(self.headers['Content-Length'])
        data_rec = self.rfile.read(content_len)
        data = json.loads(data_rec.decode())
        email = data.get('email', '')
        password = data.get('password', '')
    
        if email and password:
            cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                password_hash = user[0]
                if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                    token = JWTHandler.generate_token({'email': email})
                    self.set_Response(200, {'message': 'login successful', 'token': token})
                else:
                    self.set_Response(401, {'message': 'incorrect password'})
            else:
                self.set_Response(404, {'message': 'user not found'})
        else:
            self.set_Response(400, {'message': 'bad request'})

    
    def get_profile_info(self):
        
        email = self.verify_user()
        if email:
            cursor.execute("SELECT fullname, contact, email FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                profile = {
                    'fullname': user[0],  
                    'contact': user[1],   
                    'email': user[2]      
                }
                self.set_Response(200, profile)
            else:
                self.set_Response(404, {'message': 'user not found'})

    
    def get_all_healthcare_providers(self):
        
        email = self.verify_user()
        if email:
            cursor.execute("SELECT type_id FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                type_id = result[0]
                cursor.execute("SELECT can_view FROM permissions WHERE type_id = %s AND resource_id = 3", (type_id,))
                can_view = cursor.fetchone()
                if can_view and can_view[0]:
                    cursor.execute("SELECT provider_id, provider_name, provider_address, provider_contact FROM healthcare_providers")
                    healthcare_providers = cursor.fetchall()
                    providers_list = [
                        {'provider_id': provider[0], 'provider_name': provider[1], 'provider_address': provider[2], 'provider_contact': provider[3]}
                        for provider in healthcare_providers
                    ]
                    self.set_Response(200, providers_list)
                else:
                    self.set_Response(403, {'message': 'no view permission'})
            else:
                self.set_Response(403, {'message': 'user not found or no type_id associated'})

    
    def get_user_healthcare_provider(self):
        
        email = self.verify_user()
        if email:
            cursor.execute("SELECT type_id, user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchall()
            cursor.execute("SELECT can_view FROM permissions WHERE type_id = %s AND resource_id = 4", (user['type_id'],))
            if cursor.fetchone():
                cursor.execute("SELECT * FROM users INNER JOIN user_provider ON users.user_id = user_provider.user_id INNER JOIN healthcare_providers ON user_provider.provider_id = healthcare_providers.provider_id WHERE user_id = %s", (user['user_id'],))
                healthcare_provider = cursor.fetchone()
                if healthcare_provider:
                    self.set_Response(200, healthcare_provider)
                else:
                    self.set_Response(404, {'message': 'no healthcare provider found, pls contact with customer service'})
            else:
                self.set_Response(403, {'message': 'no view permission'})

    
    def get_all_health_records(self):
        
        email = self.verify_user()
        if email:
            cursor.execute("SELECT type_id, user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                type_id, user_id = user
                cursor.execute("SELECT can_view FROM permissions WHERE type_id = %s AND resource_id = 2", (type_id,))
                can_view = cursor.fetchone()
                if can_view and can_view[0]:
                    cursor.execute("SELECT * FROM health_records WHERE user_id = %s", (user_id,))
                    health_records = cursor.fetchall()
                    records_list = [
                        {
                            'record_id': record[0],
                            'user_id': record[1],
                            'record_date': record[2],
                            'record_text': record[3]
                        }
                        for record in health_records
                    ]
                    self.set_Response(200, records_list)
                else:
                    self.set_Response(403, {'message': 'no view permission'})
            else:
                self.set_Response(404, {'message': 'user not found'})

    
    def get_specific_health_record(self, record_id):
        
        email = self.verify_user()
        if email:
            cursor.execute("SELECT type_id, user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                type_id, user_id = user
                cursor.execute("SELECT can_view FROM permissions WHERE type_id = %s AND resource_id = 2", (type_id,))
                can_view = cursor.fetchone()
                if can_view and can_view[0]:
                    cursor.execute("SELECT * FROM health_records WHERE user_id = %s AND record_id = %s", (user_id, record_id))
                    health_record = cursor.fetchone()
                    if health_record:
                        record = {
                            'record_id': health_record[0],
                            'user_id': health_record[1],
                            'record_date': health_record[2],
                            'record_text': health_record[3]
                        }
                        self.set_Response(200, record)
                    else:
                        self.set_Response(404, {'message': 'health record not found'})
                else:
                    self.set_Response(403, {'message': 'no view permission'})
            else:
                self.set_Response(404, {'message': 'user not found'})

    
    def get_all_permissions(self):
        
        email = self.verify_user()
        if email:
            cursor.execute("SELECT type_id FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                type_id = result[0]
                cursor.execute("SELECT * FROM permissions WHERE type_id = %s", (type_id,))
                permissions = cursor.fetchall()
                if permissions:
                    formatted_permissions = [{'resource_id': perm[0], 'type_id': perm[1], 'can_add': perm[2], 'can_view': perm[3], 'can_edit': perm[4]} for perm in permissions]
                    self.set_Response(200, formatted_permissions)
                else:
                    self.set_Response(404, {'message': 'no permissions found'})
            else:
                self.set_Response(403, {'message': 'no view permission'})

    
    def get_all_reminders(self):
        
        email = self.verify_user()
        if email:
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                user_id = result[0]
                cursor.execute("SELECT * FROM reminders WHERE user_id = %s", (user_id,))
                reminders = cursor.fetchall()
                if reminders:
                    formatted_reminders = [{'reminder_id': rem[0], 'user_id': rem[1], 'reminder_text': rem[2], 'reminder_date': rem[3]} for rem in reminders]
                    self.set_Response(200, formatted_reminders)
                else:
                    self.set_Response(404, {'message': 'no reminders found'})
            else:
                self.set_Response(403, {'message': 'user not found or no user_id associated'})

    def get_due_reminders(self):
        
        email = self.verify_user()
        if email:
            cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            if result:
                user_id = result[0]
                cursor.execute("SELECT * FROM reminders WHERE user_id = %s AND reminder_date BETWEEN CURDATE() AND CURDATE() + INTERVAL 1 DAY", (user_id,))
                reminders = cursor.fetchall()
                if reminders:
                    formatted_due_reminders = [{'reminder_id': rem[0], 'user_id': rem[1], 'reminder_text': rem[2], 'reminder_date': rem[3]} for rem in reminders]
                    self.set_Response(200, formatted_due_reminders)
                else:
                    self.set_Response(404, {'message': 'no due reminders'})
            else:
                self.set_Response(403, {'message': 'user not found or no user_id associated'})

    def get_specific_reminder(self, reminder_id):
        email = self.verify_user()
        if email:
            cursor.execute("SELECT type_id, user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                type_id, user_id = user
                cursor.execute("SELECT can_view FROM permissions WHERE type_id = %s AND resource_id = 5", (type_id,))
                can_view = cursor.fetchone()
                if can_view and can_view[0]:
                    cursor.execute("SELECT * FROM reminders WHERE user_id = %s AND reminder_id = %s", (user_id, reminder_id))
                    reminder = cursor.fetchone()
                    if reminder:
                        reminder_dict = {
                            'reminder_id': reminder[0],
                            'user_id': reminder[1],
                            'reminder_text': reminder[2],
                            'reminder_date': reminder[3]
                        }
                        self.set_Response(200, reminder_dict)
                    else:
                        self.set_Response(404, {'message': 'reminder not found'})
                else:
                    self.set_Response(403, {'message': 'no view permission'})

    def create_new_health_record(self):
        
        content_len = int(self.headers['Content-Length'])
        data_rec = self.rfile.read(content_len)
        data = json.loads(data_rec.decode())
        record_text = data.get('record_text', '')

        email = self.verify_user()
        if email and record_text:
            cursor.execute("SELECT type_id, user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                type_id, user_id = user
                cursor.execute("SELECT can_add FROM permissions WHERE type_id = %s AND resource_id = 2", (type_id,))
                can_add = cursor.fetchone()
                if can_add and can_add[0]:
                    cursor.execute("INSERT INTO health_records (user_id, record_text) VALUES (%s, %s)", (user_id, record_text))
                    db_connection.commit()
                    self.set_Response(200, {'message': 'health record created successfully'})
                else:
                    self.set_Response(403, {'message': 'no add permission'})
        else:
            self.set_Response(400, {'message': 'bad request'})
            
                

    def create_new_reminder(self):
        
        content_len = int(self.headers['Content-Length'])
        data_rec = self.rfile.read(content_len)
        data = json.loads(data_rec.decode())
        reminder_text = data.get('reminder_text', '')
        reminder_date = data.get('reminder_date', '')

        email = self.verify_user()
        if email and reminder_text and reminder_date:
            cursor.execute("SELECT type_id, user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                type_id, user_id = user
                cursor.execute("SELECT can_add FROM permissions WHERE type_id = %s AND resource_id = 5", (type_id,))
                can_add = cursor.fetchone()
                if can_add and can_add[0]:
                    cursor.execute("INSERT INTO reminders (user_id, reminder_text, reminder_date) VALUES (%s, %s, %s)", (user_id, reminder_text, reminder_date))
                    db_connection.commit()
                    self.set_Response(200, {'message': 'reminder created successfully'})
                else:
                    self.set_Response(403, {'message': 'no add permission'})
        else:
            self.set_Response(400, {'message': 'bad request'})

    
    def create_new_healthcare_provider(self):
        
        content_len = int(self.headers['Content-Length'])
        data_rec = self.rfile.read(content_len)
        data = json.loads(data_rec.decode())
        provider_name = data.get('provider_name', '')
        provider_address = data.get('provider_address', '')
        provider_contact = data.get('provider_contact', '')
        
        email = self.verify_user()
        if email:
            if provider_name and provider_address and provider_contact:
                cursor.execute("SELECT type_id, user_id FROM users WHERE email = %s", (email,))
                user = cursor.fetchall()
                cursor.execute("SELECT can_add FROM permissions WHERE type_id = %s AND resource_id = 3", (user['type_id'],))
                if cursor.fetchone():
                    cursor.execute("INSERT INTO healthcare_providers (provider_name, provider_address, provider_contact) VALUES (%s, %s, %s)", (provider_name, provider_address, provider_contact))
                    db_connection.commit()
                    self.set_Response(200, {'message': 'healthcare provider created successfully'})
                else:
                    self.set_Response(403, {'message': 'no add permission'})
            else:
                self.set_Response(400, {'message': 'bad request'})
    
    
    def update_profile(self):
        
        content_len = int(self.headers['Content-Length'])
        data_rec = self.rfile.read(content_len)
        data = json.loads(data_rec.decode())
        fullname = data.get('fullname', '')
        contact = data.get('contact', '')
        
        email = self.verify_user()
        if email:
            if fullname and contact:
                cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
                user_id_result = cursor.fetchone()
                if user_id_result:
                    user_id = user_id_result[0]
                    cursor.execute("UPDATE users SET fullname = %s, contact = %s WHERE user_id = %s", (fullname, contact, user_id))
                    db_connection.commit()
                    self.set_Response(200, {'message': 'profile updated successfully'})
            else:
                self.set_Response(400, {'message': 'user not found'})


    def update_health_record(self, record_id):
        
        content_len = int(self.headers['Content-Length'])
        data_rec = self.rfile.read(content_len)
        data = json.loads(data_rec.decode())
        record_text = data.get('record_text', '')
        
        email = self.verify_user()
        if email:
            cursor.execute("SELECT type_id, user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                user_id = user[1] 
                type_id = user[0]
                cursor.execute("SELECT can_edit FROM permissions WHERE type_id = %s AND resource_id = 2", (type_id,))
                can_edit = cursor.fetchone()
                if can_edit and can_edit[0]:
                    cursor.execute("UPDATE health_records SET record_text = %s WHERE user_id = %s AND record_id = %s", (record_text, user_id, record_id))
                    db_connection.commit()
                    self.set_Response(200, {'message': 'health record updated successfully'})
                else:
                    self.set_Response(403, {'message': 'no edit permission'})
            else:
                self.set_Response(404, {'message': 'user not found'})
        else:
            self.set_Response(400, {'message': 'bad request'})


    def update_reminder(self, reminder_id):
        
        content_len = int(self.headers['Content-Length'])
        data_rec = self.rfile.read(content_len)
        data = json.loads(data_rec.decode())
        reminder_text = data.get('reminder_text', '')
        reminder_date = data.get('reminder_date', '')
        
        if reminder_text and reminder_date:
            cursor.execute("SELECT type_id, user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                type_id, user_id = user
                cursor.execute("SELECT can_edit FROM permissions WHERE type_id = %s AND resource_id = 5", (type_id,))
                can_edit = cursor.fetchone()
                if can_edit and can_edit[0]:
                    cursor.execute("UPDATE reminders SET reminder_text = %s, reminder_date = %s WHERE user_id = %s AND reminder_id = %s", 
                                   (reminder_text, reminder_date, user_id, reminder_id))
                    db_connection.commit()
                    self.set_Response(200, {'message': 'reminder updated successfully'})
                else:
                    self.set_Response(403, {'message': 'no edit permission'})
            else:
                self.set_Response(404, {'message': 'reminder not found'})

    
    def update_permission(self, res_id, type_id):
        content_len = int(self.headers['Content-Length'])
        data_rec = self.rfile.read(content_len)
        data = json.loads(data_rec.decode())
        can_add = data.get('can_add', '')
        can_view = data.get('can_view', '')
        can_edit = data.get('can_edit', '')
        
        email = self.verify_user()
        if email:
            if can_add and can_view and can_edit:
                cursor.execute("SELECT type_id FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                type_id_u = user[0]
                cursor.execute("SELECT can_edit FROM permissions WHERE type_id = %s AND resource_id = 6", (type_id_u))
                if cursor.fetchone():
                    cursor.execute("SELECT * FROM permissions WHERE resource_id = %s AND type_id = %s", (res_id, type_id))
                    permission = cursor.fetchall()
                    if permission:
                        cursor.execute("UPDATE permissions SET can_add = %s, can_view = %s, can_edit = %s WHERE resource_id = %s AND type_id = %s", 
                           (can_add, can_view, can_edit, res_id, type_id))
                        db_connection.commit()
                        self.set_Response(200, {'message': 'permission updated successfully'})
                    else:
                        self.set_Response(404, {'message': 'permission not found'})
                else:
                    self.set_Response(403, {'message': 'no edit permission'})
            else:
                self.set_Response(400, {'message': 'bad request'})
        

    def delete_health_record(self, record_id):
        
        email = self.verify_user()
        if email:
            cursor.execute("SELECT type_id, user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchall()
            cursor.execute("SELECT can_edit FROM permissions WHERE type_id = %s AND resource_id = 2", (user['type_id'],))
            if cursor.fetchall():
                cursor.execute("SELECT * FROM health_records WHERE user_id = %s AND record_id = %s", (user['user_id'], record_id))
                health_rec = cursor.fetchall()
                if health_rec:
                    cursor.execute("DELETE FROM health_records WHERE user_id = %s AND record_id = %s", (user['user_id'], record_id))
                    db_connection.commit()
                    self.set_Response(200, {'message': 'health record deleted successfully'})
                else:
                    self.set_Response(404, {'message': 'health record not found'})
            else:
                self.set_Response(403, {'message': 'no edit permission'})

    
    def delete_reminder(self, reminder_id):
            
        email = self.verify_user()
        if email:
            cursor.execute("SELECT type_id, user_id FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                type_id, user_id = user
                cursor.execute("SELECT can_edit FROM permissions WHERE type_id = %s AND resource_id = 5", (type_id,))
                can_edit = cursor.fetchone()
                if can_edit and can_edit[0]:
                    cursor.execute("DELETE FROM reminders WHERE user_id = %s AND reminder_id = %s", (user_id, reminder_id))
                    db_connection.commit()
                    if cursor.rowcount > 0:
                        self.set_Response(200, {'message': 'reminder deleted successfully'})
                    else:
                        self.set_Response(404, {'message': 'reminder not found'})
                else:
                    self.set_Response(403, {'message': 'no edit permission'})
    
    
    def delete_user(self, user_id):
            
        email = self.verify_user()
        if email:
            cursor.execute("SELECT type_id FROM users WHERE email = %s", (email,))
            user_type = cursor.fetchone()
            if user_type:
                type_id = user_type[0]
                cursor.execute("SELECT can_edit FROM permissions WHERE type_id = %s AND resource_id = 1", (type_id,))
                can_edit = cursor.fetchone()
                if can_edit and can_edit[0]:
                    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                    db_connection.commit()
                    if cursor.rowcount > 0:
                        self.set_Response(200, {'message': 'user deleted successfully'})
                    else:
                        self.set_Response(404, {'message': 'user not found'})
                else:
                    self.set_Response(403, {'message': 'no edit permission'})
    

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