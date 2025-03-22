import unittest
import json
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_api(self):
        data = {'api_url': 'http://test-api.com', 'interval': 60}
        response = self.app.post('/api/apis', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {'message': 'API added for monitoring'})

    def test_get_versioned_data_success(self):
        response = self.app.get('/api/version/http://test-api.com/2.0.0')
        self.assertEqual(response.status_code, 404) # since the API is mock and does not exist.

    def test_get_versioned_data_not_found(self):
        response = self.app.get('/api/version/http://test-api.com/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
