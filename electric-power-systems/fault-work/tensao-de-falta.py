import numpy as np
from copy import deepcopy
from math import pi, sin, cos
import pandas as pd

def ret2pol(x, y):
    modulo = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    theta = theta*(180/pi)
    return (modulo, theta)

def pol2ret(modulo, theta):
    # Converter para radianos, já que Python usa rad
    theta = theta*(pi/180)
    x = modulo * np.cos(theta)
    y = modulo * np.sin(theta)
    return(complex(x,y))

# Funções Auxiliares
defasamento0Grau = pol2ret(1,0)
defasamento30Graus = pol2ret(1,30)
defasamento30GrausNeg = pol2ret(1,-30)
defasamento90Graus = pol2ret(1,90)
defasamento90GrausNeg = pol2ret(1,-90)
defasamento120Graus = pol2ret(1,120)
defasamento120GrausNeg = pol2ret(1,-120)

def gerarMatrizesDefasamento():

    VetDefasagem = np.zeros(10, dtype=complex)
    #region -- Adicionando as defasagens devido aos trafos em cada barra, sempre em referencia à barra 1
    VetDefasagem[1] = defasamento0Grau
    # Trafo 1 adiciona 30 graus
    VetDefasagem[2] = defasamento30Graus
    VetDefasagem[3] = defasamento0Grau
    # Trafo 1 adiciona 30 graus, pois é sempre em ref. a barra 1
    VetDefasagem[4] = defasamento30Graus
    # Tira os 30 graus devido ao Trafo 2
    VetDefasagem[5] = defasamento0Grau
    VetDefasagem[6] = defasamento0Grau
    # Devido ao Trafo 3, tira 120 graus
    VetDefasagem[7] = defasamento90GrausNeg
    VetDefasagem[8] = defasamento30Graus
    VetDefasagem[9] = defasamento30Graus
    #endregion

    # Fazendo cópia para manter o VetDefasagem original apenas com as defasagens, deepcopy
    VetDefasagem = deepcopy(VetDefasagem)

    # Falta na Barra 4
    # Defasagens especificas para "inverter" ... [1, 3, 5, 6, 7]
    VetDefasagemA = np.zeros(10, dtype=complex)
    VetDefasagemA[1] = defasamento30GrausNeg
    VetDefasagemA[2] = defasamento0Grau
    VetDefasagemA[3] = defasamento30GrausNeg
    VetDefasagemA[4] = defasamento0Grau
    VetDefasagemA[5] = defasamento30GrausNeg
    VetDefasagemA[6] = defasamento30GrausNeg
    VetDefasagemA[7] = defasamento120GrausNeg
    VetDefasagemA[8] = defasamento0Grau
    VetDefasagemA[9] = defasamento0Grau

    # Falta na Barra 6
    VetDefasagemB = np.zeros(10, dtype=complex)
    VetDefasagemB[1] = defasamento0Grau
    VetDefasagemB[2] = defasamento30Graus
    VetDefasagemB[3] = defasamento0Grau
    VetDefasagemB[4] = defasamento30Graus
    VetDefasagemB[5] = defasamento0Grau
    VetDefasagemB[6] = defasamento0Grau
    VetDefasagemB[7] = defasamento90GrausNeg
    VetDefasagemB[8] = defasamento30Graus
    VetDefasagemB[9] = defasamento30Graus

    # Falta na Barra 7
    VetDefasagemC = np.zeros(10, dtype=complex)
    VetDefasagemC[1] = defasamento90Graus
    VetDefasagemC[2] = defasamento120Graus
    VetDefasagemC[3] = defasamento90Graus
    VetDefasagemC[4] = defasamento120Graus
    VetDefasagemC[5] = defasamento90Graus
    VetDefasagemC[6] = defasamento90Graus
    VetDefasagemC[7] = defasamento0Grau
    VetDefasagemC[8] = defasamento120Graus
    VetDefasagemC[9] = defasamento120Graus

    # Montando matriz para referenciar o defasamento de acordo com a falta na barra adequada facilmente no cálculo das tensões de pós falta
    # O numero da linha da matriz representa a barra em que ocorreu a falta
    # A coluna indica a defasagem que a determinada barra precisa sofrer
    matrizDefasagemFinal = np.zeros(100, dtype=complex)
    matrizDefasagemFinal = matrizDefasagemFinal.reshape(10,10)
    matrizDefasagemFinal[4] = VetDefasagemA
    matrizDefasagemFinal[6] = VetDefasagemB
    matrizDefasagemFinal[7] = VetDefasagemC

    # TODO: adicionar explicação

    # Falta na Barra 4
    VetDefasagem_a = np.zeros(10, dtype=complex)
    VetDefasagem_a[1] = defasamento0Grau
    VetDefasagem_a[2] = defasamento30Graus
    VetDefasagem_a[3] = defasamento0Grau
    VetDefasagem_a[4] = defasamento30Graus
    VetDefasagem_a[5] = defasamento0Grau
    VetDefasagem_a[6] = defasamento0Grau 
    VetDefasagem_a[7] = defasamento90GrausNeg
    VetDefasagem_a[8] = defasamento30Graus
    VetDefasagem_a[9] = defasamento30Graus

    # Falta na Barra 6
    VetDefasagem_b = np.zeros(10, dtype=complex)
    VetDefasagem_b[1] = defasamento0Grau
    VetDefasagem_b[2] = defasamento0Grau
    VetDefasagem_b[3] = defasamento0Grau
    VetDefasagem_b[4] = defasamento0Grau
    VetDefasagem_b[5] = defasamento0Grau
    VetDefasagem_b[6] = defasamento0Grau
    VetDefasagem_b[7] = defasamento90GrausNeg
    VetDefasagem_b[8] = defasamento30Graus
    VetDefasagem_b[9] = defasamento30Graus

    # Falta na Barra 7
    VetDefasagem_c = np.zeros(10, dtype=complex)
    VetDefasagem_c[1] = defasamento90GrausNeg
    VetDefasagem_c[2] = defasamento120GrausNeg
    VetDefasagem_c[3] = defasamento90GrausNeg
    VetDefasagem_c[4] = defasamento120GrausNeg
    VetDefasagem_c[5] = defasamento90GrausNeg
    VetDefasagem_c[6] = defasamento90GrausNeg
    VetDefasagem_c[7] = defasamento0Grau
    VetDefasagem_c[8] = defasamento120Graus
    VetDefasagem_c[9] = defasamento120Graus

    matrizDefasagemInicial = np.zeros(100, dtype=complex)
    matrizDefasagemInicial = matrizDefasagemInicial.reshape(10,10)
    matrizDefasagemInicial[4] = VetDefasagem_a
    matrizDefasagemInicial[6] = VetDefasagem_b
    matrizDefasagemInicial[7] = VetDefasagem_c

    #mtiz = pd.DataFrame(matrizDefasagemFinal)
    mtiz = pd.DataFrame(matrizDefasagemInicial)
    print(mtiz)
    #print(matrizDefasagemInicial)

    return matrizDefasagemFinal, matrizDefasagemInicial, VetDefasagem

