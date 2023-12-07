from fastapi import FastAPI
from pydantic import BaseModel
from Valmir import Valmir
import pandas as pd 
import pickle

app = FastAPI()

# Instancie o modelo
detect_fraude = Valmir()

# Carregue o modelo salvo
with open("/home/valmir/Documentos/deteccao_fraude/src/xgboost.pkl", "rb") as model_file:
    model = pickle.load(model_file)

class Item(BaseModel):
    # Defina a estrutura dos dados de entrada aqui
    tempo: int
    tipo: int
    quantia: float
    clienteOrigem: str
    saldoInicialOrig: float
    saldoFinalOrig: float
    clienteDest: str
    saldoInicialDest: float
    saldoFinalDest: float
    poderCompra: str
    maior50: str
    tipoTransacao: str

# Rota para receber dados e retornar a previsão
@app.post("/predict")
async def predict(item: Item):
    data = item.dict()

    # Exemplo de pré-processamento (ajuste conforme necessário)
    df = pd.DataFrame([data])
    cleaned_data = detect_fraude.data_cleaning(df)
    feature_engineered_data = detect_fraude.feature_engineering(cleaned_data)
    prepared_data = detect_fraude.data_preparation(feature_engineered_data)
    selected_features = detect_fraude.feature_selection(prepared_data)

       # Selecione as colunas relevantes para a previsão
    X = selected_features.drop(columns=["Fraude", "isFlaggedFraud"])

    # Faça a previsão usando o modelo
    prediction_result = detect_fraude.get_prediction(model, prepared_data, X)

    return {"prediction": prediction}