from rest_framework import serializers
from .models import AnalyzedString


class AnalyzedStringSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()

    class Meta:
        model = AnalyzedString
        # include top-level fields for backwards compatibility (tests expect them)
        # while also providing the nested `properties` object required by the spec
        fields = (
            'id', 'value', 'properties', 'length', 'is_palindrome',
            'unique_characters', 'word_count', 'sha256_hash',
            'character_frequency_map', 'created_at'
        )

    def get_properties(self, obj):
        return {
            'length': obj.length,
            'is_palindrome': obj.is_palindrome,
            'unique_characters': obj.unique_characters,
            'word_count': obj.word_count,
            'sha256_hash': obj.sha256_hash,
            'character_frequency_map': obj.character_frequency_map,
        }