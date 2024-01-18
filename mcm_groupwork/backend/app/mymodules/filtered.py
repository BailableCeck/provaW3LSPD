import pandas as pd

def apply_filters(df,  piscina, accesso_disabili, fitness, sauna, aria_condizionata, lago):

    if piscina is not None and piscina:
        df = df[df['PISCINA'] == 'Vero']

    if accesso_disabili is not None and accesso_disabili:
        df = df[df['ACCESSO AI DISABILI'] == 'Vero']

    if fitness is not None and fitness:
        df = df[df['FITNESS'] == 'Vero']

    if sauna is not None and sauna:
        df = df[df['SAUNA'] == 'Vero']

    if aria_condizionata is not None and aria_condizionata:
        df = df[df['ARIA CONDIZIONATA'] == 'Vero']

    if lago is not None and lago:
        df = df[df['LAGO'] == 'Vero']

    return df