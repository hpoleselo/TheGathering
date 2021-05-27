from copy import deepcopy, copy
from math import pi, sin, cos, sqrt
import pandas as pd
import numpy as np

compararComAnafas = True

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


ZBarra_positivo = np.genfromtxt('zbarra.csv', dtype=complex, delimiter=',')
ZBarra_neg = deepcopy(ZBarra_positivo)

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

"""
    Calcular as tensoes de pós-falta em sequencia +, - e 0 em TODAS as barras
    Sabendo que as faltas ocorrem:
    - a) Falta Monofásica na barra 4 (SE - 345kV),          ZfA = 1.673
    - b) Falta Bifásica na barra 5 (SE - 138kV),            ZfB = 2.033
    - c) Falta Bifásica À TERRA na barra 2 (SE - 345kV),    ZfC = 0.328

    Va_0_pos : tensão de pós-falta em sequencia 0
    Va_1_pos : tensão de pós-falta em sequencia +
    Va_2_pos : tensão de pós-falta em sequencia -

    Va = Va_2_pos + Va_1_pos + Va_0_pos
"""

ZfA = 1.673
ZfB = 2.033
ZfC = 0.328

ZB1 = 1.9044000000000003
ZB2 = 1190.25
ZB3 = 0.17305600000000002
ZB4 = 190.44
ZB5 = 1.9044000000000003

# -- Impedância de Falta em PU --
Zf = np.zeros(8)
# Para Letra A, usa-se a ZB2
Zf[4] = ZfA/ZB2
# Para Letra B, usa-se a ZB4 TODO: CONFIRMAR CARALHO!
Zf[5] = ZfB/ZB4
# Para Letra C, usa-se a ZB2
Zf[2] = ZfC/ZB2


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
A_df = pd.DataFrame(A)
#print(A_df)
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

tmp1 = (9.15+(NA/100))
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


Z0 = pol2ret(0.19252,87.84669)
Y0 = 1/Z0

# Impedância Mutua para seq. 0
Z0m = ((0.05213 + 0.58234j) * (300+NA))/ZBase2

# Impedância do Trafo. de Aterramento
tmp = 6.385+NA/100
ZAT01A1 = pol2ret(tmp,90)

# Pot de base no valor que ZAT101A1 foi calculado
ZAT01A1 = (ZAT01A1*SBase)/40

YAT01A1 = 1/ZAT01A1

# Pot. trifásica na barra 9 

# Pot monofásica em retangular (MVA)
Scc1f = pol2ret(16942.0622, 86.1346)
Scc1f = Scc1f/100 # pu

# Equivalente de rede na barra 9
Zg9 = 3*SBase/Scc1f

Zg0 = Zg9 - 2*ZEQ9
Yg0 = 1/Zg0


Z24_0_tmp = (LT01C1Z_0 + Z0m)/2
Y24_0 = 1/Z24_0_tmp

# Não entra o enrolamento do trafo pois está em Delta 
# Y de seq. zero
Y11_0 = Y0 + YS    # é Ys pois está em em Yg, em seq. 0 se mantém
Y22_0 = Y24_0 + YAT01A1
Y33_0 = YT
Y44_0 = Y24_0 + LT02C1Y_0 + LT02C2Y_0 + LT04C1Y_0
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
Y42_0 = -Y24_0
Y48_0 = Y84_0 = -LT02C1Y_0 - LT02C2Y_0
Y49_0 = Y94_0 = -LT04C1Y_0 - LT03C1Y_0 - Yg0
Y56_0 = Y65_0 = -LT05C1Y_0
Y89_0 = Y98_0 = -LT03C1Y_0

# Barra Virtual
Y02_0 = Y04_0 = Y05_0 = Y06_0 =  Y07_0 = Y08_0 =  Y09_0 = Y00_0 = 0
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

YBarra_0 = YBarra_0.reshape(10,10)
ZBarra_0 = np.linalg.inv(YBarra_0)
Ybdf = pd.DataFrame(YBarra_0)
Zbdf = pd.DataFrame(ZBarra_0)
print("Zé Barra Sequência de Toma Toma 0:\n")
print(Ybdf)
print(Zbdf)



If = np.zeros(10, dtype=complex)
# barraOndeOcorreuAFalta = [4, 5, 2]
barraOndeOcorreuAFalta = [4]

# Calcular as tensoes de pós-falta em sequencia +, - e 0 em TODAS as barras
for k in barraOndeOcorreuAFalta:

    print(f'\n\n\n------------ Falta na Barra {k} ------------')

    If[k] = (3*VpreF[k]) / (ZBarra_positivo[k-1,k-1] + ZBarra_neg[k-1,k-1] + ZBarra_0[k-1,k-1])
    

if compararComAnafas:
    print("Valores para comparar com o Anafas")
    print(LT01C1Z_0*100)
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
    print(f'Corrente de Falta na barra 4: {ret2pol(If[4])}')



