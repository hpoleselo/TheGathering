from copy import deepcopy, copy
from math import pi, sin, cos, sqrt
import pandas as pd
import numpy as np


def ret2pol(z):
    x = z.real
    y = z.imag
    modulo = np.sqrt(x**2 + y**2)
    theta = (180/pi)*(np.arctan2(y, x))
    return(modulo, theta)

def pol2ret(modulo, theta):
    # Converter para radianos, já que Python usa rad internamente
    theta = theta*(pi/180)
    x = modulo * np.cos(theta)
    y = modulo * np.sin(theta)
    return(complex(x,y))


# Defasagens para auxiliar na leitura do código
defasagem0Grau = pol2ret(1,0)
defasagem30GrausPos = pol2ret(1,30)
defasagem30GrausNeg = pol2ret(1,-30)
defasagem90GrausPos = pol2ret(1,90)
defasagem90GrausNeg = pol2ret(1,-90)
defasagem120GrausPos = pol2ret(1,120)
defasagem120GrausNeg = pol2ret(1,-120)

NA = 6
VBase1 = 13.8
VBase2 = 345
VBase3 = 4.16
VBase4 = 138
VBase5 = 13.8
SBase = 100
ZBase1 = ((VBase1**2)/SBase)
ZBase2 = ((VBase2**2)/SBase)
ZBase3 = ((VBase3**2)/SBase)
ZBase4 = ((VBase4**2)/SBase)
ZBase5 = ((VBase5**2)/SBase)

# Importando ZBarra e YBarra de sequência positiva do código da parte 1 do trabalho
ZBarra_positivo = np.genfromtxt('zbarra.csv', dtype=complex, delimiter=',')
YBarra_positivo = np.genfromtxt('ybarra.csv', dtype=complex, delimiter=',')
ybarra = pd.DataFrame(YBarra_positivo)
# Já que o ZBarra de seq. positivo é igual o de seq. negativa
ZBarra_neg = deepcopy(ZBarra_positivo)
YBarra_neg = deepcopy(YBarra_positivo)
ZBarraP = pd.DataFrame(ZBarra_positivo)


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

ZfA = 1.673
ZfB = 2.033
ZfC = 0.328

# -- Impedância de Falta em PU --
Zf = np.zeros(8)
# Para Letra A, usa-se a ZB2
Zf[4] = ZfA/ZBase2
# Para Letra B, usa-se a ZB4 TODO: CONFIRMAR CARALHO!
Zf[5] = ZfB/ZBase4
# Para Letra C, usa-se a ZB2
Zf[2] = ZfC/ZBase2


#region Matriz de transformação modal A = 1 1 1; 1 a**2 a; 1 a a**2
A = np.zeros(9, dtype=complex)

# Operador rotacional
a = pol2ret(1,120)

indices = [0, 1, 2, 3, 6]
indices2 = [5, 7]
indices3 = [4, 8]
A[indices] = 1
A[indices2] = a
A[indices3] = a**2
A = A.reshape(3,3)
#A_df = pd.DataFrame(A)
#print(A_df)
#A_inv = np.linalg.inv(A)
#Ainv_df = pd.DataFrame(A_inv)
#print(Ainv_df)
#endregion

# Potencia 
Scc3f = (1564.1935+29720.5403j)

# Equivalentes de Rede:
ZEQ1 = (0.0048+0.0569j) * (((13.8/VBase1)**2) * (SBase/100))
_ZEQ9 = ((abs((1)**2)) * SBase) / (Scc3f)
ZEQ9 = _ZEQ9.conjugate()

RPS = (0.0539+(NA/10000))/100
XPS = (4.2540+(NA/100))/100
ZPS = complex(RPS,XPS)

RPT = (0.2974+(NA/10000))/100
XPT = (18.1540+(NA/100))/100
ZPT = complex(RPT,XPT)

RST = (0.2981+(NA/10000))/100
XST = (15.9510+(NA/100))/100
ZST = complex(RST,XST)

ZP = ((ZPS+ZPT-ZST)/2)
ZS = ((ZPS-ZPT+ZST)/2)
ZT = ((-ZPS+ZPT+ZST)/2)

YP = 1/ZP
YS = 1/ZS
YT = 1/ZT

tmp1 = 9.15+(NA/100)
tmp1 = complex(0,tmp1)
TR02T1Z = (tmp1/100)*(SBase/75)
TR02T1Y = 1/TR02T1Z

tmp2 = (8.33+(NA/100))
tmp2 = complex(0, tmp2)
TR03T1Z = (tmp2/100)*(SBase/50)
TR03T1Y = 1/TR03T1Z

