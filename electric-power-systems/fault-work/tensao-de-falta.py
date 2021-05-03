from copy import deepcopy, copy
from math import pi, sin, cos, sqrt
import pandas as pd
import numpy as np


def ret2pol(x, y):
    modulo = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    theta = theta*(180/pi)
    return (modulo, theta)

def pol2ret(modulo, theta):
    # Converter para radianos, já que Python usa rad internamente
    theta = theta*(pi/180)
    x = modulo * np.cos(theta)
    y = modulo * np.sin(theta)
    return(complex(x,y))

# -- Funções Auxiliares --
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

    #mtiz = pd.DataFrame(matrizDefasagemFinal)
    #print(mtiz)

    return matrizDefasagemFinal, VetDefasagem


#region Dados do Código Anterior

LT01C1Z = 0.004589035916824197+0.05059251417769376j
LT01C2Z = 0.004589035916824197+0.05059251417769376j
LT02C1Z = 0.004627027935307709+0.05150148288174754j
LT02C2Z = 0.004627027935307709+0.05150148288174754j
LT03C1Z = 0.00542410417979416+0.05754327242176014j
LT04C1Z = 0.005848452005881117+0.07352606595253099j
LT05C1Z = 0.007037807183364839+0.08547561436672968j
TR02T1Z = 0.12280000000000002j
TR03T1Z = 0.1678j

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
IB1 = SBase/(VBase1*sqrt(3))
IB2 = SBase/(VBase2*sqrt(3))
IB3 = SBase/(VBase3*sqrt(3))
IB4 = SBase/(VBase4*sqrt(3))
IB5 = SBase/(VBase5*sqrt(3))


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

#region -- Calculando as Correntes de Falta e Tensão Pós-Falta
# Inicializando a corrente de falta
If = np.zeros(10, dtype=complex)
# Inicializando as tensões pós-falta, deixamos uma dimensão maior para as correntes Circunvizinhas
Vpos = np.zeros(100, dtype=complex)
Vpos = Vpos.reshape(10,10)

# Inicializando as correntes Circunvizinhas
Iv = np.zeros(10, dtype=complex)

# Inicializando o vetor das tensões pós-falta para armazenar as tensões em referência a barra 4
Vpos_ = np.zeros(100, dtype=complex)
Vpos_ = Vpos_.reshape(10,10)

matrizDefasagemFinal, VetDefasagem = gerarMatrizesDefasamento()

# Barras onde ocorrem as faltas
barra = [4, 6, 7]

for k in barra:

    print(f'\n\n\n------------ Falta na Barra {k} ------------')

    # Multiplicando pelo VetDefasagem pois este possui as defasagens corretas
    If[k] = (VpreF[k] * VetDefasagem[k]) / (Zf[k] + ZBarra[k-1,k-1]) # k-1 pois eh uma matriz 10x10
    
    for n in range(1,10):

        # Em relação a barra 4, escrever as tensões em relação a si propria
        Vpos[k,n] = (VpreF[n] * VetDefasagem[n]) - (ZBarra[n-1,k-1] * If[k])

        # Copiando os valores das tensões pós-falta para o cálculo das correntes Circunvizinhas (pois)
        Vpos_[k,n] = deepcopy(Vpos[k,n])
        
        # Matriz adicionada para colocar as barras em referência a si mesma
        Vpos[k,n] = Vpos[k,n] * matrizDefasagemFinal[k,n]

        re_vpos = Vpos[k,n].real
        im_vpos = Vpos[k,n].imag
        Vpos_polar_r, Vpos_polar_theta = ret2pol(re_vpos, im_vpos)

        print(f'\nTensão pós-falta na barra {n} é: Módulo(PU): {Vpos_polar_r} Fase(graus): {Vpos_polar_theta}')
        
        if (n in [2,4,8,9]):
            print("")
            print(f'Tensão pós-falta na barra {n} é: Módulo(kV): {Vpos_polar_r*VBase2} Fase(graus): {Vpos_polar_theta}')
        elif(n in [1,7]):
            print(f'Tensão pós-falta na barra {n} é: Módulo(kV): {Vpos_polar_r*VBase1} Fase(graus): {Vpos_polar_theta}')
        elif(n in [3]):
            print(f'Tensão pós-falta na barra {n} é: Módulo(kV): {Vpos_polar_r*VBase3} Fase(graus): {Vpos_polar_theta}')
        elif(n in [5,6]):
            print(f'Tensão pós-falta na barra {n} é: Módulo(kV): {Vpos_polar_r*VBase4} Fase(graus): {Vpos_polar_theta}')
#endregion

#region -- Correntes Circuvizinhas --
Iv_4_2 = (Vpos_[4,2] - Vpos_[4,4] )/ LT01C1Z
re_iv42 = Iv_4_2.real
im_iv42 = Iv_4_2.imag
Iv_42r, Iv_42theta = ret2pol(re_iv42, im_iv42)

Iv_4_5 = (Vpos_[4,4] - Vpos_[4,5]) / TR02T1Z
re_iv45 = Iv_4_5.real
im_iv45 = Iv_4_5.imag
Iv_45r, Iv_45theta = ret2pol(re_iv45, im_iv45)

