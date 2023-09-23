import pandas as pd
from features import new_maior_50
from features import rename
import json
from IPython.display import display


base_teste_final = pd.read_csv('data/intermediario/base_fraude_raw_teste')

base_teste_final = rename.renomear_colunas(base_teste_final, 'src/json_rename.json')

base_teste_final = new_maior_50.feature_maior_50(base_teste_final)

del base_teste_final['Unnamed: 0']

display(base_teste_final)