# Impedância da LT de seq. positiva
LT01C1Z_1 = ((0.01785+0.19679j)*(300+NA))/ZBase2
LT01C2Z_1 = ((0.01785+0.19679j)*(300+NA))/ZBase2
LT02C1Z_1 = ((0.01547+0.17219j)*(350+NA))/ZBase2
LT02C2Z_1 = ((0.01547+0.17219j)*(350+NA))/ZBase2
LT03C1Z_1 = ((0.03134+0.33248j)*(200+NA))/ZBase2
LT04C1Z_1 = ((0.01252+0.15740j)*(550+NA))/ZBase2
LT05C1Z_1 = ((0.04380+0.53196j)*(30+(NA/10)))/ZBase4

# Impedância da LT de seq. negativa
LT01C1Z_0 = ((0.10474+0.83159j)*(300+NA))/ZBase2
LT01C2Z_0 = ((0.10474+0.83159j)*(300+NA))/ZBase2
LT02C1Z_0 = ((0.09125+0.72486j)*(350+NA))/ZBase2
LT02C2Z_0 = ((0.09125+0.72486j)*(350+NA))/ZBase2
LT03C1Z_0 = ((0.30550+1.21921j)*(200+NA))/ZBase2
LT04C1Z_0 = ((0.09522+0.59865j)*(550+NA))/ZBase2
LT05C1Z_0 = ((0.48880+1.76855j)*(30+(NA/10)))/ZBase4


LT01C1Y_0 = 1/LT01C1Z_0
LT01C2Y_0 = 1/LT01C2Z_0
LT02C1Y_0 = 1/LT02C1Z_0
LT02C2Y_0 = 1/LT02C2Z_0
LT03C1Y_0 = 1/LT03C1Z_0
LT04C1Y_0 = 1/LT04C1Z_0
LT05C1Y_0 = 1/LT05C1Z_0


Z0 = pol2ret(0.19242,87.84669)
Y0 = 1/Z0

# Impedância Mutua para seq. 0
Z0m = ((0.05213 + 0.58234j) * (300+NA))/ZBase2

# Impedância do Trafo. de Aterramento
tmp = (6.385+NA/100)/100
ZAT01A1 = pol2ret(tmp,90)

# Pot de base no valor que ZAT101A1 foi calculado
ZAT01A1 = (ZAT01A1*SBase)/40

YAT01A1 = 1/ZAT01A1

# Pot. trifásica na barra 9 

# Pot monofásica em retangular (MVA)
Scc1f = pol2ret(16942.0622, 86.1346)

#region ---- Montagem matriz YBarra Seq 0 -----
# Equivalente de rede na barra 9
Zg9t = 3*SBase/Scc1f
Zg9 = Zg9t.conjugate()
Zg0 = Zg9 - 2*ZEQ9
Yg0 = 1/Zg0


Z24_0_tmp = (LT01C1Z_0 + Z0m)/2
Y24_0 = -1/Z24_0_tmp

# Não entra o enrolamento do trafo pois está em Delta 
# Y de seq. zero
Y11_0 = Y0 + YS    # é Ys pois está em em Yg, em seq. 0 se mantém
Y22_0 = -Y24_0 + YAT01A1
Y33_0 = YT
Y44_0 = -Y24_0 + LT02C1Y_0 + LT02C2Y_0 + LT04C1Y_0
Y55_0 = TR02T1Y + LT05C1Y_0
Y66_0 = LT05C1Y_0
Y77_0 = TR03T1Y
Y88_0 = LT02C1Y_0 + LT02C2Y_0 + LT03C1Y_0
Y99_0 = LT03C1Y_0 + LT04C1Y_0 + Yg0
Y10_0 = -YS
Y30_0 = -YT

Y12_0 = Y13_0 = Y14_0 = Y15_0 = Y16_0 = Y17_0 = Y18_0 = Y19_0 = 0
Y21_0 = Y23_0 = Y25_0 = Y26_0 = Y27_0 = Y28_0 = Y29_0 = Y20_0 = 0
Y31_0 = Y32_0 = Y34_0 = Y35_0 = Y36_0 = Y37_0 = Y38_0 = Y39_0 = 0
Y41_0 = Y43_0 = Y45_0 = Y46_0 = Y47_0 = Y40_0 = 0
Y51_0 = Y52_0 = Y53_0 = Y54_0 = Y57_0 = Y58_0 = Y59_0 = Y50_0 = 0
Y61_0 = Y62_0 = Y63_0 = Y64_0 = Y67_0 = Y68_0 = Y69_0 = Y60_0 = 0
Y71_0 = Y72_0 = Y73_0 = Y74_0 = Y75_0 = Y76_0 = Y78_0 = Y79_0 = Y70_0 = 0
Y81_0 = Y82_0 = Y83_0 = Y85_0 = Y86_0 = Y87_0 = Y80_0 = 0
Y91_0 = Y92_0 = Y93_0 = Y95_0 = Y96_0 = Y97_0 = Y90_0 = 0

