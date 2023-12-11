from fastapi import FastAPI
from pydantic import BaseModel
from Valmir import Valmir
import pandas as pd 
import pickle
import logging

app = FastAPI()

# Instancie o modelo
detect_fraude = Valmir()

# Carregue o modelo salvo
with open("/home/valmir/Documentos/deteccao_fraude/src/xgboost.pkl", "rb") as model_file:
    model = pickle.load(model_file)

class Item(BaseModel):
    tempo: int
    tipo: int
    Quantia: float
    clienteOrigem: str
    SaldoInicialOrig: float
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
    print("Dados recebidos:")
    print(item.dict())

    # Exemplo de pré-processamento (ajuste conforme necessário)
    df = pd.DataFrame([item.dict()])
    #print("DataFrame após criação:")
    #print(df)

    # Restante do código...

    # Exemplo de pré-processamento (ajuste conforme necessário)
    df = pd.DataFrame([item.dict()])
    cleaned_data = detect_fraude.data_cleaning(df)
    feature_engineered_data = detect_fraude.feature_engineering(cleaned_data)
    prepared_data = detect_fraude.data_preparation(feature_engineered_data)
    selected_features = detect_fraude.feature_selection(prepared_data)

    # Selecione as colunas relevantes para a previsão
    
    X = selected_features.drop(columns=["Fraude", "isFlaggedFraud"])

    # Exemplo de pré-processamento (ajuste conforme necessário)
    df = pd.DataFrame([data])
    #print("DataFrame antes do pré-processamento:")
    #print(df)
    cleaned_data = detect_fraude.data_cleaning(df)
    # Restante do pré-processamento...


    # Faça a previsão usando o modelo
    X = pd.DataFrame(X)
    prediction_result = detect_fraude.get_prediction(model, prepared_data, X)
    logger = logging.getLogger(__name__)
    logger.info("Dados recebidos:")
    logger.info(item.dict())

    return {"prediction": prediction_result}

# Rota padrão para a raiz da aplicação
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Rota para o ícone favorito
@app.get("/favicon.ico")
async def get_favicon():
    return {"favicon": "not found"}
