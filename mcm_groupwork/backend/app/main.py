# main.py
from fastapi import FastAPI, Query
from mymodules import data_loader, filtering, result_formatter, utilities

app = FastAPI()

# Load data from .csv files
df = data_loader.load_accommodation_data('/app/app/output.csv')
df_musei = data_loader.load_musei_data('/app/app/musei_veneto.csv')

@app.get('/query/{comune}')
def read_item(
    comune: str,
    piscina: bool = Query(None),
    accesso_disabili: bool = Query(None),
    fitness: bool = Query(None),
    sauna: bool = Query(None),
    aria_condizionata: bool = Query(None),
    lago: bool = Query(None)
):
    # Use functions from filtering.py and result_formatter.py here
    comune = utilities.normalize_string(comune)
    results = filtering.apply_filters(df, piscina=piscina, accesso_disabili=accesso_disabili, fitness=fitness, sauna=sauna, aria_condizionata=aria_condizionata, lago=lago)
    formatted_results = result_formatter.format_results(results, df_musei)
    return formatted_results
