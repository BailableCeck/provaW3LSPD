"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd
from typing import Optional, List
from fastapi import Query

app = FastAPI()

df = pd.read_csv('/app/app/output.csv')
df_musei = pd.read_csv('/app/app/musei_veneto.csv')

@app.get('/')
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
    """
    return {"Funziona?": "World"}


@app.get('/query/{comune}')
#Filter by 7 variables below (True or False)
def read_item(
    comune: str,
    piscina: Optional[bool] = Query(None),
    accesso_disabili: Optional[bool] = Query(None),
    fitness: Optional[bool] = Query(None),
    sauna: Optional[bool] = Query(None),
    aria_condizionata: Optional[bool] = Query(None),
    animali_amessi: Optional[bool] = Query(None)
):
    comune = comune.upper()

    results = df[df['COMUNE'] == comune]

    if piscina is not None and piscina:
        results = results[results['PISCINA'] == 'Vero']

    if accesso_disabili is not None and accesso_disabili:
        results = results[results['ACCESSO AI DISABILI'] == 'Vero']

    if fitness is not None and fitness:
        results = results[results['FITNESS'] == 'Vero']

    if sauna is not None and sauna:
        results = results[results['SAUNA'] == 'Vero']

    if aria_condizionata is not None and aria_condizionata:
        results = results[results['ARIA CONDIZIONATA'] == 'Vero']

    if animali_amessi is not None and animali_amessi:
        results = results[results['ANIMALI AMMESSI'] == 'Vero']

    denominazione_alloggio = results['DENOMINAZIONE'].tolist()
    link_alloggio = results['SITO WEB'].tolist()

    results_musei = df_musei[df_musei['Comune'] == comune]
    denominazione_musei = results_musei['Nome'].tolist()

    result_list = []
    for nome, link in zip(denominazione_alloggio, link_alloggio):
        result_item = {"nome": nome}
        if pd.notna(link):
            result_item["link"] = link
        result_list.append(result_item)

    if denominazione_musei or denominazione_alloggio:
        return {"comune": comune, "risultati": result_list, "musei_consigliati": denominazione_musei}
    else:
        return {"error": "Alloggio non trovato"}

@app.get('/get-date')
def get_date():
    """
    Endpoint to get the current date.

    Returns:
        dict: Current date in ISO format.
    """
    current_date = datetime.now().isoformat()
    return JSONResponse(content={"date": current_date})
