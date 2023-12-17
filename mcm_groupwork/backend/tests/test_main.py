import os
import sys
from fastapi.testclient import TestClient
from fastapi import status
import pandas as pd


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
    """
    Test the root endpoint ("/") to ensure it returns the expected response.

    Returns:
        None
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Funziona?": "World"}


""" def test_fail_read_item():
    response = client.get("/query/Pippo")
    assert response.status_code == 200
    assert response.json() == {"error": "Person not found"} """


# The following will generate an error in pycheck
""" def test_success_read_item_module():
    response = client.get("/module/search/Albert Einstein")
    assert response.status_code == 200
    assert response.json() == {"Albert Einstein's birthday is 03/14/1879."} """


# Defining 4 tests
def test_query_endpoint_success():
    """
    Test the query endpoint with valid parameters to ensure it returns the expected response.

    Returns:
        None
    """
    comune = "Monfumo"
    response = client.get(f"/query/{comune}")
    assert response.json() == {"comune": 'MONFUMO', 'musei_consigliati':[], 
                               "risultati": [{'nome': 'DA GERRY LOCANDA', 'link': 'www.ristorantedagerry.com'}, {'nome': "AGRITURISMO GHISOLANA - DALL'EST LISA", 'link': 'www.agriturismoalcapitello.it'}, {'nome': 'CASA ROSA AGRITURISMO - GIRARDI GIUSEPPINA'}]}

def test_query_endpoint_no_results():
    """
    Test the query endpoint with a municipality that has no results, ensuring it returns the expected response.

    Returns:
        None
    """
    comune = "ComuneInesistente"
    response = client.get(f"/query/{comune}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["error"] == "Alloggio non trovato"
    assert "risultati" not in data
    assert "musei_consigliati" not in data

def test_query_endpoint_with_piscina():
    """
    Test the query endpoint with a municipality and piscina parameter, ensuring it returns the expected response.

    Returns:
        None
    """
    comune = "zero branco"
    response = client.get(f"/query/{comune}?piscina=true")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"comune": 'ZERO BRANCO', 'musei_consigliati':[],
                               "risultati": [{'nome': 'GIUSTO ELISA - B&B SOLOQUI', 'link': 'www.soloqui.com'}]}

def test_query_endpoint_musei_only():
    """
    Test the query endpoint with a municipality and piscina parameter, ensuring it returns the expected response.

    Returns:
        None
    """
    comune = "nove"
    response = client.get(f"/query/{comune}?piscina=true")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"comune": 'NOVE', 'musei_consigliati':['Museo della Ceramica'],"risultati":[]}