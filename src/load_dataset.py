from IPython.display import display
from data import load

base_teste_final = load.load_data("data/intermediario/base_fraude_raw_teste", "csv")
del base_teste_final['Unnamed: 0']

display(base_teste_final)