# Elementos da não diagonal principal precisam do negativo
Y42_0 = Y24_0
Y48_0 = Y84_0 = -LT02C1Y_0 - LT02C2Y_0
Y49_0 = Y94_0 = -LT04C1Y_0 
Y56_0 = Y65_0 = -LT05C1Y_0
Y89_0 = Y98_0 = -LT03C1Y_0

# Barra Virtual
Y00_0 = YP + YS + YT
Y02_0 = Y04_0 = Y05_0 = Y06_0 =  Y07_0 = Y08_0 =  Y09_0 = 0
Y01_0 = Y10_0
Y03_0 = Y30_0

YBarra_0 = np.array([Y11_0, Y12_0, Y13_0, Y14_0, Y15_0, Y16_0, Y17_0, Y18_0, Y19_0, Y10_0,
        Y21_0, Y22_0, Y23_0, Y24_0, Y25_0, Y26_0, Y27_0, Y28_0, Y29_0, Y20_0,
        Y31_0, Y32_0, Y33_0, Y34_0, Y35_0, Y36_0, Y37_0, Y38_0, Y39_0, Y30_0,
        Y41_0, Y42_0, Y43_0, Y44_0, Y45_0, Y46_0, Y47_0, Y48_0, Y49_0, Y40_0,
        Y51_0, Y52_0, Y53_0, Y54_0, Y55_0, Y56_0, Y57_0, Y58_0, Y59_0, Y50_0,
        Y61_0, Y62_0, Y63_0, Y64_0, Y65_0, Y66_0, Y67_0, Y68_0, Y69_0, Y60_0,
        Y71_0, Y72_0, Y73_0, Y74_0, Y75_0, Y76_0, Y77_0, Y78_0, Y79_0, Y70_0,
        Y81_0, Y82_0, Y83_0, Y84_0, Y85_0, Y86_0, Y87_0, Y88_0, Y89_0, Y80_0,
        Y91_0, Y92_0, Y93_0, Y94_0, Y95_0, Y96_0, Y97_0, Y98_0, Y99_0, Y90_0,
        Y01_0, Y02_0, Y03_0, Y04_0, Y05_0, Y06_0, Y07_0, Y08_0, Y09_0, Y00_0
        ])

# Modificando a matriz YBarra de seq 0 para calcular as correntes circunvizinhas
# Já que no Anafas a corrente se divide nas barras, portanto precisamos tirar
# Não entra o enrolamento do trafo pois está em Delta 
Z24_0_tmp = LT01C1Z_0 + Z0m
Y24_0 = -1/Z24_0_tmp
Y11_0 = Y0 + YS    # é Ys pois está em em Yg, em seq. 0 se mantém
Y22_0 = -Y24_0 + YAT01A1
Y33_0 = YT
Y44_0 = -Y24_0 + LT02C1Y_0 + LT02C2Y_0 + LT04C1Y_0
Y55_0 = TR02T1Y + LT05C1Y_0
Y66_0 = LT05C1Y_0
Y77_0 = TR03T1Y
Y88_0 = LT02C1Y_0 + LT02C2Y_0 + LT03C1Y_0
Y99_0 = LT03C1Y_0 + LT04C1Y_0 + Yg0
Y10_0 = -YS
Y30_0 = -YT

Y12_0 = Y13_0 = Y14_0 = Y15_0 = Y16_0 = Y17_0 = Y18_0 = Y19_0 = 0
Y21_0 = Y23_0 = Y25_0 = Y26_0 = Y27_0 = Y28_0 = Y29_0 = Y20_0 = 0
Y31_0 = Y32_0 = Y34_0 = Y35_0 = Y36_0 = Y37_0 = Y38_0 = Y39_0 = 0
Y41_0 = Y43_0 = Y45_0 = Y46_0 = Y47_0 = Y40_0 = 0
Y51_0 = Y52_0 = Y53_0 = Y54_0 = Y57_0 = Y58_0 = Y59_0 = Y50_0 = 0
Y61_0 = Y62_0 = Y63_0 = Y64_0 = Y67_0 = Y68_0 = Y69_0 = Y60_0 = 0
Y71_0 = Y72_0 = Y73_0 = Y74_0 = Y75_0 = Y76_0 = Y78_0 = Y79_0 = Y70_0 = 0
Y81_0 = Y82_0 = Y83_0 = Y85_0 = Y86_0 = Y87_0 = Y80_0 = 0
Y91_0 = Y92_0 = Y93_0 = Y95_0 = Y96_0 = Y97_0 = Y90_0 = 0

