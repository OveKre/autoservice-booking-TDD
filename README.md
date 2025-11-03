# AutoService Booking TDD

A Test-Driven Development (TDD) learning project demonstrating core functionality of an auto repair booking system.

**NOTE:** This is an educational project for demonstrating TDD methodology. Features are selected from the auto repair domain.

## Technology Stack

- **Language:** Python 3.11+
- **ORM:** SQLAlchemy 2.0
- **Test Framework:** pytest + pytest-cov
- **Mock Library:** unittest.mock
- **Database:** SQLite (dev) / PostgreSQL (production)
- **Migrations:** Alembic
- **Dependency Management:** pip + requirements.txt

## Prerequisites

- Python 3.11 or newer
- pip (Python package manager)
- Git
- SQLite (comes with Python)

## Project Setup

### 1. Clone Repository

```bash
git clone https://github.com/OveKre/autoservice-booking-TDD.git
cd autoservice-booking-TDD
```

### 2. Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Environment Configuration

```bash
# Copy example file
cp .env.example .env

# Edit .env file with your values if needed
# DATABASE_URL=sqlite:///./autoservice.db
```

### 5. Database Migrations

```bash
# Run migrations
alembic upgrade head

# Check status
alembic current
```

## Running Tests

### All Tests

```bash
# Run all tests
pytest

# Verbose mode
pytest -v

# Stop at first failure
pytest -x
```

### Coverage Report

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term

# View HTML report
# Open: htmlcov/index.html
```

### Individual Test Files

```bash
# Only booking validation tests
pytest tests/unit/test_booking_validation.py

# Only spare part tests
pytest tests/unit/test_spare_part_availability.py

# Only booking cancellation tests
pytest tests/unit/test_booking_cancellation.py
```

## Project Structure

```
autoservice-booking-tdd/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py              # SQLAlchemy Base
│   │   ├── booking.py           # Booking model
│   │   └── spare_part.py        # Spare part model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── booking_service.py   # Booking business logic
│   │   └── spare_part_service.py # Spare part business logic
│   ├── utils/
│   │   ├── __init__.py
│   │   └── datetime_provider.py # Time mocking utility
│   └── database.py              # DB session management
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   └── unit/
│       ├── __init__.py
│       ├── test_booking_validation.py
│       ├── test_spare_part_availability.py
│       └── test_booking_cancellation.py
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
├── requirements-dev.txt
└── README.md
```
## Features

### 1. Booking Time Validation

**Domain Rule:** Booking time must be within working hours (Mon-Fri 8:00-17:00) and at least 24 hours in the future.

**Tests:** 11 tests covering all validation rules

**Model:** `Booking` (id, customer_email, service_type, booking_datetime, status, created_at)

**Test File:** `tests/unit/test_booking_validation.py`

**Implementation:** `src/services/booking_service.py` - `validate_booking_time()` method

### 2. Spare Part Availability Check

**Domain Rule:** Spare part is 'available' only if quantity > 0 AND price is defined (not NULL).

**Tests:** 8 tests covering all availability scenarios

**Model:** `SparePart` (id, name, part_number, quantity, price, created_at)

**Test File:** `tests/unit/test_spare_part_availability.py`

**Implementation:** `src/services/spare_part_service.py` - `check_availability()` method

### 3. Booking Cancellation

**Domain Rule:** Booking can be cancelled only if more than 2 hours before booking start time and status is 'CONFIRMED'.

**Tests:** 8 tests covering all cancellation scenarios

**Model:** `Booking` (status: PENDING, CONFIRMED, CANCELLED, COMPLETED)

**Test File:** `tests/unit/test_booking_cancellation.py`

**Implementation:** `src/services/booking_service.py` - `cancel_booking()` method

## Test Results

```
✅ Booking Validation Tests: 11/11 PASSED
✅ Spare Part Availability Tests: 8/8 PASSED
✅ Booking Cancellation Tests: 8/8 PASSED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ TOTAL: 27/27 PASSED (100%)
```

## Code Coverage

```
Overall Coverage: 76%
- Models: 95-100% coverage
- Services: 59-71% coverage
- Utils: 80% coverage
```

## Git Workflow (TDD Red-Green-Refactor)

### Create Feature Branch

```bash
git checkout -b feature/booking-time-validation
```

### RED Phase - Write Tests

```bash
git add tests/unit/test_booking_validation.py
git commit -m "red: booking time must be within working hours and 24h ahead"
```

### GREEN Phase - Minimal Code

```bash
git add src/services/booking_service.py
git commit -m "green: implement booking time validation logic"
```

### REFACTOR Phase - Code Cleanup

```bash
git add src/services/booking_service.py
git commit -m "refactor: extract time validation to separate method"
```

### Merge to Main

```bash
git checkout main
git merge --no-ff feature/booking-time-validation
git push origin main
```

## Testing Best Practices

### AAA Pattern (Arrange-Act-Assert)

```python
def test_should_allow_booking_tomorrow():
    # Arrange
    service = BookingService()
    tomorrow_10am = datetime.now() + timedelta(days=1, hours=10)

    # Act
    result = service.validate_booking_time(tomorrow_10am)

    # Assert
    assert result is True
```

### Mocking Strategy

✅ **Mock:** Datetime Provider, Email Service, External APIs
❌ **Don't Mock:** Domain Logic, Simple Calculations, Internal Methods

## Useful Commands

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=src --cov-report=html

# Format code
black src/ tests/

# Lint code
pylint src/

# Type checking
mypy src/

# Database migrations
alembic upgrade head
alembic downgrade -1
alembic history
```

## Common Issues and Solutions

### Issue: Tests fail due to time

```python
# ❌ BAD
def test_booking():
    now = datetime.now()  # Changes every time!

# ✅ GOOD
@patch('src.utils.datetime_provider.DatetimeProvider.now')
def test_booking(mock_now):
    mock_now.return_value = datetime(2025, 1, 15, 10, 0)
```

### Issue: Import errors in tests

```python
# Use absolute imports
from src.models.booking import Booking  # ✅ GOOD
from ..models.booking import Booking    # ❌ BAD
```

## References

- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

## License

This is an educational project. Free to use and modify.

## Author

[Your Name] - Test-Driven Development Exercise

---

**Note:** This project demonstrates TDD methodology. Focus is on process (red-green-refactor) and quality, not on a fully functional application.
