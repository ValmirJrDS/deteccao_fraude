import pandas as pd
import json

def renomear_colunas_com_json(dataset, json_path):
    """
    Renomeia as colunas de um dataset com base em um arquivo JSON de mapeamento.

    Args:
        dataset (pandas DataFrame): O dataset cujas colunas você deseja renomear.
        json_path (str): O caminho para o arquivo JSON de mapeamento das colunas.

    Returns:
        pandas DataFrame: O dataset com as colunas renomeadas.
    """
    # Carrega o mapeamento de colunas a partir do arquivo JSON
    with open(json_path, 'r') as json_file:
        mapeamento_colunas = json.load(json_file)

    # Renomeia as colunas
    dataset.rename(columns=mapeamento_colunas, inplace=True)

    return dataset
    