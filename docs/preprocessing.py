"""
Este arquivo contém funções esboçadas para o carregamento de dados, pré-processamento, 
divisão de conjuntos de treinamento e teste, bem como para a escalonamento de recursos. 
"""

import pandas as pd
from pandas import DataFrame
from config import tempo_scaler
import numpy as np
import sklearn


# Carregar os Dados (E)
def load_data(file_path: str) -> DataFrame:
    return pd.read_csv(file_path)


# Limpar os dados (T)
def data_cleaning(base_fraude_raw1):
    # STEP 1: Renomear as colunas (Seção 1.2)
    base_fraude_raw1.rename(
        columns={
            "step": "Tempo",
            "type": "Tipo",
            "amount": "Quantia",
            "nameOrig": "ClienteOrigem",
            "oldbalanceOrg": "SaldoInicalOrig",
            "newbalanceOrig": "SaldoFinalOrig",
            "nameDest": "ClienteDest",
            "oldbalanceDest": "SaldoInicialDest",
            "newbalanceDest": "SaldoFinalDest",
            "isFraud": "Fraude",
        },
        inplace=True,
    )

    # STEP 2: Mudar os tipos, se necessário

    # STEP 3: Preenchimento de dados ausentes, se necessário

    return base_fraude_raw1


# Limpar os dados (T)
def feature_engineering(base_fraude_raw2):
    base_fraude_raw2["maior_50%"] = base_fraude_raw2[
        ["Quantia", "SaldoInicalOrig"]
    ].apply(
        lambda x: "yes" if x["Quantia"] / 2 > x["SaldoInicalOrig"] else "no", axis=1
    )

    base_salarial = 3800
    media_salarial = base_fraude_raw2["SaldoInicalOrig"].median()

    base_fraude_raw2["poder_compra"] = base_fraude_raw2["SaldoInicalOrig"].apply(
        lambda x: "baixa"
        if x <= base_salarial
        else "medio"
        if x > base_salarial and x <= media_salarial
        else "alta"
    )

    base_fraude_raw2["tipo_transacao"] = base_fraude_raw2[
        ["ClienteOrigem", "ClienteDest"]
    ].apply(
        lambda x: "C para C"
        if x["ClienteOrigem"][0] == "C" and x["ClienteDest"][0] == "C"
        else "M para M"
        if x["ClienteOrigem"][0] == "M" and x["ClienteDest"][0] == "M"
        else "C para M"
        if x["ClienteOrigem"][0] == "C" and x["ClienteDest"][0] == "M"
        else "M para C"
        if x["ClienteOrigem"][0] == "M" and x["ClienteDest"][0] == "C"
        else None,
        axis=1,
    )

    tipos_fraude = ["CASH_OUT", "TRANSFER"]
    base_fraude_real = base_fraude_raw2[base_fraude_raw2["Tipo"].isin(tipos_fraude)]

    # Realizar filtro de colunas, se necessário

    return base_fraude_real


# Preparar os dados para entrar no modelo (T)
def data_preparation(df):
    # Scaler
    tempo_scaler = pickle.load(open(HOME_PATH + "parameter/tempo_scaler.pkl", "rb"))
    df["Tempo"] = tempo_scaler.fit_transform(df[["Tempo"]].values)

    # LabelEncoder
    label_encoder = LabelEncoder()
    df["poder_compra"] = label_encoder.fit_transform(df["poder_compra"])
    df["maior_50%"] = label_encoder.fit_transform(df["maior_50%"])
    df["Tipo"] = label_encoder.fit_transform(df["Tipo"])
    df["tipo_transacao"] = label_encoder.fit_transform(df["tipo_transacao"])

    # One-Hot Encoding
    df = pd.get_dummies(df, prefix="tipo_transacao", columns=["tipo_transacao"])

    cols_selected = [
        "Tempo",
        "Tipo",
        "Quantia",
        "ClienteOrigem",
        "SaldoInicalOrig",
        "SaldoFinalOrig",
        "ClienteDest",
        "SaldoInicialDest",
        "SaldoFinalDest",
        "Fraude",
        "isFlaggedFraud",
        "maior_50%",
        "poder_compra",
        "tipo_transacao_0",
    ]

    return df[cols_selected]
