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
    comune = "Monfumo"
    response = client.get(f"/query/{comune}")
    assert response.json() == {"comune": 'MONFUMO', 'musei_consigliati':[], 
                               "risultati": [{'indirizzo': 'Via Chiesa', 'nome': 'DA GERRY LOCANDA', 'link': 'www.ristorantedagerry.com', 'telefono': '0423545082'}, {'indirizzo': 'Via Sassetti, 5','nome': "AGRITURISMO GHISOLANA - DALL'EST LISA", 'telefono': '0423545167 - 3460035183', 'link': 'www.agriturismoalcapitello.it'}, {'indirizzo': 'Via Collibert', 'nome': 'CASA ROSA AGRITURISMO - GIRARDI GIUSEPPINA', 'telefono': '0423543393 - 3387647667'}]}

def test_query_endpoint_no_results():
    comune = "ComuneInesistente"
    response = client.get(f"/query/{comune}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["error"] == "Alloggio non trovato"
    assert "risultati" not in data
    assert "musei_consigliati" not in data

def test_query_endpoint_with_piscina():
    comune = "zero branco"
    response = client.get(f"/query/{comune}?piscina=true")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"comune": 'ZERO BRANCO', 'musei_consigliati':[],
                               "risultati": [{'indirizzo': 'Via Fontane', 'nome': 'GIUSTO ELISA - B&B SOLOQUI', 'link': 'www.soloqui.com', 'telefono': '3473864299'}]}

def test_query_endpoint_with_sauna_no_link():
    comune = "vicenza"
    response = client.get(f"/query/{comune}?piscina=False&accesso_disabili=False&fitness=False&sauna=True&aria_condizionata=False&animali_ammessi=False")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"comune": 'VICENZA', 'musei_consigliati':['Basilica Palladiana', 'Gallerie di palazzo Leoni Montanari', 'Museo Civico', 'Museo del Risorgimento e della Resistenza', 'Museo diocesano', 'Museo Naturalistico Archeologico'],
                               "risultati": [{'nome': 'HOTEL VERDI', 'indirizzo': 'VIA LANZA', 'telefono': '0444965929'}]}

def test_query_endpoint_with_all_but_sauna():
    comune = "jesolo"
    response = client.get(f"/query/{comune}?piscina=True&accesso_disabili=True&fitness=True&sauna=False&aria_condizionata=True&animali_ammessi=True")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"comune": 'JESOLO', 'musei_consigliati':[],
                               "risultati": [{'nome': 'CASA BIANCA AL MARE', 'link': 'www.thegiannettihotelsgroup.com', 'indirizzo': 'PIAZZETTA CASA BIANCA', 'telefono': '0421.370615/16'}, {'nome': 'SPORTING (DIPENDENZA BAUER)', 'link': 'www.hotelbauer.it', 'indirizzo': 'Viale Orientale', 'telefono': '0421961363'}]}

def test_query_endpoint_musei_only():
    comune = "nove"
    response = client.get(f"/query/{comune}?piscina=true")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"comune": 'NOVE', 'musei_consigliati':['Museo della Ceramica'],"risultati":[]}