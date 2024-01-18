import pandas as pd

def format_results(results):
    
    alloggio = results['DENOMINAZIONE'].tolist()
    l_alloggio = results['SITO WEB'].tolist()
    i_alloggio = results['INDIRIZZO'].tolist()
    n_telefono= results['TELEFONO'].tolist()
    i_email = results['EMAIL'].tolist()
    
    result_list = []

    for nome, link, indirizzo, telefono, email in zip(alloggio, l_alloggio, i_alloggio, n_telefono, i_email):
        result_item = {"nome": nome}
        if pd.notna(link):
            result_item["link"] = link
        if pd.notna(indirizzo):
            result_item["indirizzo"] = indirizzo
        if pd.notna(telefono):
            result_item["telefono"] = telefono
        if pd.notna(email):
            result_item["email"] = email

        result_list.append(result_item)

    return result_list