# Elementos da não diagonal principal precisam do negativo
Y42_0 = Y24_0
Y48_0 = Y84_0 = -LT02C2Y_0
Y49_0 = Y94_0 = -LT04C1Y_0 
Y56_0 = Y65_0 = -LT05C1Y_0
Y89_0 = Y98_0 = -LT03C1Y_0

# Barra Virtual
Y00_0 = YP + YS + YT
Y02_0 = Y04_0 = Y05_0 = Y06_0 =  Y07_0 = Y08_0 =  Y09_0 = 0
Y01_0 = Y10_0
Y03_0 = Y30_0

YBarra_0_mod = np.array([Y11_0, Y12_0, Y13_0, Y14_0, Y15_0, Y16_0, Y17_0, Y18_0, Y19_0, Y10_0,
        Y21_0, Y22_0, Y23_0, Y24_0, Y25_0, Y26_0, Y27_0, Y28_0, Y29_0, Y20_0,
        Y31_0, Y32_0, Y33_0, Y34_0, Y35_0, Y36_0, Y37_0, Y38_0, Y39_0, Y30_0,
        Y41_0, Y42_0, Y43_0, Y44_0, Y45_0, Y46_0, Y47_0, Y48_0, Y49_0, Y40_0,
        Y51_0, Y52_0, Y53_0, Y54_0, Y55_0, Y56_0, Y57_0, Y58_0, Y59_0, Y50_0,
        Y61_0, Y62_0, Y63_0, Y64_0, Y65_0, Y66_0, Y67_0, Y68_0, Y69_0, Y60_0,
        Y71_0, Y72_0, Y73_0, Y74_0, Y75_0, Y76_0, Y77_0, Y78_0, Y79_0, Y70_0,
        Y81_0, Y82_0, Y83_0, Y84_0, Y85_0, Y86_0, Y87_0, Y88_0, Y89_0, Y80_0,
        Y91_0, Y92_0, Y93_0, Y94_0, Y95_0, Y96_0, Y97_0, Y98_0, Y99_0, Y90_0,
        Y01_0, Y02_0, Y03_0, Y04_0, Y05_0, Y06_0, Y07_0, Y08_0, Y09_0, Y00_0
        ])

YBarra_0_mod = YBarra_0_mod.reshape(10,10)
YBarra_0 = YBarra_0.reshape(10,10)
ZBarra_0 = np.linalg.inv(YBarra_0)
Ybdf = pd.DataFrame(YBarra_0)
Zbdf = pd.DataFrame(ZBarra_0)
#endregion

# Queremos individualmente para calcular as tensões pos falta
If = np.zeros(10, dtype=complex)

# Resultante (soma dos 3)
If_3 = np.zeros(10, dtype=complex)

Vpos_positiva = np.zeros(10, dtype=complex)
Vpos_neg = np.zeros(10, dtype=complex)
Vpos_0 = np.zeros(10, dtype=complex)

# Vetor que contém as defasagens para as tensões de pós-falta, colocando as barras em relação a barra de falta, neste caso, 4.
Vdefasagem = np.zeros(10, dtype=complex)
Vdefasagem[1] = defasagem30GrausNeg
Vdefasagem[2] = defasagem0Grau
Vdefasagem[3] = defasagem30GrausNeg
Vdefasagem[4] = defasagem0Grau
Vdefasagem[5] = defasagem30GrausNeg
Vdefasagem[6] = defasagem30GrausNeg
Vdefasagem[7] = defasagem120GrausNeg
Vdefasagem[8] = defasagem0Grau
Vdefasagem[9] = defasagem0Grau

Vdefasagem_oposto = np.zeros(10, dtype=complex)
Vdefasagem_oposto[1] = defasagem30GrausPos
Vdefasagem_oposto[2] = defasagem0Grau
Vdefasagem_oposto[3] = defasagem30GrausPos
Vdefasagem_oposto[4] = defasagem0Grau
Vdefasagem_oposto[5] = defasagem30GrausPos
Vdefasagem_oposto[6] = defasagem30GrausPos
Vdefasagem_oposto[7] = defasagem120GrausPos
Vdefasagem_oposto[8] = defasagem0Grau
Vdefasagem_oposto[9] = defasagem0Grau


# barraOndeOcorreuAFalta = [4, 5, 2]
faltaBarra4 = [4]
faltaBarra5 = [5]
faltaBarra2 = [2]


