from hashlib import sha256
from collections import Counter
import re
from warnings import filters


def compute_properties(value: str) -> dict:
    normalized = value.casefold()
    props = {
        'length': len(value),
        'is_palindrome': normalized == normalized[::-1],
        'unique_characters': len(set(value)),
        'word_count': len(value.split()) if value.strip() else 0,
        'sha256_hash': sha256(value.encode()).hexdigest(),
        'character_frequency_map': dict(Counter(value)),
    }
    return props


def parse_nl_query(query: str) -> dict:
    ql = query.lower()
    filters = {}
    if 'palind' in ql:
        filters['is_palindrome'] = True
    if 'single word' in ql or 'one word' in ql:
        filters['word_count'] = 1

    import re
    m = re.search(r'longer than (\d+)', ql)
    if m:
        filters['min_length'] = int(m.group(1)) + 1
    m2 = re.search(r'containing the letter (\w)', ql)
    if m2:
        filters['contains_character'] = m2.group(1)
    if not filters:
        raise ValueError('Unable to parse natural language query')
    return filters