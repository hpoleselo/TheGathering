import numpy as np
from math import pi, sin, cos

# As pos falta sao dadas em PU
# corrente de falta -> tensao pos falta p/ 9 barras e pras 3 sequencias
# 120 graus entre cada seq, 240 na ultima
# TODO: Dar em PU e em Volts

def ret2pol(x, y):
    modulo = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    theta = theta*(180/pi)
    return(modulo, theta)

def pol2ret(modulo, theta):
    # Converter para radianos, já que Python usa rad
    theta = theta*pi/180
    x = modulo * np.cos(theta)
    y = modulo * np.sin(theta)
    return(complex(x,y))

# Importando ZBarra calculado no programa anterior
ZBarra = np.genfromtxt('zbarra.csv', dtype=complex, delimiter=',')

# Resistencia de falta para as 3 fases
ZfA = 0.467 # Questao 3 Letra A, ou seja, resistencia na fase A barra 4,6,7
ZfB = 1.187 # Questao 3 Letra B (ZBarra*120graus)
ZfC = 1.005 # Questao 3 Letra C

ZB1 = 1.9044000000000003
ZB2 = 1190.25
ZB3 = 0.17305600000000002
ZB4 = 190.44
ZB5 = 1.9044000000000003

# Tensão Pré-falta em regime permanente (PU)
VpreF4 = pol2ret(1.022, -13.6568)

# Defasamento da barra 4 em relação a barra 1
defasamento30Graus = pol2ret(1,30)
# Defasamento da barra 7 em relação a barra 1
defasamento90Graus = pol2ret(1,90)

VpreF4 = VpreF4*defasamento30Graus

# ----- Tensao Pós-Falta ------

# -- Resistencias de Falta --
Zf = np.zeros(8)
# Para Letra A, usa-se a ZB2
Zf[4] = ZfA/ZB2
# Para Letra B, usa-se a ZB4
Zf[6] = ZfB/ZB4
# Para Letra C, usa-se a ZB5
Zf[7] = ZfC/ZB5


Ifk = VpreF4/(ZfA + ZBarra[4,4]) # Corrente de Falta

# !!!!!!!!! CONSIDERAÇÃO: tensão pre-falta é a mesma, no final iremos defasar !!!!!!!!!!!!!

# Criando vetor para guardar os valores de VpreF
VpreF = np.zeros(10, dtype=complex)
VpreF[1] = pol2ret(1.0394,-13.8148)
VpreF[2] = pol2ret(1.0266,-13.8715)
VpreF[3] = pol2ret(1.0346,-14.0869)
VpreF[4] = pol2ret(1.0222,-13.6568)
VpreF[5] = pol2ret(1.0166,-20.6902)
VpreF[6] = pol2ret(1.0161,-21.1685)
VpreF[7] = pol2ret(0.9891,-26.0122)
VpreF[8] = pol2ret(1.0136,-12.2356)
VpreF[9] = pol2ret(1.0207,-8.8582)

If = np.zeros(10, dtype=complex)


barra = [4, 6, 7]
# k indica o local onde ocorre a falta
for k in barra:
    print(f'Falta na barra {k}')
    If[k] = VpreF[k]/(Zf[k] + ZBarra[k,k])
    re_ifk = If[k].real
    im_ifk = If[k].imag
    #print(re_ifk, im_ifk)
    #print(type(re_ifk), type(im_ifk))
    If[k] = ret2pol(re_ifk, im_ifk)
    print(f'Corrente de Falta na barra {k} é: {If[k]}')

    for n in range(1,10):
        print(f'Calculando a tensao pós-falta na barra {n}')
        #VposN = VpreN - ZBarra[i,i]*Ifk  


VposF4 = VpreF4 - ZBarra[4,4]*Ifk        # Tensão pós-falta
print(VposF4)


# TODO: Calcular a tensão pós-falta nas outras barras


# TODO: Correntes Circuvizinha
# Correntes adjacentes àos lugares das faltas
# Calcular todas as ramificacoes de onde a falta se deu, da barra 4
# para calcular a corrente circunviinha: tensao de pos falta entre as barras/impedancia

#Iv = (VposF4 - VposF3)/ZLTij