tensoesDeFaseABC = []

# Vetor que guarda as tensões de fase A, B e C, usado para exportar e colocar no relatório depois.
Vetf = np.zeros(30, dtype=tuple)
Vetf = Vetf.reshape(3,10)

# Correntes circunvizinhas de seq. positiva, neg e 0
Ic_positivo = np.zeros(10, dtype=complex)
Ic_neg = np.zeros(10, dtype=complex)
Ic_0 = np.zeros(10, dtype=complex)

# Matriz para guardar as correntes circunvizinhas de fase A, B e C
Ivetpf = np.zeros(30, dtype=tuple)  # Coloquei como tuple para guardar os dados já convertidos em polar
Ivetpf = Ivetpf.reshape(3,10)

# Calcular as tensoes de pós-falta em sequencia +, - e 0 em TODAS as barras
for k in faltaBarra4:
    # Colocando em termos do Anafas
    # Quando for falta na barra 5, a defasagem é de 0 em relaçã o a barra 5 (da 1 pra 5)
    # Quando for na barra 4, 30 graus positivos

    print(f'\n\n\n------------ Falta na Barra {k} ------------')

    If[k] = (VpreF[k])*defasagem30GrausPos / (ZBarra_positivo[k-1,k-1] + ZBarra_neg[k-1,k-1] + ZBarra_0[k-1,k-1] + 3*Zf[k])
    If_3[k] = (3*VpreF[k])*defasagem30GrausPos / (ZBarra_positivo[k-1,k-1] + ZBarra_neg[k-1,k-1] + ZBarra_0[k-1,k-1] + 3*Zf[k])

    # TODO: Calcular corrente de falta por FASE (A,B e C)

    print(f'Corrente de Falta na barra {k}: {ret2pol(If[k])}')
    # 9 Barras
    for n in range(1,10):

        print(f'Z{n}, {k-1}: {ZBarra_0[n-1,k-1]}')
        # Tensao pos falta na barra de falta (4)
        # n-1 pois a matriz Zbarra possui dimensão 10 devido ao barra virtual
        Vpos_positiva[n] = (VpreF[n]*defasagem30GrausPos - ZBarra_positivo[n-1,k-1]*If[k])*Vdefasagem[n]
        Vpos_neg[n] = -(ZBarra_neg[n-1,k-1]*If[k])*Vdefasagem_oposto[n]
        Vpos_0[n] = -ZBarra_0[n-1,k-1]*If[k]

        print(f"\n\n---- Tensão pós falta na barra {n} ----")
        print(f'Tensão Pos Falta Positiva: {ret2pol(Vpos_positiva[n])}')
        print(f'Tensão Pos Falta Negativa: {ret2pol(Vpos_neg[n])}')
        print(f'Tensão Pos Falta Zero: {ret2pol(Vpos_0[n])}')

        # Guardando valores para dar output nas tensoes de barra de fase A, B e C
        vetSeq = np.array([[Vpos_0[n], Vpos_positiva[n], Vpos_neg[n]]])
        vetSeq = vetSeq.transpose()

        # Vph: tensões nas fases A, B e C
        Vph = np.dot(A,vetSeq)
        # Loop auxiliar para guardar os valores de forma correta na matriz das tensões de fase A, B e C
        for m in range(0,3):
            Vetf[m,n] = ret2pol(Vph[m])
    
    # Números das barras adjacentes para calcular as correntes circunvizinhas; nested de acordo com a barra de falta
    for h in [2,5,8,9]:
        #print(f"\nVpos {h} {ret2pol(Vpos_positiva[h])}")
        #print(f"Vpos {k} {ret2pol(Vpos_positiva[k])}")
        #print(f"ZBarra {k} {ret2pol(Vpos_positiva[k])}")

        Ic_positivo[h] = (Vpos_positiva[h]*Vdefasagem_oposto[h] - Vpos_positiva[k])*(-YBarra_positivo[h-1,k-1])
        Ic_neg[h] = (Vpos_neg[h]*Vdefasagem[h]-Vpos_neg[k])*(-YBarra_neg[h-1,k-1])
        Ic_0[h] = (Vpos_0[h]-Vpos_0[k])*(-YBarra_0_mod[h-1,k-1])
        print(f'\nCorrente Circunvizinha Positiva: {k}-{h}:\n{ret2pol(Ic_positivo[h])}')
        print(f'\nCorrente Circunvizinha Negativa: {k}-{h}:\n{ret2pol(Ic_neg[h])}')
        print(f'\nCorrente Circunvizinha 0: {k}-{h}:\n{ret2pol(Ic_0[h])}')
        ISeq = np.array([[Ic_0[h], Ic_positivo[h], Ic_neg[h]]])
        ISeq = ISeq.transpose()
        Iph = np.dot(A,ISeq)
        # Loop auxiliar para guardar os valores de forma correta na matriz das correntes circunvizinhas de fase A, B e C
        for g in range(0,3):
            Ivetpf[g,h] = ret2pol(Iph[g])

    matCorrenteCircunvizinhasABC = pd.DataFrame(Ivetpf)
    matTensaoPosFaltaABC = pd.DataFrame(Vetf)
    print(matCorrenteCircunvizinhasABC)





