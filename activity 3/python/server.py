from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
import mysql.connector
import json
import os 

load_dotenv('./.env')

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
    
    # Return all the notes from the database
    def do_GET(self):
        if self.path == '/notes':
            cursor.execute("SELECT * FROM Note")
            notes = cursor.fetchall()
            if len(notes) != 0:
                self.set_Response(200)
                self.wfile.write(json.dumps(notes).encode('utf-8'))
            else:
                self.set_Response(204)
                self.wfile.write("No Content".encode('utf-8'))
        else:
            self.set_Response(404)
            self.wfile.write("Not Found".encode('utf-8'))

    # Add a new note to the database
    def do_POST(self):
        content_len = int(self.headers['Content-Length'])
        data_rec = self.rfile.read(content_len)
        data = json.loads(data_rec.decode())
        title = data.get('title', '')
        content = data.get('content', '')
        if title and content:
            cursor.execute("INSERT INTO Note (title, content) VALUES (%s, %s)", (title, content))
            db_connection.commit()
            self.set_Response(201)
            self.wfile.write("Success: Note created".encode('utf-8'))
        else:
            self.set_Response(400)
            self.wfile.write("Bad Request: Title and Content required".encode('utf-8'))

    # Modify and update the note specified from the database
    def do_PUT(self):
        if self.path.startswith('/notes/'):
            note_id = int(self.path.split('/')[-1])
            content_len = int(self.headers['Content-Length'])
            data_rec = self.rfile.read(content_len)
            data = json.loads(data_rec.decode())
            title = data.get('title', '')
            content = data.get('content', '')
            if title and content:
                cursor.execute("UPDATE Note SET title=%s, content=%s WHERE id=%s", (title, content, note_id))
                db_connection.commit()
                self.set_Response(200)
                self.wfile.write("Success: Note updated".encode('utf-8'))
            else:
                self.set_Response(400)
                self.wfile.write("Bad Request: Title and Content are required".encode('utf-8'))
        else:
            self.set_Response(404)
            self.wfile.write("Not Found".encode('utf-8'))

    # Delete the note specified from the database
    def do_DELETE(self):
        if self.path.startswith('/notes/'):
            note_id = int(self.path.split('/')[-1])
            cursor.execute("DELETE FROM Note WHERE id=%s", (note_id,))
            db_connection.commit()
            self.set_Response(200)
            self.wfile.write("Success: Note deleted".encode('utf-8'))
        else:
            self.set_Response(404)
            self.wfile.write("Not Found".encode('utf-8'))

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