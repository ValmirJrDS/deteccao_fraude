import pandas as pd
from sklearn.model_selection import train_test_split

def div_treino_teste(dataset, coluna_alvo, tamanho_teste=0.3, random_state=42):
    """
    Divide um dataset em conjuntos de treino e teste, nomeia as bases e retorna as bases de treino e teste.

    Args:
        dataset (pandas DataFrame): O dataset que você deseja dividir.
        coluna_alvo (str): O nome da coluna alvo.
        tamanho_teste (float): A proporção do dataset a ser usado como conjunto de teste (padrão é 0.2).
        random_state (int ou None): Seed para a aleatoriedade na divisão. Use None para resultados não determinísticos.

    Returns:
        pandas DataFrame, pandas DataFrame: Duas bases de dados pandas, uma para treino e outra para teste.
    """
    X = dataset.drop(coluna_alvo, axis=1)
    y = dataset[coluna_alvo]

    # Divide o dataset em conjuntos de treino e teste
    X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=tamanho_teste, stratify=y, random_state=random_state)

    # Nomeia as bases de treino e teste
    base_treino = pd.concat([X_treino, y_treino], axis=1)
    base_teste = pd.concat([X_teste, y_teste], axis=1)

    return base_treino, base_teste






