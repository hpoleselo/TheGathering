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
    # TODO: Resolver problema de retornar como tuple
    return (modulo, theta)

def pol2ret(modulo, theta):
    # Converter para radianos, já que Python usa rad
    theta = theta*(pi/180)
    x = modulo * np.cos(theta)
    y = modulo * np.sin(theta)
    return(complex(x,y))

# Importando ZBarra calculado no programa anterior
ZBarra = np.genfromtxt('zbarra.csv', dtype=complex, delimiter=',')
print(f'Deveria ser 11:{ZBarra[0,0]} \nDeveria ser 22:{ZBarra[1,1]} \nDeveria ser 33:{ZBarra[2,2]} \nDeveria ser 44:{ZBarra[3,3]}')

# Resistencia de falta para as 3 fases
ZfA = 0.467 # Questao 3 Letra A, ou seja, resistencia na fase A barra 4,6,7
ZfB = 1.187 # Questao 3 Letra B (ZBarra*120graus)
ZfC = 1.005 # Questao 3 Letra C

ZB1 = 1.9044000000000003
ZB2 = 1190.25
ZB3 = 0.17305600000000002
ZB4 = 190.44
ZB5 = 1.9044000000000003

# Defasamento da barra 4 em relação a barra 1
defasamento30Graus = pol2ret(1,30)

# Defasamento da barra 7 em relação a barra 1
defasamento90GrausNeg = pol2ret(1,-90)
defasamento0Grau = pol2ret(1,0)

print(defasamento30Graus)
print(defasamento90GrausNeg)
print(defasamento0Grau)

# ----- Tensao Pós-Falta ------

# -- Resistencias de Falta em PU --
Zf = np.zeros(8)
# Para Letra A, usa-se a ZB2
Zf[4] = ZfA/ZB2
# Para Letra B, usa-se a ZB4
Zf[6] = ZfB/ZB4
# Para Letra C, usa-se a ZB5
Zf[7] = ZfC/ZB5

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
Vpos = np.zeros(10, dtype=complex)

# Adicionando as defasagens no vetor
Vpos[1] = defasamento0Grau
# Trafo 1 adiciona 30 graus
Vpos[2] = defasamento30Graus
Vpos[3] = defasamento0Grau
# Trafo 1 adiciona 30 graus, pois é sempre em ref. a barra 1
Vpos[4] = defasamento30Graus
# Tira os 30 graus devido ao Trafo 2
Vpos[5] = defasamento0Grau
Vpos[6] = defasamento0Grau
# Devido ao Trafo 3, tira 90 graus
Vpos[7] = defasamento90GrausNeg
Vpos[8] = defasamento30Graus
Vpos[9] = defasamento30Graus

# Fazendo cópia para manter o Vpos original apenas com as defasagens
# TODO: MUDAR A PORRA DO NOME PRA VETOR_DEFASAGEM
_Vpos = Vpos

# Barras onde ocorrem as faltas
barra = [4, 6, 7]


for k in barra:
    #print("\n")
    print(f'\n\n\n######## Falta na barra {k} #######')
    # Multiplicando pelo _VPos pois este possui as defasagens corretas
    If[k] = (VpreF[k]*_Vpos[k]) / (Zf[k] + ZBarra[k-1,k-1]) # k-1 pois eh uma matriz 10x10
    re_ifk = If[k].real
    im_ifk = If[k].imag
    # Expondo em polar pois no Anafas é como sera inputado
    Ifk_polar_r, Ifk_polar_theta  = ret2pol(re_ifk, im_ifk)
    print(f'\nCorrente de Falta na barra {k} é: Módulo(PU): {Ifk_polar_r} Fase(graus): {Ifk_polar_theta}')

    for n in range(1,10):
        Vpos[n] = (VpreF[n] * _Vpos[n]) - (ZBarra[n-1,k-1] * If[k])
        re_vpos = Vpos[n].real
        im_vpos = Vpos[n].imag
        Vpos_polar_r, Vpos_polar_theta = ret2pol(re_vpos, im_vpos)
        print(f'\n Tensão pós-falta na barra {n} é: Módulo(PU): {Vpos_polar_r} Fase(graus): {Vpos_polar_theta}')

# TODO VER DEFASAGEM 5, 6

# TODO: Correntes Circuvizinha
# Correntes adjacentes àos lugares das faltas
# Calcular todas as ramificacoes de onde a falta se deu, da barra 4
# para calcular a corrente circunviinha: tensao de pos falta entre as barras/impedancia

#Iv = (VposF4 - VposF3)/ZLTij
