import os
import sys
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
import pandas as pd


# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now you can do the relative import

"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
 """

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_success_read_item():
    response = client.get("/query/Albert Einstein")
    assert response.status_code == 200
    assert response.json() == {"person_name": 'Albert Einstein', 
                               "birthday": '03/14/1879'}


""" def test_fail_read_item():
    response = client.get("/query/Pippo")
    assert response.status_code == 200
    assert response.json() == {"error": "Person not found"} """


# The following will generate an error in pycheck
""" def test_success_read_item_module():
    response = client.get("/module/search/Albert Einstein")
    assert response.status_code == 200
    assert response.json() == {"Albert Einstein's birthday is 03/14/1879."} """


# The following is correct, can you spot the diffence?
def test_success_read_item_module():
    response = client.get("/module/search/Albert Einstein")
    assert response.status_code == 200
    assert response.json() == ["Albert Einstein's birthday is 03/14/1879."]




def test_query_endpoint_success():
    comune = "Verona"
    response = client.get(f"/query/{comune}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["comune"] == comune
    assert "risultati" in data
    assert "musei_consigliati" in data

def test_query_endpoint_no_results():
    comune = "ComuneInesistente"
    response = client.get(f"/query/{comune}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["error"] == "Alloggio non trovato"
    assert "risultati" not in data
    assert "musei_consigliati" not in data

def test_query_endpoint_with_piscina():
    comune = "Verona"
    response = client.get(f"/query/{comune}?piscina=true")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["comune"] == comune
    assert "risultati" in data
    assert "musei_consigliati" in data

def test_query_endpoint_musei_only():
    comune = "Venezia"
    response = client.get(f"/query/{comune}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["comune"] == comune
    assert "risultati" not in data
    assert "musei_consigliati" in data