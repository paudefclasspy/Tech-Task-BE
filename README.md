# Loan Calculator

A Django-based web application for managing and calculating loan invoices with a modern Bootstrap UI.

## 🚀 Features

- User authentication and registration system
- Interactive dashboard with real-time calculations
- Multi-currency support
- Visual data representation using Chart.js
- RESTful API with Django REST Framework
- Responsive Bootstrap 5 UI
- Comprehensive test suite

## 🛠️ Tech Stack

- Python 3.9+
- Django 4.2.7
- Django REST Framework 3.14.0
- Bootstrap 5.1.3
- Chart.js
- SQLite (Development) / PostgreSQL (Production)
- pytest for testing

## 🔧 Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/loan-calculator.git
cd loan-calculator
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up the database:
```
python manage.py migrate
```

5. Create a superuser:
```
python manage.py createsuperuser
```

6. Run the development server:
```
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 🗂️ Project Structure

```
loan_calculator/
├── manage.py
├── requirements.txt
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    ├── accounts/
    │   ├── forms.py
    │   ├── views.py
    │   └── urls.py
    └── invoices/
        ├── models.py
        ├── services.py
        ├── views.py
        └── templates/
```

## 🧪 Running Tests

The project uses pytest for testing. To run the test suite:

```
pytest
```

For more verbose output:
```
pytest -v
```

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

## 🚀 Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Update `ALLOWED_HOSTS`
3. Use a production-grade database (PostgreSQL recommended)
4. Configure static files serving
5. Set up proper security measures

## 📝 API Documentation

The API endpoints are available at:

- `/` - Dashboard
- `/invoices` - Invoices