# ------------ Letra b, Falta Bifásica ------------------

Vdefasagem_b = np.zeros(10, dtype=complex)
Vdefasagem_b[1] = defasagem0Grau
Vdefasagem_b[2] = defasagem30GrausPos
Vdefasagem_b[3] = defasagem0Grau
Vdefasagem_b[4] = defasagem30GrausPos
Vdefasagem_b[5] = defasagem0Grau
Vdefasagem_b[6] = defasagem0Grau
Vdefasagem_b[7] = defasagem90GrausNeg
Vdefasagem_b[8] = defasagem30GrausPos
Vdefasagem_b[9] = defasagem30GrausPos


Vdefasagem_b_oposto = np.zeros(10, dtype=complex)
Vdefasagem_b_oposto[1] = defasagem0Grau
Vdefasagem_b_oposto[2] = defasagem30GrausNeg
Vdefasagem_b_oposto[3] = defasagem0Grau
Vdefasagem_b_oposto[4] = defasagem30GrausNeg
Vdefasagem_b_oposto[5] = defasagem0Grau
Vdefasagem_b_oposto[6] = defasagem0Grau
Vdefasagem_b_oposto[7] = defasagem90GrausPos
Vdefasagem_b_oposto[8] = defasagem30GrausNeg
Vdefasagem_b_oposto[9] = defasagem30GrausNeg

# Matriz para guardar as correntes de falta de fase A, B e C
If_ph = np.zeros(3, dtype=tuple)
#If_ph = If_ph.reshape(3,1)

