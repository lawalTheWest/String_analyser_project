from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import AnalyzedString
from .serializers import AnalyzedStringSerializer
from .utils import compute_properties, parse_nl_query
from hashlib import sha256


class ListCreateStringView(generics.ListCreateAPIView):
    """Handles GET / POST on /api/strings

    - GET: list with filters
    - POST: create/analyze a string
    """
    serializer_class = AnalyzedStringSerializer

    def get_queryset(self):
        qs = AnalyzedString.objects.all()
        params = self.request.query_params
        is_palindrome = params.get('is_palindrome')
        min_length = params.get('min_length')
        max_length = params.get('max_length')
        word_count = params.get('word_count')
        contains_char = params.get('contains_character')

        if is_palindrome is not None:
            qs = qs.filter(is_palindrome=is_palindrome.lower() == 'true')
        if min_length:
            qs = qs.filter(length__gte=int(min_length))
        if max_length:
            qs = qs.filter(length__lte=int(max_length))
        if word_count:
            qs = qs.filter(word_count=int(word_count))
        if contains_char:
            qs = qs.filter(value__icontains=contains_char)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = AnalyzedStringSerializer(queryset, many=True).data
        filters_applied = dict(request.query_params)
        return Response({'data': data, 'count': len(data), 'filters_applied': filters_applied})

    def post(self, request, *args, **kwargs):
        value = request.data.get('value')
        if value is None:
            return Response({'error': 'Missing value'}, status=400)
        if not isinstance(value, str):
            return Response({'error': 'Invalid type for value'}, status=422)
        props = compute_properties(value)
        if AnalyzedString.objects.filter(id=props['sha256_hash']).exists():
            return Response({'error': 'String already exists'}, status=409)
        record = AnalyzedString.objects.create(
            id=props['sha256_hash'],
            value=value,
            created_at=timezone.now(),
            **props
        )
        return Response(AnalyzedStringSerializer(record).data, status=201)


class RetrieveDeleteStringView(APIView):
    """Handles GET and DELETE on /api/strings/<string_value>"""

    def get(self, request, string_value):
        hash_ = sha256(string_value.encode()).hexdigest()
        record = get_object_or_404(AnalyzedString, id=hash_)
        return Response(AnalyzedStringSerializer(record).data)

    def delete(self, request, string_value):
        hash_ = sha256(string_value.encode()).hexdigest()
        record = AnalyzedString.objects.filter(id=hash_).first()
        if not record:
            return Response({'error': 'Not found'}, status=404)
        record.delete()
        return Response(status=204)


class NaturalLanguageFilterView(APIView):
    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({'error': 'Missing query'}, status=400)
        try:
            parsed = parse_nl_query(query)
        except ValueError as e:
            return Response({'error': str(e)}, status=400)
        qs = AnalyzedString.objects.all()
        if parsed.get('is_palindrome'):
            qs = qs.filter(is_palindrome=True)
        if parsed.get('word_count'):
            qs = qs.filter(word_count=parsed['word_count'])
        if parsed.get('min_length'):
            qs = qs.filter(length__gte=parsed['min_length'])
        if parsed.get('contains_character'):
            qs = qs.filter(value__icontains=parsed['contains_character'])


        data = AnalyzedStringSerializer(qs, many=True).data
        return Response({
            'data': data,
            'count': len(data),
            'interpreted_query': {
                'original': query,
                'parsed_filters': parsed
            }
        })
