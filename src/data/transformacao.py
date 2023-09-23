import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

def transformar_data(dataset):
    label_encoder = LabelEncoder()
    dataset['poder_compra'] = label_encoder.fit_transform(dataset['poder_compra'])
    dataset['maior_50%'] = label_encoder.fit_transform(dataset['maior_50%'])
    dataset['Tipo'] = label_encoder.fit_transform(dataset['Tipo'])
    dataset['tipo_transacao'] = label_encoder.fit_transform(dataset['tipo_transacao'])

    return dataset