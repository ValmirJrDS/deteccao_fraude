import pandas as pd

def feature_maior_50(dataset):
    dataset['maior_50%'] = dataset[['Quantia', 'SaldoInicalOrig']].apply(
        lambda x: 'yes' if x['Quantia'] / 2 > x['SaldoInicalOrig'] else 'no', axis=1)
    
    return dataset
    