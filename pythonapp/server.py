from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
import mysql.connector
import json
import os 

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