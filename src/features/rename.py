import pandas as pd
import json

def renomear_colunas(dataset, json_path):
     """
    Renomeia as colunas de um dataset com base em um arquivo JSON de mapeamento.

    Args:
        dataset (pandas DataFrame): O dataset cujas colunas você deseja renomear.
        json_path (str): O caminho para o arquivo JSON de mapeamento das colunas.

    Returns:
        pandas DataFrame: O dataset com as colunas renomeadas.
    """
     with open(json_path, 'r') as json_file:
            json_rename = json.load(json_file)
     dataset.rename(columns=json_rename, inplace=True)

     return dataset
    
