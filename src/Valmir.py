"""
Este arquivo contém funções esboçadas para o carregamento de dados, pré-processamento, 
divisão de conjuntos de treinamento e teste, bem como para a escalonamento de recursos. 
"""

import pandas as pd
from pandas import DataFrame
import json
import numpy as np
import sklearn
import pickle



class Valmir:

    def __init__(self):

        #Carregar as transformações
        self.lb_maior_50 = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/lb_maior_50.pkl', 'rb'))
        self.lb_poder_compra = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/lb_poder_compra.pkl', 'rb'))
        self.lb_tipo_transacao = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/lb_tipo_transacao.pkl', 'rb'))
        self.lb_tipo = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/lb_tipo.pkl', 'rb'))
        self.rs_passos = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/rs_passos.pkl', 'rb'))
        self.rs_quantia = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/rs_quantia.pkl', 'rb'))
        self.rs_saldo_orig_inicial = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/rs_saldo_orig_inicial.pkl', 'rb'))
        self.rs_saldofinaldest = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/rs_saldofinaldest.pkl', 'rb'))
        self.rs_saldoinicialdest = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/rs_saldoinicialdest.pkl', 'rb'))


    # Carregar os Dados (E)
    def load_data(self,file_path: str) -> DataFrame:
        return pd.read_csv(file_path)


    # Limpar os dados (T)
    def data_cleaning(self,base_fraude_raw1):
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
    def feature_engineering(self,base_fraude_raw2):
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
    def data_preparation(self,base_fraude_real):

        # Scaler
        
        base_fraude_real['Tempo'] = self.rs_passos.transform(base_fraude_real[['Tempo']].values)
        base_fraude_real['Quantia'] = self.rs_quantia.transform(base_fraude_real[['Quantia']].values)
        base_fraude_real['SaldoFinalOrig'] =  self.rs_saldo_orig_inicial.transform(base_fraude_real[['SaldoFinalOrig']].values)
        base_fraude_real['SaldoFinalDest'] = self.rs_saldofinaldest.transform(base_fraude_real[['SaldoFinalDest']].values)
        base_fraude_real['SaldoInicialDest'] = self.rs_saldoinicialdest.transform(base_fraude_real[['SaldoInicialDest']].values)



        # LabelEncoder
        base_fraude_real["poder_compra"] = self.lb_poder_compra.transform(base_fraude_real["poder_compra"])
        base_fraude_real["maior_50%"] = self.lb_maior_50.transform(base_fraude_real["maior_50%"])
        base_fraude_real["Tipo"] = self.lb_tipo.transform(base_fraude_real["Tipo"])
        base_fraude_real["tipo_transacao"] = self.lb_tipo_transacao.transform(base_fraude_real["tipo_transacao"])

        # One-Hot Encoding
        base_fraude_real = pd.get_dummies(base_fraude_real, prefix="tipo_transacao", columns=["tipo_transacao"])

        return base_fraude_real

    def feature_selection(self, base_fraude_real):
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

            base_fraude_real = base_fraude_real[cols_selected]


            return base_fraude_real

    
    def get_prediction(self, model, original_data, test_data):
        # Predição
        prediction = self.get_prediction(model, test_data)

        # Concatena a predicao aos dados originais e, se necessário,
        # aplica alguma operação aos resultados da predição.
        original_data["prediction"] = prediction

        return original_data.to_json(orient="records", date_format="iso")