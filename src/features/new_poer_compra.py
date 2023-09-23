import pandas as pd

def feature_poder_compra(dataset,base_salarial:int):
     base_salarial == (int)
     media_salarial = dataset['SaldoInicalOrig'].median()

     dataset['poder_compra'] = dataset['SaldoInicalOrig'].apply(
        lambda x: 'baixa' if x <= base_salarial else 'medio'
                          if x > base_salarial and x <= media_salarial else 'alta')
     return (dataset)
