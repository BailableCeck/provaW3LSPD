"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd
from typing import Optional
from fastapi import Query
from typing import List




#from .mymodules.birthdays import return_birthday, print_birthdays_str

app = FastAPI()

# Dictionary of birthdays
#birthdays_dictionary = {
#    'Albert Einstein': '03/14/1879',
#    'Benjamin Franklin': '01/17/1706',
#    'Ada Lovelace': '12/10/1815',
#    'Donald Trump': '06/14/1946',
#    'Rowan Atkinson': '01/6/1955'
#}

df = pd.read_csv('/app/app/output.csv')
df_musei = pd.read_csv('/app/app/musei_veneto.csv')
"""
@app.get('/csv_show')
def read_and_return_csv():
    aux = df['Age'].values
    return{"Age": str(aux.argmin())}
"""
@app.get('/')
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
    """
    return {"Funziona?": "World"}


@app.get('/query/{comune}')
def read_item(comune: str, piscina: Optional[bool] = Query(None, description="Filter by piscina (True or False).")):
    comune = comune.upper()

    # Cerca l'alloggio nel Data Frame in base al comune
    results = df[df['COMUNE'] == comune]

    # Aggiungi la logica per filtrare in base alla presenza della piscina
    if piscina is not None and piscina:
        results = results[results['PISCINA'] == 'Vero']

    # Estrai il nome dell'alloggio e il link associato
    denominazione_alloggio = results['DENOMINAZIONE'].tolist()
    link_alloggio = results['SITO WEB'].tolist()  # Assumi che la colonna LINK contenga i link delle strutture

    # Cerca i musei nel Data Frame in base al comune
    results_musei = df_musei[df_musei['Comune'] == comune]

    # Estrai il nome dei musei
    denominazione_musei = results_musei['Nome'].tolist()

    # Costruisci la lista di risultati con nomi cliccabili
    result_list = []
    for nome, link in zip(denominazione_alloggio, link_alloggio):
        result_item = {"nome": nome}
        if pd.notna(link):  # Controlla se il link non è NaN
            result_item["link"] = link
        result_list.append(result_item)
    print(f"{result_list}")
    if denominazione_musei or denominazione_alloggio:
        return {"comune": comune, "risultati": result_list, "musei_consigliati": denominazione_musei}
    else:
        return {"error": "Alloggio non trovato"}
"""
@app.get('/module/search/{person_name}')
def read_item_from_module(person_name: str):
    return {return_birthday(person_name)}


@app.get('/module/all')
def dump_all_birthdays():
    return {print_birthdays_str()}
"""

@app.get('/get-date')
def get_date():
    """
    Endpoint to get the current date.

    Returns:
        dict: Current date in ISO format.
    """
    current_date = datetime.now().isoformat()
    return JSONResponse(content={"date": current_date})
