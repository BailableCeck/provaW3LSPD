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
def read_item(comune: str):
    """
    Endpoint to query accommodation information based on comune.

    Args:
        comune (str): The comune name.

    Returns:
        dict: Accommodation information for the provided comune.
    """
    comune = comune.upper()  # Convert to title case for consistency

    # Cerca l'alloggio nel Data Frame in base al comune
    results = df[df['COMUNE'] == comune]['DENOMINAZIONE'].tolist()

    if results:
        # Estrai il nome dell'alloggio
        return {"comune": comune, "denominazione_alloggio": results}
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
