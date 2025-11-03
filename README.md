# AutoService Booking TDD

Testjuhitud arenduse harjutusprojekt autoremondi broneeringusüsteemi tuumfunktsionaalsustega.



## Tehnoloogia Stack

- **Keel:** Python 3.11+
- **ORM:** SQLAlchemy 2.0
- **Test Framework:** pytest + pytest-cov
- **Mock Library:** unittest.mock
- **Andmebaas:** SQLite (dev) / PostgreSQL (production)
- **Migratsioonid:** Alembic
- **Dependency Management:** pip + requirements.txt

## Eeltingimused

- Python 3.11 või uuem
- pip (Python package manager)
- Git
- SQLite (tuleb Pythoniga kaasa)

## Projekti Seadistamine

### 1. Klooni Repositoorium

```bash
git clone https://github.com/sinu-kasutaja/autoservice-booking-tdd.git
cd autoservice-booking-tdd
```

### 2. Virtuaalne Keskkond

```bash
# Loo virtuaalne keskkond
python -m venv venv

# Aktiveeri (Linux/Mac)
source venv/bin/activate

# Aktiveeri (Windows)
venv\Scripts\activate
```

### 3. Installeeri Sõltuvused

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Keskkonna Konfiguratsioon

```bash
# Kopeeri näidisfail
cp .env.example .env

# Muuda .env failis väärtused vajaduse järgi
# DATABASE_URL=sqlite:///./autoservice.db
```

### 5. Andmebaasi Migratsioonid

```bash
# Käivita migratsioonid
alembic upgrade head

# Kontrolli staatust
alembic current
```

## Testide Käivitamine

### Kõik Testid

```bash
# Käivita kõik testid
pytest

# Verbose režiim
pytest -v

# Peata esimese vea juures
pytest -x
```

### Katvuse Raport

```bash
# Käivita testid katvusega
pytest --cov=src --cov-report=html --cov-report=term

# Vaata HTML raportit
# Ava: htmlcov/index.html
```

### Üksikud Testifailid

```bash
# Ainult broneeringu valideerimise testid
pytest tests/unit/test_booking_validation.py

# Ainult varuosa testid
pytest tests/unit/test_spare_part_availability.py

# Ainult broneeringu tühistamise testid
pytest tests/unit/test_booking_cancellation.py
```

## Projekti Struktuur

