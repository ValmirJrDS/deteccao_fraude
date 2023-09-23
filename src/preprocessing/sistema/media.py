
print("Entrei em media")

def status(onenote, twonote, threenote ,fournote, sit=True):
    """
    ->Função para realizar Média e resultado das notas finas de cada aluno,
    inserindo as notas de cada Bimestre retornando sua média final e avaliação
    do seu resultado

    :param onenote: A nota do primeiro bimestre que se quer laça. O 'tipo' desse valor é FLOAT
    :param twonote: A nota do segundo bimestre que se quer laça. O 'tipo' desse valor é FLOAT
    :param threenote: A nota terceiro bimestre que se quer laça. O 'tipo' desse valor é FLOAT
    :param fournote: A nota do quarto bimestre que se quer laça. O 'tipo' desse valor é FLOAT
    :param sit: Aqui já esta predefinido os resultados de avaliação da media final: REPROVADO, APROVADO
                APROVADO COM LOUVOR.
    :return: O retorno é a Média de todas as Notas dos bimestres e o resultado do páramentro sit.

    """
    soma = onenote+twonote+threenote+fournote
    media= soma/4
    if sit:
        if media <=6:
            return f'Media Final: {media} situação = REPROVADO'
        elif media ==7:
            return f'Media Final: {media}. Resultado = APROVADO'
        elif media ==8:
            return f'Media Final: {media}. Resultado = APROVADO'
        else:
            media >=9
            return f'Media Final: {media}. Resultado = APROVADO COM LOUVOR'
