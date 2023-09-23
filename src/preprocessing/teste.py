# IMPORTAR O MODULO MEDIA E CHAMA-LO DE "md"
from sistema import media as md


a = float(input('NOTA 1° BIMESTRE: '))
b = float(input('NOTA 2° BIMESTRE: '))
c = float(input('NOTA 3° BIMESTRE: '))
d = float(input('NOTA 4° BIMESTRE: '))


resp = md.status(a, b, c, d, sit=True)
print(resp)
