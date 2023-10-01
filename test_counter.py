"""TestCase for counter app"""

from unittest import TestCase
from app.server import app
from app.statuscodes import STATUS_CODE_OK, STATUS_CODE_CREATED, \
STATUS_CODE_NOT_FOUND, STATUS_CODE_DUPLICATE
#from unittest.mock import patch
import json

class TestCounterApp(TestCase):
    """Testing counter flask app"""
    @classmethod
    def setUpClass(cls):
        """Initialize state"""
        cls.client = app.test_client()

    
    def test_create_counter(self):
        """Test create a counter"""
        res = self.client.post('/counters/foo')
        counter = json.loads(res.data.decode())
        self.assertEqual(counter['data']['foo'], 0)
        self.assertEqual(res.status_code, STATUS_CODE_CREATED)

    def test_get_counter(self):
        "Test get a counter"
        res = self.client.post('/counters/bar')
        counter = json.loads(res.data.decode())
        self.assertEqual(counter['data']['bar'], 0)
        self.assertEqual(res.status_code, STATUS_CODE_CREATED)
        res = self.client.get('/counters/bar')
        counter = json.loads(res.data.decode())
        self.assertIn('bar', counter['data'])
        self.assertEqual(res.status_code, STATUS_CODE_OK)
    
    def test_create_duplicate_counter(self):
        """Test duplicate counters"""
        res = self.client.post('/counters/lorem')
        counter = json.loads(res.data.decode())
        self.assertEqual(counter['data']['lorem'], 0)
        self.assertEqual(res.status_code, STATUS_CODE_CREATED)
        res = self.client.post('/counters/lorem')
        counter = json.loads(res.data.decode())
        self.assertEqual(res.status_code, STATUS_CODE_DUPLICATE)
    
    def test_get_nonexistent_counter(self):
        """Test non-existent counter """
        res = self.client.get('/counters/dolo')
        self.assertEqual(res.status_code, STATUS_CODE_NOT_FOUND)

    def test_increment_counter(self):
        "Test increment a counter"
        res = self.client.post('/counters/score')
        counter = json.loads(res.data.decode())
        score = counter['data']['score']
        self.assertEqual(score, 0)
        self.assertEqual(res.status_code, STATUS_CODE_CREATED)
        res = self.client.put("/counters/score/increment")
        data = json.loads(res.data.decode())
        updated_score = data['data']['score']
        self.assertEqual(updated_score, score + 1)

    def test_empty_name(self):
        """Test empty name"""
        res = self.client.post('/counters/')
        self.assertEqual(res.status_code, STATUS_CODE_NOT_FOUND)
