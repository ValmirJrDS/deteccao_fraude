import pandas as pd
from sklearn.preprocessing import RobustScaler

def padronizar(dataset):
    scaler = RobustScaler()
    num_cols = ['Tempo','Quantia', 'SaldoInicalOrig', 'SaldoFinalOrig', 'SaldoInicialDest', 'SaldoFinalDest']
    dataset[num_cols] = scaler.fit_transform(dataset[num_cols])

    return dataset


