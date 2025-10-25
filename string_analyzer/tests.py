from django.test import TestCase, Client, override_settings
import hashlib
import json


@override_settings(SECRET_KEY='test-secret-key')
class StringAnalyzerAPITests(TestCase):
	def setUp(self):
		self.client = Client()

	def test_index_endpoint(self):
		resp = self.client.get('/')
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertIn('message', data)

	def test_analyze_basic_racecar(self):
		value = 'racecar'
		resp = self.client.post(
			'/analyze/',
			data=json.dumps({'value': value}),
			content_type='application/json',
		)
		self.assertEqual(resp.status_code, 201)
		data = resp.json()

		self.assertEqual(data['length'], len(value))
		self.assertTrue(data['is_palindrome'])
		self.assertEqual(data['unique_characters'], len(set(value)))
		self.assertEqual(data['word_count'], 1)
		expected_hash = hashlib.sha256(value.encode('utf-8')).hexdigest()
		self.assertEqual(data['sha256_hash'], expected_hash)
		freq = {c: value.count(c) for c in value}
		self.assertEqual(data['character_frequency_map'], freq)

	def test_analyze_phrase_palindrome(self):
		value = 'A man a plan a canal Panama'
		resp = self.client.post(
			'/analyze/',
			data=json.dumps({'value': value}),
			content_type='application/json',
		)
		self.assertEqual(resp.status_code, 201)
		data = resp.json()

		self.assertTrue(data['is_palindrome'])
		self.assertEqual(data['word_count'], len(value.split()))

	def test_analyze_empty_string(self):
		value = ''
		resp = self.client.post(
			'/analyze/',
			data=json.dumps({'value': value}),
			content_type='application/json',
		)
		self.assertEqual(resp.status_code, 201)
		data = resp.json()

		self.assertEqual(data['length'], 0)
		self.assertTrue(data['is_palindrome'])
		self.assertEqual(data['word_count'], 0)
		self.assertEqual(data['unique_characters'], 0)
		self.assertEqual(data['character_frequency_map'], {})