Iv_4_8 = (Vpos_[4,8] - Vpos_[4,4]) / LT02C1Z
re_iv48 = Iv_4_8.real
im_iv48 = Iv_4_8.imag
Iv_48r, Iv_48theta = ret2pol(re_iv48, im_iv48)

Iv_4_9 = (Vpos_[4,9] - Vpos_[4,4]) / LT04C1Z
re_iv49 = Iv_4_9.real
im_iv49 = Iv_4_9.imag
Iv_49r, Iv_49theta = ret2pol(re_iv49, im_iv49)

Iv_6_5 = (Vpos_[6,5]- Vpos_[6,6]) / LT05C1Z
re_iv65 = Iv_6_5.real
im_iv65 = Iv_6_5.imag
Iv_65r, Iv_65theta = ret2pol(re_iv65, im_iv65)

Iv_6_7 = (Vpos_[6,6] - Vpos_[6,7]) / TR03T1Z
re_iv67 = Iv_6_7.real
im_iv67 = Iv_6_7.imag
Iv_67r, Iv_67theta = ret2pol(re_iv67, im_iv67)

Iv_7_6 = (Vpos_[7,6] - Vpos_[7,7]) / TR03T1Z
re_iv76 = Iv_7_6.real
im_iv76 = Iv_7_6.imag
Iv_76r, Iv_76theta = ret2pol(re_iv76, im_iv76)
#endregion


#region -- Printando Valores --
print("\n\n------------ Correntes de Falta ------------")

re_ifk4 = If[4].real
im_ifk4 = If[4].imag
Ifk4_polar_r, Ifk4_polar_theta  = ret2pol(re_ifk4, im_ifk4)
print(f'\nCorrente de Falta na barra 4 é: Módulo(PU): {Ifk4_polar_r} Fase(graus): {Ifk4_polar_theta}')
print(f'Corrente de Falta na barra 4 é: Módulo(kA): {Ifk4_polar_r*IB2} Fase(graus): {Ifk4_polar_theta}')

re_ifk6 = If[6].real
im_ifk6 = If[6].imag
Ifk6_polar_r, Ifk6_polar_theta  = ret2pol(re_ifk6, im_ifk6)
print(f'\nCorrente de Falta na barra 6 é: Módulo(PU): {Ifk6_polar_r} Fase(graus): {Ifk6_polar_theta}')
print(f'Corrente de Falta na barra 6 é: Módulo(kA): {Ifk6_polar_r*IB4} Fase(graus): {Ifk6_polar_theta}')

re_ifk7 = If[7].real
im_ifk7 = If[7].imag
Ifk7_polar_r, Ifk7_polar_theta  = ret2pol(re_ifk7, im_ifk7)
print(f'\nCorrente de Falta na barra 7 é: Módulo(PU): {Ifk7_polar_r} Fase(graus): {Ifk7_polar_theta}')
print(f'Corrente de Falta na barra 7 é: Módulo(kA): {Ifk7_polar_r*IB5} Fase(graus): {Ifk7_polar_theta}')

print("\n\n------------ Correntes Circunvizinhas ------------")

print(f'\nCorrente Circunvizinha Iv_4_2 é: Módulo(PU): {Iv_42r} Fase(graus): {Iv_42theta}')
print(f'Corrente Circunvizinha Iv_4_2 é: Módulo(kA): {Iv_42r*IB2} Fase(graus): {Iv_42theta}')

print(f'\nCorrente Circunvizinha Iv_4_5 é: Módulo(PU): {Iv_45r} Fase(graus): {Iv_45theta}')
print(f'Corrente Circunvizinha Iv_4_5 é: Módulo(kA): {Iv_45r*IB2} Fase(graus): {Iv_45theta}')

print(f'\nCorrente Circunvizinha Iv_4_8 é: Módulo(PU): {Iv_48r} Fase(graus): {Iv_48theta}')
print(f'Corrente Circunvizinha Iv_4_8 é: Módulo(kA): {Iv_48r*IB2} Fase(graus): {Iv_48theta}')

print(f'\nCorrente Circunvizinha Iv_4_9 é: Módulo(PU): {Iv_49r} Fase(graus): {Iv_49theta}')
print(f'Corrente Circunvizinha Iv_4_9 é: Módulo(kA): {Iv_49r*IB2} Fase(graus): {Iv_49theta}')

print(f'\nCorrente Circunvizinha Iv_6_5 é: Módulo(PU): {Iv_65r} Fase(graus): {Iv_65theta}')
print(f'Corrente Circunvizinha Iv_6_5 é: Módulo(kA): {Iv_65r*IB4} Fase(graus): {Iv_65theta}')

print(f'\nCorrente Circunvizinha Iv_6_7 é: Módulo(PU): {Iv_67r} Fase(graus): {Iv_67theta}')
print(f'Corrente Circunvizinha Iv_6_7 é: Módulo(kA): {Iv_67r*IB4} Fase(graus): {Iv_67theta}')

print(f'\nCorrente Circunvizinha Iv_7_6 é: Módulo(PU): {Iv_76r} Fase(graus): {Iv_76theta}')
print(f'Corrente Circunvizinha Iv_7_6 é: Módulo(kA): {Iv_76r*IB5} Fase(graus): {Iv_76theta}')
#endregion