# Letra b, falta bifásica na barra 5
for k in faltaBarra5:
    print(f'\n\n\n------------ Falta na Barra {k} ------------')
    
    # Quando a falta é bifasica, a corrente de falta de seq é 0
    If_positivo = (VpreF[k]) / (ZBarra_positivo[k-1,k-1] + ZBarra_neg[k-1,k-1] + Zf[k])
    # IMPORTANTE: deixamos igual ao If_positivo pois somente assim os ângulos dos dois serão iguais!
    If_neg = -(VpreF[k]) / (ZBarra_positivo[k-1,k-1] + ZBarra_neg[k-1,k-1] + Zf[k])
    If_0 = 0 + 0j
    # Corrente de falta de sequencia
    IfSeq = np.array([[If_0, If_positivo, If_neg]])
    IfSeq = IfSeq.transpose()

    # Corrente de falta por fase (A, B e C)
    # TODO: FIZEMOS O CALCULO NA MAO E POR ALGUMA RAZAO NP.DOT, @ UO MATMUL NAO ESTÃO RETORNANDO OS VALORES
    # TODO CORRETOS, JÁ VERIFICAMOS NA MÃO. POR ENQUNATO IGNORAMOS ESTE RESULTADO
    # TODO: DEIXAMOS NO FINAL COM O MENOS NA FRENTE DO If_neg, JÁ QUE NÃO É POSSÍVEL DEIXAR UM MÓDULO DE UM NUMERO
    # TODO: DE FORMA NEGATIVA, COLOCANDO O SINAL, OS VALORES BATERAM, MAS A ORDEM DE If_ph ESTÁ ERRADA
    Ifph = A @ IfSeq
    #Ifph = np.dot(A,IfSeq)
    #Ifph = np.matmul(A,IfSeq)

    for g in range(0,3):
        If_ph[g] = ret2pol(Ifph[g])
    # forçamos o resultado da fase que "sobrou" da falta para ser 0, por isso os resultados são iguais da B e C.
    If_ph[0] = 0

    for n in range(1,10):
        # Não tem defasagem neste pois é em relação a barra 5, a mesma coisa.
        Vpos_positiva[n] = (VpreF[n] - ZBarra_positivo[n-1,k-1]*If_positivo)*Vdefasagem_b[n]
        Vpos_neg[n] = -(ZBarra_neg[n-1,k-1]*If_neg)*Vdefasagem_b_oposto[n]
        Vpos_0[n] = -ZBarra_0[n-1,k-1]*If_0

        print(f"\n\n---- Tensão pós falta na barra {n} ----")
        print(f'Tensão Pos Falta Positiva: {ret2pol(Vpos_positiva[n])}')
        print(f'Tensão Pos Falta Negativa: {ret2pol(Vpos_neg[n])}')
        print(f'Tensão Pos Falta Zero: {ret2pol(Vpos_0[n])}')

        # Guardando valores para dar output nas tensoes de barra de fase A, B e C
        vetSeq = np.array([[Vpos_0[n], Vpos_positiva[n], Vpos_neg[n]]])
        vetSeq = vetSeq.transpose()

        # Vph: tensões nas fases A, B e C
        Vph = np.dot(A,vetSeq)
        # Loop auxiliar para guardar os valores de forma correta na matriz das tensões de fase A, B e C
        for m in range(0,3):
            Vetf[m,n] = ret2pol(Vph[m])
        

    for h in [4,6]:

        # Oposto aqui pois precisamos desfazer a defasagem que demos inicialmente
        Ic_positivo[h] = (Vpos_positiva[h]*Vdefasagem_b_oposto[h] - Vpos_positiva[k])*(-YBarra_positivo[h-1,k-1])
        Ic_neg[h] = (Vpos_neg[h]*Vdefasagem_b[h]-Vpos_neg[k])*(-YBarra_neg[h-1,k-1])
        Ic_0[h] = (Vpos_0[h]-Vpos_0[k])*(-YBarra_0_mod[h-1,k-1])
        
        print(f'\nCorrente Circunvizinha Positiva: {k}-{h}:\n{ret2pol(Ic_positivo[h])}')
        print(f'\nCorrente Circunvizinha Negativa: {k}-{h}:\n{ret2pol(Ic_neg[h])}')
        print(f'\nCorrente Circunvizinha 0: {k}-{h}:\n{ret2pol(Ic_0[h])}')
        ISeq = np.array([[Ic_0[h], Ic_positivo[h], Ic_neg[h]]])
        ISeq = ISeq.transpose()
        Iph = np.dot(A,ISeq)
        # Loop auxiliar para guardar os valores de forma correta na matriz das correntes circunvizinhas de fase A, B e C
        for g in range(0,3):
            Ivetpf[g,h] = ret2pol(Iph[g])
    
    matCorrenteCircunvizinhasABC = pd.DataFrame(Ivetpf)
    matTensaoPosFaltaABC = pd.DataFrame(Vetf)
    #matTensaoPosFaltaABC.to_csv(r'.csv', index=False)
    matCorrenteCircunvizinhasABC.to_csv(r'CorrentesCircunvizinhas.csv', index=False)
#print(f"Correntes de falta por fase: A, B e C: {If_ph}")
#print(f'Corrente positiva de Falta na barra {k}: {ret2pol(If_positivo)}')
# Justamente pelo fato do Anafas mostrar o If_negativo com módulo negativo, "forçamos" o resultado ser negativo
#print(f'Corrente negativa de Falta na barra {k}: -{ret2pol(If_neg)}')
#print(f'Corrente zero de Falta na barra {k}: {ret2pol(0+0j)}')


# -------- Letra C, Falta na Barra 2 ---------

# Vetor que contém as defasagens para as tensões de pós-falta, colocando as barras em relação a barra de falta, neste caso, barra 2.
# APROVEITAMOS O Vdefasagem da primeira questão pois não há nenhum trafo a mais, igual a barra 4, em referência a barra 1, portanto segue a mesma regra


