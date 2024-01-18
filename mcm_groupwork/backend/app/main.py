"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd
from typing import Optional, List
from .mymodules import formatting, utilities, filtered

app = FastAPI()

# Load data from .csv files
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
# Filter by 7 variables below (True or False)
def read_item(
    comune: str,
    piscina: Optional[bool] = Query(None),
    accesso_disabili: Optional[bool] = Query(None),
    fitness: Optional[bool] = Query(None),
    sauna: Optional[bool] = Query(None),
    aria_condizionata: Optional[bool] = Query(None),
    lago: Optional[bool] = Query(None)
):
    """
    Retrieve accommodation and museum information based on specified filters.

    Args:
        comune (str): The municipality for which to retrieve information.
        piscina (Optional[bool]): Filter by swimming pool availability.
        accesso_disabili (Optional[bool]): Filter by disabled access.
        fitness (Optional[bool]): Filter by fitness facilities availability.
        sauna (Optional[bool]): Filter by sauna availability.
        aria_condizionata (Optional[bool]): Filter by air conditioning.
        lago (Optional[bool]): Filter by lake availability.

    Returns:
        dict: Accommodation and museum information based on specified filters.
    """
    comune = utilities.normalize_string(comune)
    results = df[df['COMUNE'] == comune]
    results = filtered.apply_filters(results, piscina, accesso_disabili, fitness, sauna, aria_condizionata, lago)
    results_musei = df_musei[df_musei['Comune'] == comune]
    denominazione_musei = results_musei['Nome'].tolist()

    if denominazione_musei or results['DENOMINAZIONE'].tolist():
        return {"comune": comune, "risultati": formatting.format_results(results), "musei_consigliati": denominazione_musei}
    else:
        return {"error": "Alloggio non trovato"}
