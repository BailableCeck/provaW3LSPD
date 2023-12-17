import os
import sys
from fastapi.testclient import TestClient
from datetime import datetime

# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now you can do the relative import
from app.main import app


"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
 """

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Funziona?": "World"}

"""
def test_success_read_item():
    response = client.get("/query/Albert Einstein")
    assert response.status_code == 200
    assert response.json() == {"person_name": 'Albert Einstein', 
                               "birthday": '03/14/1879'}
"""


def test_fail_read_item():
    response = client.get("/query/MONFMO")
    assert response.status_code == 200
    assert response.json() == {"error": "Alloggio non trovato"}

# The following will generate an error in pycheck
"""def test_success_read_item_module():
    response = client.get("/module/search/Albert Einstein")
    assert response.status_code == 200
    assert response.json() == {"Albert Einstein's birthday is 03/14/1879."}"""

"""
# The following is correct, can you spot the diffence?
def test_success_read_item_module_wow():
    response = client.get("/module/search/Albert Einstein")
    assert response.status_code == 200
    assert response.json() == ["Albert Einstein's birthday is 03/14/1879."]
"""
def test_success_read_item_csv():
    response = client.get("/query/MONFUMO")
    assert response.status_code == 200
    assert response.json() == {"comune": 'MONFUMO', 
                               "denominazione_alloggio": ['DA GERRY LOCANDA', 'AGRITURISMO GHISOLANA - DALL\'EST LISA', 'CASA ROSA AGRITURISMO - GIRARDI GIUSEPPINA']}

def test_get_date():
    response = client.get("/get-date")
    assert response.status_code == 200
    
    # Estrai la data attuale
    expected_date = datetime.now().isoformat()
    
    # Estrai la data dalla risposta JSON
    actual_date = response.json()["date"]
    
    # Verifica che la data attesa e quella effettiva siano simili
    assert expected_date[:10] == actual_date[:10]  # Confronta solo la parte della data, non l'orario