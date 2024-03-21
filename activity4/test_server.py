import unittest
import http.server
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler
import http.client
import json
import threading

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_address = ('localhost', 8000)
        cls.server = HTTPServer(cls.server_address, SimpleHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()
        
    def test_get_request(self):
        # Connect to the server and send a GET request
        connection = http.client.HTTPConnection(*self.server_address)
        connection.request('GET', '/')
        response = connection.getresponse()

        # Read and Decode the response
        data = response.read().decode()
        connection.close()

        #check That the response as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-Type'), 'application/json')

        # Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data, {'message': 'This is a GET request response'})
    
    def test_post_method(self):
        connection = http.client.HTTPConnection(*self.server_address)
        headers = {'Content-type': 'application/json'}
        data = json.dumps({'key': 'value'})
        connection.request('POST', '/', data, headers)
        response = connection.getresponse()
        
        #Read and Decode the response
        data = response.read().decode()
        connection.close()
        
        #Check that the response as expected
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        self.assertEqual(response.getheader('Content-type'), 'application/json')
        
        #Parse the JSON data and verify the content
        response_data = json.loads(data)
        self.assertEqual(response_data, {'received': {'key': 'value'}})

if __name__ == '__main__':
    unittest.main()