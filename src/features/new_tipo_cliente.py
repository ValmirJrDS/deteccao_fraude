import pandas as pd 

def feature_tipo_cliente(dataset):
    dataset['tipo_transacao'] = dataset[['ClienteOrigem', 'ClienteDest']].apply(
    lambda x: 'C para C' if x['ClienteOrigem'][0] == 'C' and x['ClienteDest'][0] == 'C' else 'M para M'
                         if x['ClienteOrigem'][0] == 'M' and x['ClienteDest'][0] == 'M' else 'C para M'
                         if x['ClienteOrigem'][0] == 'C' and x['ClienteDest'][0] == 'M' else 'M para C'
                         if x['ClienteOrigem'][0] == 'M' and x['ClienteDest'][0] == 'C' else None, axis=1)
    return dataset