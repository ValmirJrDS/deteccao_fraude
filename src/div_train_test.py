import pandas as pd
from IPython.display import display 
from data import divisao

# Carregue seu dataset ou crie um DataFrame pandas
base_fraude_raw = pd.read_csv("data/raw/fraud_detection_dataset.csv")

# Chame a função para dividir e nomear as bases
base_treino, base_teste = divisao.div_treino_teste(base_fraude_raw, coluna_alvo="isFlaggedFraud", tamanho_teste=0.2, random_state=42)

display(base_treino)