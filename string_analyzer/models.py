from django.db import models
import hashlib
from django.utils import timezone

class AnalyzedString(models.Model):
    """documentation
    Model to store analyzed strings and their computed properties.
    Uses SHA256 hash of the string as the primary key for uniqueness.

    Args:
        models (Model): Django model base class.
    """
    #  primary key as SHA256 hash of the string
    id = models.CharField(primary_key=True, max_length=64, editable=False)
    value = models.TextField(unique=True)
    
    # Computed properties
    length = models.PositiveIntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.PositiveIntegerField()
    word_count = models.PositiveIntegerField()
    sha256_hash = models.CharField(max_length=64, unique=True)
    character_frequency_map = models.JSONField()
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'analyzed_strings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_palindrome']),
            models.Index(fields=['length']),
            models.Index(fields=['word_count']),
        ]
    
    def save(self, *args, **kwargs):
        """
        Compute all strings properties before saving.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.length = len(self.value)
        self.is_palindrome = self.check_palindrome()
        self.unnique_characters = len(set(self.value))
        self.word_count = len(self.value.split())
        self.sha256_hash = hashlib.sha256(self.value.encode('utf-8')).hexdigest()
        self.id = self.sha256_hash
        self.character_frequency_map = self._compute_frequency_map()
        
    def _check_palindrome(self):
        """
        Check if the string is a palindrome, ignoring case and spaces.
        Args:
            None
        """
        cleaned = ''.join(self.value.lower().split())
        return cleaned == cleaned[::-1]
    
    def _computed_frequency_map(self):
        """
        Compute frequency map of characters in the string.
        Args:
            None
        """
        freq_map = {}
        for char in self.value:
            freq_map[char] = freq_map.get(char, 0) + 1
        return freq_map
    
    def __str__(self):
        """String representation of the analyzed string.
        Returns:
            str: Truncated string value for representation.
            args: None
        """
        return f"{self.value[:50]}..."