from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
import bcrypt 
import json
import jwt
import mysql.connector
import os 

load_dotenv('./.env')

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



class RequestHandler(BaseHTTPRequestHandler):
    
    # Set the HTTP response status and header
    def set_Response(self, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', "application/json")
        self.end_headers()
     
    
    '''
        # HTTP REQUEST METHODS
        
        GET     /register               creates a new user
        GET     /healthcare             returns all healthcare providers
        GET     /healthcare/me          returns the user's healthcare provider
        
        GET     /health_records         returns all health rec
        GET     /health_records/:id     returns a specific health rec
        
        GET     /reminders              returns all reminders
        GET     /reminders/due          returns all due reminders
        GET     /reminders/:id          returns a specific reminder
        
        POST    /health_records         creates a new health rec
        POST    /reminders              creates a new reminder
        
        PUT     /health_records/:id     updates a specific health rec
        PUT     /reminders/:id           updates a specific reminder
        
        DELETE  /health_records/:id     deletes a specific health rec
        DELETE  /reminders/:id          deletes a specific reminder
        
    '''
    
    
    
    
    

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