for k in faltaBarra2:
    print(f'\n\n\n------------ Falta na Barra {k} ------------')
    
    If_positivo = (VpreF[k])*defasagem30GrausPos / (ZBarra_positivo[k-1,k-1] + ( ZBarra_neg[k-1,k-1] * (ZBarra_0[k-1,k-1] + 3*Zf[k]) ) / (ZBarra_neg[k-1,k-1] + ZBarra_0[k-1,k-1] + 3*Zf[k]) )
    If_neg = -( If_positivo * (ZBarra_0[k-1,k-1] + 3*Zf[k]) / (ZBarra_neg[k-1,k-1] + ZBarra_0[k-1,k-1] + 3*Zf[k]) )
    If_0 = -( If_positivo * (ZBarra_neg[k-1,k-1]) / (ZBarra_neg[k-1,k-1] + ZBarra_0[k-1,k-1] + 3*Zf[k]) )

    # Corrente de falta de sequencia
    IfSeq = np.array([[If_0, If_positivo, If_neg]])
    IfSeq = IfSeq.transpose()

    # Corrente de falta por fase (A, B e C)
    Ifph = A @ IfSeq
    #Ifph = np.dot(A,IfSeq)
    #Ifph = np.matmul(A,IfSeq)

    for g in range(0,3):
        If_ph[g] = ret2pol(Ifph[g])

    for n in range(1,10):
        # Não tem defasagem neste pois é em relação a barra 5, a mesma coisa.
        Vpos_positiva[n] = (VpreF[n]*defasagem30GrausPos - ZBarra_positivo[n-1,k-1]*If_positivo)*Vdefasagem[n]
        Vpos_neg[n] = -(ZBarra_neg[n-1,k-1]*If_neg)*Vdefasagem_oposto[n]
        Vpos_0[n] = -ZBarra_0[n-1,k-1]*If_0

        print(f"\n\n---- Tensão pós falta na barra {n} ----")
        print(f'Tensão Pos Falta Positiva: {ret2pol(Vpos_positiva[n])}')
        print(f'Tensão Pos Falta Negativa: {ret2pol(Vpos_neg[n])}')
        print(f'Tensão Pos Falta Zero: {ret2pol(Vpos_0[n])}')

        # Guardando valores para dar output nas tensoes de barra de fase A, B e C
        vetSeq = np.array([[Vpos_0[n], Vpos_positiva[n], Vpos_neg[n]]])
        vetSeq = vetSeq.transpose()

        # Vph: tensões nas fases A, B e C
        Vph = np.dot(A,vetSeq)
        # Loop auxiliar para guardar os valores de forma correta na matriz das tensões de fase A, B e C
        for m in range(0,3):
            Vetf[m,n] = ret2pol(Vph[m])
        
    # Barras adjacentes
    for h in [4,0]:

        # Oposto aqui pois precisamos desfazer a defasagem que demos inicialmente
        Ic_positivo[h] = (Vpos_positiva[h]*Vdefasagem_oposto[h] - Vpos_positiva[k])*(-YBarra_positivo[h-1,k-1])
        Ic_neg[h] = (Vpos_neg[h]*Vdefasagem[h]-Vpos_neg[k])*(-YBarra_neg[h-1,k-1])
        Ic_0[h] = (Vpos_0[h]-Vpos_0[k])*(-YBarra_0_mod[h-1,k-1])
        
        print(f'\nCorrente Circunvizinha Positiva: {k}-{h}:\n{ret2pol(Ic_positivo[h])}')
        print(f'\nCorrente Circunvizinha Negativa: {k}-{h}:\n{ret2pol(Ic_neg[h])}')
        print(f'\nCorrente Circunvizinha 0: {k}-{h}:\n{ret2pol(Ic_0[h])}')
        ISeq = np.array([[Ic_0[h], Ic_positivo[h], Ic_neg[h]]])
        ISeq = ISeq.transpose()
        Iph = np.dot(A,ISeq)
        # Loop auxiliar para guardar os valores de forma correta na matriz das correntes circunvizinhas de fase A, B e C
        for g in range(0,3):
            Ivetpf[g,h] = ret2pol(Iph[g])
    
    matCorrentesDeFaltaDeFase = pd.DataFrame(If_ph)
    matCorrenteCircunvizinhasABC = pd.DataFrame(Ivetpf)
    matTensaoPosFaltaABC = pd.DataFrame(Vetf)
    #matCorrenteCircunvizinhasABC.to_csv(r'CorrentesCircunvizinhas.csv', index=False)
    matTensaoPosFaltaABC.to_csv(r'TensaoPosFaltaABC.csv', index=False)
    #matCorrenteCircunvizinhasABC.to_csv(r'CorrentesCircunvizinhas.csv', index=False)


compararComAnafas = False

if compararComAnafas:
    print("Valores para comparar com o Anafas")
    print(f"LT01C1Z: {LT01C1Z_0*100}")
    print(LT01C2Z_0*100)
    print(LT02C1Z_0*100)
    print(LT02C2Z_0*100)
    print(LT03C1Z_0*100)
    print(LT04C1Z_0*100)
    print(LT05C1Z_0*100)
    print(f"Zg0: {Zg0*100}")
    print(f'Z0: {Z0*100}')
    print(f'ZP: {ZP*100}')
    print(f'ZS: {ZS*100}')
    print(f'ZT: {ZT*100}')
    print(f'ZAT01A1: {ZAT01A1*100}')
    print("ZBarra de Sequência 0:\n")
    print(Zbdf)
    print(100*Zbdf)
    print("Tensoes de Fase ABC:")
    for column in matTensaoPosFaltaABC:
        print(matTensaoPosFaltaABC[column])

