from django.test import TestCase
from rest_framework.test import APIClient
from hashlib import sha256
from string_analyser.models import AnalyzedString


class StringAnalyzerTests(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_create_and_retrieve(self):
        resp = self.client.post('/api/strings', {'value': 'racecar'}, format='json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertTrue(data['is_palindrome'])
        get_resp = self.client.get(f"/api/strings/racecar")
        self.assertEqual(get_resp.status_code, 200)


    def test_filter_and_delete(self):
        self.client.post('/api/strings', {'value': 'hello world'}, format='json')
        resp = self.client.get('/api/strings?min_length=5')
        self.assertEqual(resp.status_code, 200)
        del_resp = self.client.delete('/api/strings/hello world')
        self.assertEqual(del_resp.status_code, 204)