#region Dados do Código Anterior
VBase1 = 13.8
VBase2 = 345
VBase3 = 4.16
VBase4 = 138
VBase5 = 13.8
SBase = 100

ZB1 = 1.9044000000000003
ZB2 = 1190.25
ZB3 = 0.17305600000000002
ZB4 = 190.44
ZB5 = 1.9044000000000003

# Importando ZBarra calculado no programa anterior
ZBarra = np.genfromtxt('zbarra.csv', dtype=complex, delimiter=',')
#endregion

# Corrente de Base
IB1 = SBase/VBase1

# Resistencia de falta para as 3 fases
ZfA = 0.467 # Questao 3 Letra A, ou seja, resistencia na fase A barra 4,6,7
ZfB = 1.187 # Questao 3 Letra B (ZBarra*120graus)
ZfC = 1.005 # Questao 3 Letra C

# -- Resistencias de Falta em PU --
Zf = np.zeros(8)
# Para Letra A, usa-se a ZB2
Zf[4] = ZfA/ZB2
# Para Letra B, usa-se a ZB4
Zf[6] = ZfB/ZB4
# Para Letra C, usa-se a ZB5
Zf[7] = ZfC/ZB5

#region -- Criando vetor para guardar os valores de VpreF, dados na tabela no roteiro do trabalho --
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
#endregion

# Inicializando a corrente de falta
If = np.zeros(10, dtype=complex)
# Inicializando as tensões pós-falta
Vpos = np.zeros(10, dtype=complex)

matrizDefasagemFinal, matrizDefasagemInicial, VetDefasagem = gerarMatrizesDefasamento()

# Barras onde ocorrem as faltas
barra = [4, 6, 7]

for k in barra:
    print(f'\n\n\n######## Falta na Barra {k} ########')
    # Multiplicando pelo _VPos pois este possui as defasagens corretas
    If[k] = (VpreF[k] * matrizDefasagemInicial[k,k]) / (Zf[k] + ZBarra[k-1,k-1]) # k-1 pois eh uma matriz 10x10
    re_ifk = If[k].real
    im_ifk = If[k].imag
    # Expondo em polar pois no Anafas é como sera inputado
    Ifk_polar_r, Ifk_polar_theta  = ret2pol(re_ifk, im_ifk)
    # TODO: Dar em PU e em Volts
    print(f'\nCorrente de Falta na barra {k} é: Módulo(PU): {Ifk_polar_r} Fase(graus): {Ifk_polar_theta}')
    for n in range(1,10):

        # Em relação a barra 4, escrever as tensões em relação a si propria
        Vpos[n] = (VpreF[n] * matrizDefasagemInicial[k,n]) - (ZBarra[n-1,k-1] * If[k])

        Vpos[n] = Vpos[n] * matrizDefasagemFinal[k,n]
        re_vpos = Vpos[n].real
        im_vpos = Vpos[n].imag
        Vpos_polar_r, Vpos_polar_theta = ret2pol(re_vpos, im_vpos)

        # TODO: Dar em PU e em Volts
        # VBase*
        print(f'\n Tensão pós-falta na barra {n} é: Módulo(PU): {Vpos_polar_r} Fase(graus): {Vpos_polar_theta}')

#region -- Correntes Circuvizinhas --
# Correntes adjacentes àos lugares das faltas
# Calcular todas as ramificacoes de onde a falta se deu, da barra 4
# para calcular a corrente circunvizinhas: tensao de pos falta entre as barras/impedancia

#Iv = (VposF4 - VposF3)/ZLTij
#endregion
