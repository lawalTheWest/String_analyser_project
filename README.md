# String Analyzer Service - Backend Stage 1

A RESTful API service that analyzes strings and stores their computed properties. Built with Django REST Framework.

## Features

- **String Analysis**: Automatically computes length, palindrome status, unique characters, word count, SHA-256 hash, and character frequency
- **CRUD Operations**: Create, read, and delete analyzed strings
- **Advanced Filtering**: Filter by palindrome status, length, word count, and character presence
- **Natural Language Queries**: Filter strings using natural language (e.g., "single word palindromic strings")
- **Duplicate Prevention**: Returns 409 Conflict for duplicate strings
- **Production Ready**: Configured for deployment on Railway, Heroku, AWS, etc.

## Tech Stack

- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: PostgreSQL (production) / SQLite (development)
- **Server**: Gunicorn
- **Language**: Python 3.9+

## Project Structure



## Local Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd string-analyzer-service
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Variables
### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

Server will start at `http://localhost:8000`

### Step 8: Run Tests

```bash
python manage.py test string_analyzer
```

## API Endpoints

### 1. Create/Analyze String

**Endpoint**: `POST /strings`

**Request Body**:
```json
{
  "value": "racecar"
}
```

**Success Response (201 Created)**:
```json
{
  "id": "58d2c9c8e...",
  "value": "racecar",
  "properties": {
    "length": 7,
    "is_palindrome": true,
    "unique_characters": 4,
    "word_count": 1,
    "sha256_hash": "58d2c9c8e...",
    "character_frequency_map": {
      "r": 2,
      "a": 2,
      "c": 2,
      "e": 1
    }
  },
  "created_at": "2025-10-24T10:00:00Z"
}
```

**Error Responses**:
- `409 Conflict`: String already exists
- `400 Bad Request`: Missing 'value' field
- `422 Unprocessable Entity`: Invalid data type

### 2. Get Specific String

**Endpoint**: `GET /strings/{string_value}`

**Example**: `GET /strings/racecar`

**Success Response (200 OK)**:
```json
{
  "id": "58d2c9c8e...",
  "value": "racecar",
  "properties": { ... },
  "created_at": "2025-10-24T10:00:00Z"
}
```

**Error Response**:
- `404 Not Found`: String does not exist

### 3. Get All Strings with Filtering

**Endpoint**: `GET /strings`

**Query Parameters**:
- `is_palindrome` (boolean): true/false
- `min_length` (integer): Minimum string length
- `max_length` (integer): Maximum string length
- `word_count` (integer): Exact word count
- `contains_character` (string): Single character to search

**Examples**:
```bash
GET /strings?is_palindrome=true
GET /strings?min_length=5&max_length=20
GET /strings?word_count=2&contains_character=a
```

**Success Response (200 OK)**:
```json
{
  "data": [
    {
      "id": "hash1",
      "value": "racecar",
      "properties": { ... },
      "created_at": "2025-10-24T10:00:00Z"
    }
  ],
  "count": 1,
  "filters_applied": {
    "is_palindrome": true
  }
}
```

### 4. Natural Language Filtering

**Endpoint**: `GET /strings/filter-by-natural-language`

**Query Parameter**: `query` (string)

**Examples**:
```bash
GET /strings/filter-by-natural-language?query=single word palindromic strings
GET /strings/filter-by-natural-language?query=strings longer than 10 characters
GET /strings/filter-by-natural-language?query=strings containing the letter z
```

**Success Response (200 OK)**:
```json
{
  "data": [ ... ],
  "count": 3,
  "interpreted_query": {
    "original": "single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}
```

**Supported Natural Language Patterns**:
- "single word palindromic strings"
- "strings longer than 10 characters"
- "palindromic strings that contain the first vowel"
- "strings containing the letter z"
- "two word strings"
- "strings with at least 5 characters"


## License

## Author

[Lawal Tajudeen Ogunsola]  
[lwltjdn@gmail.com] 