```
autoservice-booking-tdd/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py              # SQLAlchemy Base
│   │   ├── booking.py           # Broneeringu mudel
│   │   └── spare_part.py        # Varuosa mudel
│   ├── services/
│   │   ├── __init__.py
│   │   ├── booking_service.py   # Broneeringu äriloogika
│   │   └── spare_part_service.py # Varuosa äriloogika
│   ├── utils/
│   │   ├── __init__.py
│   │   └── datetime_provider.py # Aja mock'imiseks
│   └── database.py              # DB session haldus
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

## Funktsionaalsused

### 1. Broneeringu Aja Valideerimine

**Domeenireegel:** Broneeringu aeg peab olema tööajal (E-R 8:00-17:00) ja vähemalt 24 tundi tulevikus.

**Testid:**
- ✅ `test_should_allow_booking_tomorrow_at_10am` - lubab broneerida homme kell 10:00
- ✅ `test_should_not_allow_booking_today` - ei luba broneerida täna
- ✅ `test_should_not_allow_booking_on_weekend` - ei luba broneerida nädalavahetusel
- ✅ `test_should_not_allow_booking_outside_working_hours` - ei luba broneerida väljaspool tööaega

**Mudel:** `Booking` (id, customer_email, service_type, booking_datetime, status, created_at)

**Testifail:** `tests/unit/test_booking_validation.py`

**Implementatsioon:** `src/services/booking_service.py` - `validate_booking_time()` meetod

---

### 2. Varuosa Saadavuse Kontroll

**Domeenireegel:** Varuosa on 'saadaval' ainult kui laos kogus > 0 JA hind on määratud (ei ole NULL).

**Testid:**
- ✅ `test_should_return_available_when_in_stock_and_priced` - tagastab 'saadaval'
- ✅ `test_should_return_out_of_stock_when_quantity_zero` - tagastab 'otsas' kui laos=0
- ✅ `test_should_return_price_undefined_when_price_null` - tagastab 'määramata' kui hind puudub
- ✅ `test_should_return_out_of_stock_when_negative_quantity` - ei luba negatiivset kogust

**Mudel:** `SparePart` (id, name, part_number, quantity, price, created_at)

**Testifail:** `tests/unit/test_spare_part_availability.py`

**Implementatsioon:** `src/services/spare_part_service.py` - `check_availability()` meetod

---

### 3. Broneeringu Tühistamine

**Domeenireegel:** Broneeringu saab tühistada ainult:
- Rohkem kui 2 tundi enne broneeringu algust
- Kui broneering on staatuses 'CONFIRMED'

**Testid:**
- ✅ `test_should_allow_cancellation_3_hours_before` - lubab tühistada 3h enne
- ✅ `test_should_not_allow_cancellation_1_hour_before` - ei luba tühistada 1h enne
- ✅ `test_should_not_allow_cancellation_of_cancelled_booking` - ei luba tühistada juba tühistatud
- ✅ `test_should_not_allow_cancellation_of_completed_booking` - ei luba tühistada lõpetatud broneeringut

**Mudel:** `Booking` (status: PENDING, CONFIRMED, CANCELLED, COMPLETED)

**Testifail:** `tests/unit/test_booking_cancellation.py`

**Implementatsioon:** `src/services/booking_service.py` - `cancel_booking()` meetod

---

## ORM Parimad Praktikad

### Rakendatud Praktikad

1. **Korrektsed Seosed**
   - Foreign Key piirangud
   - Cascade valikud läbimõeldud
   - Index'id jõudlusele

2. **Andmebaasi Piirangud**
   ```python
   # Näide: Booking mudel
   customer_email = Column(String(255), nullable=False)
   booking_datetime = Column(DateTime, nullable=False)
   status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.PENDING)
   
   __table_args__ = (
       CheckConstraint('booking_datetime > created_at'),
       Index('idx_booking_datetime', 'booking_datetime'),
   )
   ```

3. **Migratsioonid**
   - Iga skeemi muudatus = eraldi migratsioon
   - Up ja Down operatsioonid
   - Käivitatavad nullist

4. **Transaktsioonid**
   ```python
   # Näide: Atomic operatsioon
   with session.begin():
       booking.status = BookingStatus.CONFIRMED
       spare_part.quantity -= 1
       session.commit()
   ```

### Migratsiooni Käsud

```bash
# Loo uus migratsioon
alembic revision --autogenerate -m "kirjeldus"

# Käivita migratsioonid
alembic upgrade head

# Tagasi võtmine
alembic downgrade -1

# Ajalugu
alembic history
```

## Mock'imise Strateegia

### Mockitakse

✅ **Datetime Provider** - kõik kellaaja päringud
```python
from unittest.mock import patch

@patch('src.utils.datetime_provider.DatetimeProvider.now')
def test_something(mock_now):
    mock_now.return_value = datetime(2025, 1, 15, 10, 0)
    # Test code...
```

✅ **Email Teenus** - broneeringu kinnitused
```python
@patch('src.services.email_service.EmailService.send')
def test_booking_confirmation(mock_email):
    mock_email.return_value = True
    # Test code...
```

✅ **UUID Generaator** - determineeritud ID-d
```python
@patch('uuid.uuid4')
def test_with_fixed_uuid(mock_uuid):
    mock_uuid.return_value = UUID('12345678-1234-5678-1234-567812345678')
    # Test code...
```

### EI Mockata

❌ **Domeeni loogika** - valideerimise reeglid  
❌ **Lihtsad arvutused** - viivise arvutamine  
❌ **Sisemised meetodid** - oma service'i meetodid  

## Git Töövoog (TDD Red-Green-Refactor)

### Feature Haru Loomine

```bash
git checkout -b feature/booking-time-validation
```

### RED Faas - Testid Kirjutatakse

```bash
# Kirjuta testid mis KUKUVAD LÄBI
# tests/unit/test_booking_validation.py

git add tests/unit/test_booking_validation.py
git commit -m "red: booking time must be within working hours and 24h ahead"
```

### GREEN Faas - Minimaalne Kood

```bash
# Kirjuta minimaalne kood testide läbimiseks
# src/services/booking_service.py

git add src/services/booking_service.py
git commit -m "green: implement booking time validation logic"
```

### REFACTOR Faas - Koodi Puhastamine

```bash
# Paranda koodi kvaliteeti
# - Ekstrakti meetodid
# - Nimede parandamine
# - Korduste eemaldamine

