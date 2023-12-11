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
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder




class Valmir:

    def __init__(self):

        #Carregar as transformações
        self.lb_maior_50 = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/lb_maior_50.pkl', 'rb'))
        self.lb_poder_compra = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/lb_poder_compra.pkl', 'rb'))
        self.lb_tipo_transacao = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/lb_tipo_transacao.pkl', 'rb'))
        self.lb_tipo = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/lb_tipo.pkl', 'rb'))
        self.rs_passos = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/rs_passos.pkl', 'rb'))
        self.rs_Quantia = pickle.load(open('/home/valmir/Documentos/deteccao_fraude/src/parameter/rs_quantia.pkl', 'rb'))
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
                "step": "tempo",
                "type": "tipo",
                "amount": "Quantia",
                "nameOrig": "clienteOrigem",
                "oldbalanceOrg": "SaldoInicialOrig",
                "newbalanceOrig": "SaldoFinalOrig",
                "nameDest": "clienteDest",
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
            ["Quantia", "SaldoInicialOrig"]
        ].apply(
            lambda x: "yes" if x["Quantia"] / 2 > x["SaldoInicialOrig"] else "no", axis=1
        )

        base_salarial = 3800
        media_salarial = base_fraude_raw2["SaldoInicialOrig"].median()

        base_fraude_raw2["poder_compra"] = base_fraude_raw2["SaldoInicialOrig"].apply(
            lambda x: "baixa"
            if x <= base_salarial
            else "medio"
            if x > base_salarial and x <= media_salarial
            else "alta"
        )
        base_fraude_raw2["clienteOrigem"] = base_fraude_raw2["clienteOrigem"].astype(str)
        base_fraude_raw2["clienteDest"] = base_fraude_raw2["clienteDest"].astype(str)
        base_fraude_raw2["tipo_transacao"] = base_fraude_raw2[
            ["clienteOrigem", "clienteDest"]
        ].apply(
            lambda x: "C para C"
            if x["clienteOrigem"][0] == "C" and x["clienteDest"][0] == "C"
            else "M para M"
            if x["clienteOrigem"][0] == "M" and x["clienteDest"][0] == "M"
            else "C para M"
            if x["clienteOrigem"][0] == "C" and x["clienteDest"][0] == "M"
            else "M para C"
            if x["clienteOrigem"][0] == "M" and x["clienteDest"][0] == "C"
            else None,
            axis=1,
        )

        tipos_fraude = ["CASH_OUT", "TRANSFER"]
        base_fraude_real = base_fraude_raw2[base_fraude_raw2["tipo"].isin(tipos_fraude)]

        # Realizar filtro de colunas, se necessário

        return base_fraude_real


    # Preparar os dados para entrar no modelo (T)
    def data_preparation(self,base_fraude_real):

        # Scaler
        
        base_fraude_real['tempo'] = self.rs_passos.transform(base_fraude_real[['tempo']].values)
        base_fraude_real['quantia'] = self.rs_Quantia.transform(base_fraude_real[['Quantia']].values)
        base_fraude_real['SaldoFinalOrig'] =  self.rs_saldo_orig_inicial.transform(base_fraude_real[['SaldoFinalOrig']].values)
        base_fraude_real['SaldoFinalDest'] = self.rs_saldofinaldest.transform(base_fraude_real[['SaldoFinalDest']].values)
        base_fraude_real['SaldoInicialDest'] = self.rs_saldoinicialdest.transform(base_fraude_real[['SaldoInicialDest']].values)



        # LabelEncoder
        base_fraude_real["poder_compra"] = self.lb_poder_compra.transform(base_fraude_real["poder_compra"])
        base_fraude_real["maior_50%"] = self.lb_maior_50.transform(base_fraude_real["maior_50%"])
        base_fraude_real["tipo"] = self.lb_tipo.transform(base_fraude_real["tipo"])
        base_fraude_real["tipo_transacao"] = self.lb_tipo_transacao.transform(base_fraude_real["tipo_transacao"])

        # One-Hot Encoding
        base_fraude_real = pd.get_dummies(base_fraude_real, prefix="tipo_transacao", columns=["tipo_transacao"])

        return base_fraude_real

    def feature_selection(self, base_fraude_real):
            
            cols_selected = [
            "tempo",
            "tipo",
            "Quantia",
            "clienteOrigem",
            "SaldoInicialOrig",
            "SaldoFinalOrig",
            "clienteDest",
            "SaldoInicialDest",
            "SaldoFinalDest",
            "Fraude",
            "isFlaggedFraud",
            "maior_50%",
            "poder_compra",
            "tipo_transacao_C para C",
           ]

            base_fraude_real = base_fraude_real[cols_selected]


            return base_fraude_real

    
    def get_prediction(self, model_loaded, original_data, test_data):
        # Predição
        with open("/home/valmir/Documentos/deteccao_fraude/src/model.pkl", "rb") as model_file:
         model_loaded = pickle.load(model_file)
        test_data = pd.DataFrame(test_data)
        prediction = model_loaded.predict(test_data)

        # Concatena a predicao aos dados originais e, se necessário,
        # aplica alguma operação aos resultados da predição.
        original_data = pd.DataFrame.from_dict(original_data)
        
        return original_data.to_json(orient="records", date_format="iso")