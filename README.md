String Analyzer Service (Django REST Framework)


This is a Django REST Framework-based API for analyzing strings, computing various properties, and filtering stored results.


## Features
- **POST /strings/** — Analyze and store a string
- **GET /strings/{value}/** — Retrieve details for a specific string
- **GET /strings/** — List strings with optional filters
- **GET /strings/filter-by-natural-language/** — Filter using human-readable queries
- **DELETE /strings/{value}/** — Delete an analyzed string


## Setup Instructions
```bash
git clone <repo-url>
cd string_analyzer_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver