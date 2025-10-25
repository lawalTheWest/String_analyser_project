from django.db import models


class AnalyzedString(models.Model):
    id = models.CharField(primary_key=True, max_length=64) # sha256 hash
    value = models.TextField(unique=True)
    length = models.PositiveIntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.PositiveIntegerField()
    word_count = models.PositiveIntegerField()
    sha256_hash = models.CharField(max_length=64)
    character_frequency_map = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.value