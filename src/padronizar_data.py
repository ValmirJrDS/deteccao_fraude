import pandas as pd
from features import new_maior_50
from features import rename
from features import new_poer_compra
from features import new_tipo_cliente
from data import padronizacao
from data import load
import json
from IPython.display import display

base_teste_final = load.load_data('data/intermediario/base_fraude_raw_teste.csv', 'csv')

base_teste_final = rename.renomear_colunas(base_teste_final, 'src/json_rename.json')

base_teste_final = new_maior_50.feature_maior_50(base_teste_final)

base_teste_final = new_poer_compra.feature_poder_compra(base_teste_final, 3800)

base_teste_final = new_tipo_cliente.feature_tipo_cliente(base_teste_final)

base_teste_final = padronizacao.padronizar(base_teste_final)

del base_teste_final['Unnamed: 0']

display(base_teste_final)