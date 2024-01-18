import pandas as pd

def format_results(results, results_musei):
    # Placeholder result formatting logic
    result_list = []

    for _, row in results.iterrows():
        result_item = {"nome": row['DENOMINAZIONE']}

        if pd.notna(row['SITO WEB']):
            result_item["link"] = row['SITO WEB']
        if pd.notna(row['INDIRIZZO']):
            result_item["indirizzo"] = row['INDIRIZZO']
        if pd.notna(row['TELEFONO']):
            result_item["telefono"] = row['TELEFONO']
        if pd.notna(row['EMAIL']):
            result_item["email"] = row['EMAIL']

        result_list.append(result_item)

    if results_musei.empty and not result_list:
        return {"error": "Alloggio non trovato"}
    
    formatted_results = {"comune": results_musei.iloc[0]['Comune'], "risultati": result_list, "musei_consigliati": results_musei['Nome'].tolist()}
    
    return formatted_results