git add src/services/booking_service.py
git commit -m "refactor: extract time validation to separate method"
```

### Merge Main'i

```bash
git checkout main
git merge --no-ff feature/booking-time-validation
git push origin main

# ÄRA KUSTUTA feature haru!
```

## Testimise Parimad Praktikad

### AAA Muster (Arrange-Act-Assert)

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

### Kirjeldavad Nimed

```python
# ✅ HEA
def test_should_return_available_when_in_stock_and_priced()

# ❌ HALB
def test_spare_part()
def test_1()
```

### Isoleeritud Testid

```python
# Iga test peab olema iseseisev
# Kasuta pytest fixtures

@pytest.fixture
def clean_database():
    # Setup
    Base.metadata.create_all(engine)
    yield
    # Teardown
    Base.metadata.drop_all(engine)
```

## Kasulikud Käsud

```bash
# Arendusserveri käivitamine (kui tehakse API)
python -m src.main

# Formateerimine
black src/ tests/

# Linting
pylint src/

# Type checking
mypy src/

# Migratsioonide kontroll
alembic check

# Testide käivitamine watch režiimis
pytest-watch
```

## Levinud Probleemid ja Lahendused

### Probleem: Testid kukuvad läbi aja tõttu

```python
# ❌ HALB
def test_booking():
    now = datetime.now()  # Muutub iga kord!
    
# ✅ HEA
@patch('src.utils.datetime_provider.DatetimeProvider.now')
def test_booking(mock_now):
    mock_now.return_value = datetime(2025, 1, 15, 10, 0)
```

### Probleem: Migratsioonid ei tööta

```bash
# Kontrolli alembic.ini faili
# Kontrolli DATABASE_URL keskkonna muutujat
# Vaata alembic/env.py konfiguratsioon

alembic current  # Kontrolli praegust versiooni
alembic history  # Vaata ajalugu
```

### Probleem: Import vead testides

```python
# Kasuta absoluutseid importe
from src.models.booking import Booking  # ✅ HEA
from ..models.booking import Booking    # ❌ HALB

# Lisa PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

## Hindamiskriteeriumid (Kontroll)

- [x] **TDD Distsipliin:** Iga funktsionaalsuse kohta on red → green → refactor
- [ ] **Git Protsess:** Feature harud + merge commit'id + harusid ei kustutatud
- [x] **ORM:** Korrektsed seosed, võtmed, piirangud, migratsioonid töötavad
- [x] **Testid:** Katavad reeglid, kirjeldavad nimed, jooksevad rohelistena (27/27 ✅)
- [x] **Mock'id:** Välistest sõltuvustest eraldamine, kell kontroll all
- [x] **Dokumentatsioon:** README arusaadav, setup toimib

## Testide Katvus

```
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
src\__init__.py                          0      0   100%
src\database.py                         13      3    77%
src\models\__init__.py                   4      0   100%
src\models\base.py                       2      0   100%
src\models\booking.py                   20      1    95%
src\models\spare_part.py                14      1    93%
src\services\__init__.py                 3      0   100%
src\services\booking_service.py         48     14    71%
src\services\spare_part_service.py      37     15    59%
src\utils\__init__.py                    0      0   100%
src\utils\datetime_provider.py           5      1    80%
--------------------------------------------------------
TOTAL                                  146     35    76%
```

## Edasine Arendus

Kui soovid projekti laiendada:

1. Lisa SMS meeldetuletused (mock SMS gateway)
2. Lisa teenuse hindamine (rating system)
3. Lisa teenuste kataloog koos hindadega
4. Lisa kasutaja autentimine (optional)
5. Lisa REST API endpoint'id (Flask/FastAPI)

## Viited

- [SQLAlchemy 2.0 Dokumentatsioon](https://docs.sqlalchemy.org/)
- [Pytest Dokumentatsioon](https://docs.pytest.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

## Litsents

See on õppeprojekt. Vaba kasutamiseks ja modifitseerimiseks.

## Autor

[Sinu Nimi] - TAK24 testjuhitud arenduse harjutus

---

**Märkus:** See projekt demonstreerib TDD metoodikat. Fookus on protsessil (red-green-refactor) ja kvaliteedil, mitte täisfunktsionaalsel rakendusel.

