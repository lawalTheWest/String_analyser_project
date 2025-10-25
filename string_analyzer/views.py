import json
import hashlib

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


def _compute_analysis(value: str) -> dict:
	cleaned = ''.join(value.lower().split())
	is_palindrome = cleaned == cleaned[::-1]
	length = len(value)
	unique_characters = len(set(value))
	word_count = len(value.split()) if value.strip() != '' else 0
	sha256_hash = hashlib.sha256(value.encode('utf-8')).hexdigest()
	freq = {}
	for ch in value:
		freq[ch] = freq.get(ch, 0) + 1

	return {
		'value': value,
		'length': length,
		'is_palindrome': is_palindrome,
		'unique_characters': unique_characters,
		'word_count': word_count,
		'sha256_hash': sha256_hash,
		'character_frequency_map': freq,
	}


def index(request):
	return JsonResponse({'message': 'String Analyzer API'})


@csrf_exempt
@require_http_methods(['POST'])
def analyze_string(request):
	"""Accepts JSON {"value": "..."} and returns string analysis as JSON."""
	try:
		payload = json.loads(request.body.decode('utf-8'))
	except Exception:
		return HttpResponseBadRequest('Invalid JSON')

	if not isinstance(payload, dict) or 'value' not in payload:
		return HttpResponseBadRequest('JSON must contain a "value" field')

	value = payload.get('value') or ''
	analysis = _compute_analysis(value)

	return JsonResponse(analysis, status=201)
