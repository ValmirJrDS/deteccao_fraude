import pandas as pd
import json
from IPython.display import display
from features import rename

base_teste_final = pd.read_csv('data/intermediario/base_fraude_raw_teste')

base_teste_final = rename.renomear_colunas(base_teste_final, 'src/json_rename.json')

del base_teste_final['Unnamed: 0']

display(base_teste_final)





