import numpy as np
import pandas as pd

NA = 6
VBase1 = 13.8
VBase2 = 345
VBase3 = 4.16
VBase4 = 138
VBase5 = 13.8
SBase = 100

def ret2pol(x, y):
    modulo = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return(modulo, theta)

def pol2ret(modulo, theta):
    x = modulo * np.cos(theta)
    y = modulo * np.sin(theta)
    return(x, y)

def calcImpedanciaDeBase():
    ZBase1 = ((VBase1**2)/SBase)
    ZBase2 = ((VBase2**2)/SBase)
    ZBase3 = ((VBase3**2)/SBase)
    ZBase4 = ((VBase4**2)/SBase)
    ZBase5 = ((VBase5**2)/SBase)
    print(f"Impedâncias de Base: ZB1, {ZBase1}, ZB2:{ZBase2}, ZB3: {ZBase3}, ZB4:{ZBase4}, ZB5:{ZBase5}")
    return ZBase1, ZBase2, ZBase3, ZBase4

def calcLinhaTransmissao(ZBase2, ZBase4):
    """ Calcula a impedância e admitância da linha de transmissão. """
    LT01C1Z1 = ((0.01785+0.19679j)*(300+NA))/ZBase2
    LT01C2Z1 = ((0.01785+0.19679j)*(300+NA))/ZBase2
    LT02C1Z1 = ((0.01547+0.17219j)*(350+NA))/ZBase2
    LT02C2Z1 = ((0.01547+0.17219j)*(350+NA))/ZBase2
    LT03C1Z1 = ((0.03134+0.33248j)*(200+NA))/ZBase2
    LT04C1Z1 = ((0.01252+0.15740j)*(550+NA))/ZBase2
    LT05C1Z1 = ((0.04380+0.53196j)*(30+(NA/10)))/ZBase4
    print("\n")
    print(f"Impedância da Linha de transmissão: \n{LT01C1Z1}, \n{LT01C2Z1} \n{LT02C1Z1} \n{LT02C2Z1} \n{LT03C1Z1} \n{LT04C1Z1} \n{LT05C1Z1}")
    return LT01C1Z1, LT01C2Z1, LT02C1Z1, LT02C2Z1, LT03C1Z1, LT04C1Z1, LT05C1Z1

def calcImpedanciaPorFase():
    # Divindo por 100 para tirar a porçentagem
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

    print("\n")
    print(f"Impedância por fase:\n{ZP} \b{ZS} \n{ZT}")
    return ZP, ZS, ZT

def construirMatrizAdmitancia(TR02T1Z1, TR03T1Z1, LT01C1Z1, LT01C2Z1, LT02C1Z1, LT02C2Z1, LT03C1Z1, LT04C1Z1, LT05C1Z1, ZEQ1, ZEQ9, ZP, ZS, ZT):
    
    # Preparando valores
    LT01C1Y1 = 1/LT01C1Z1
    LT01C2Y1 = 1/LT01C2Z1
    LT02C1Y1 = 1/LT02C1Z1
    LT02C2Y1 = 1/LT02C2Z1
    LT03C1Y1 = 1/LT03C1Z1
    LT04C1Y1 = 1/LT04C1Z1
    LT05C1Y1 = 1/LT05C1Z1

    YEQ1 = 1/ZEQ1
    YEQ9 = 1/ZEQ9
    YP = 1/ZP
    YS = 1/ZS
    YT = 1/ZT

    TR02T1Y1 = 1/TR02T1Z1
    TR03T1Y1 = 1/TR03T1Z1

    # Construindo elementos da Matriz Y
    Y11 = YEQ1 + YS
    Y22 = YP + LT01C1Y1 + LT01C2Y1
    Y33 = YT
    Y44 = TR02T1Y1 + LT01C1Y1 + LT02C1Y1 + LT01C2Y1 + LT02C2Y1 + LT04C1Y1
    Y55 = TR02T1Y1+LT05C1Y1
    Y66 = LT05C1Y1+TR03T1Y1
    Y77 = TR03T1Y1
    Y88 = LT02C1Y1+LT02C2Y1+LT03C1Y1
    Y99 = LT03C1Y1+LT04C1Y1+YEQ9
    Y00 = YP+YS+YT

    Y12 = Y13 = Y14 = Y15 = Y16 = Y17 = Y18 = Y19 = 0
    Y10 = -YS
    Y20 = -YP
    Y21 = Y12
    Y24 = -LT01C1Y1-LT01C2Y1
    Y23 = Y25 = Y26 = Y27 = Y28 = Y29 = 0
    Y31=  Y13
    Y32 = Y23
    Y34 = Y35 = Y36 = Y37 = Y38 = Y39 = 0
    Y30 = -YT
    Y41 = Y14
    Y42 = Y24
    Y43 = Y34
    Y45 = -TR02T1Y1
    Y46 = Y47 = Y40 = 0
    Y48 = -LT02C1Y1 - LT02C2Y1
    Y49 = -LT04C1Y1
    Y51 = Y15
    Y52 = Y25
    Y53 = Y35
    Y54 = Y45
    Y56 = -LT05C1Y1
    Y57 = Y58 = Y59 = Y50 = 0
    Y61 = Y16
    Y62 = Y26
    Y63 = Y36
    Y64 = Y46
    Y65 = Y56
    Y67 = -TR03T1Y1
    Y68 = Y69 = Y60 = 0
    Y71 = Y17
    Y72 = Y27
    Y73 = Y37
    Y74 = Y47
    Y75 = Y57
    Y76 = Y67
    Y78 = Y79 = Y70 = 0
    Y81 = Y18
    Y82 = Y28
    Y83 = Y38
    Y84 = Y48
    Y85 = Y58
    Y86 = Y68
    Y87 = Y78
    Y89 = -LT03C1Y1
    Y80 = 0
    Y91 = Y19
    Y92 = Y29
    Y93 = Y39
    Y94 = Y49
    Y95 = Y59
    Y96 = Y69
    Y97 = Y79
    Y98 = Y89
    Y90 = 0
    Y01 = Y10
    Y02 = Y20
    Y03 = Y30
    Y04 = Y40
    Y05 = Y50
    Y06 = Y60
    Y07 = Y70
    Y08 = Y80
    Y09 = Y90

    vetor = np.array([Y11, Y12, Y13, Y14, Y15, Y16, Y17, Y18, Y19, Y10,
    Y21, Y22, Y23, Y24, Y25, Y26, Y27, Y28, Y29, Y20,
    Y31, Y32, Y33, Y34, Y35, Y36, Y37, Y38, Y39, Y30,
    Y41, Y42, Y43, Y44, Y45, Y46, Y47, Y48, Y49, Y40,
    Y51, Y52, Y53, Y54, Y55, Y56, Y57, Y58, Y59, Y50,
    Y61, Y62, Y63, Y64, Y65, Y66, Y67, Y68, Y69, Y60,
    Y71, Y72, Y73, Y74, Y75, Y76, Y77, Y78, Y79, Y70,
    Y81, Y82, Y83, Y84, Y85, Y86, Y87, Y88, Y89, Y80,
    Y91, Y92, Y93, Y94, Y95, Y96, Y97, Y98, Y99, Y90,
    Y01, Y02, Y03, Y04, Y05, Y06, Y07, Y08, Y09, Y00
    ])

    YBarra = vetor.reshape(10,10)
    ZBarra = np.linalg.inv(YBarra)
    return YBarra, ZBarra

def main():

    ZBase1, ZBase2, ZBase3, ZBase4 = calcImpedanciaDeBase()
    LT01C1Z1, LT01C2Z1, LT02C1Z1, LT02C2Z1, LT03C1Z1, LT04C1Z1, LT05C1Z1 = calcLinhaTransmissao(ZBase2, ZBase4)
    ZP, ZS, ZT = calcImpedanciaPorFase()

    # Potencia 
    Scc3f = (1564.1935+29720.5403j)

    # Equivalentes de Rede:
    ZEQ1 = (0.0048+0.0569j) * (((13.8/VBase1)**2)*(SBase/100))
    _ZEQ9 = ((abs((1)**2)) *SBase) / (Scc3f)
    ZEQ9 = _ZEQ9.conjugate()

    # Mudança de Base
    # TODO: definir nome correto de tmp1
    tmp1 = (9.15+(NA/100))
    tmp1 = complex(0,tmp1)
    TR02T1Z1 = (tmp1/100)*(SBase/75)

    tmp2 = (8.33+(NA/100))
    tmp2 = complex(0, tmp2)
    TR03T1Z1 = (tmp2/100)*(SBase/50)
    
    YBarra, ZBarra = construirMatrizAdmitancia(
        TR02T1Z1, TR03T1Z1,
         LT01C1Z1, LT01C2Z1, LT02C1Z1, LT02C2Z1, LT03C1Z1, LT04C1Z1, LT05C1Z1,
         ZEQ1, ZEQ9, ZP, ZS, ZT
        )

    # Convertendo para DataFrame para exportar como CSV
    df_zbarra = pd.DataFrame(ZBarra)
    df_ybarra = pd.DataFrame(YBarra)
    # TODO: Exportar sem index
    #df_zbarra.to_csv(r'zbarra.csv')
    df_ybarra.to_csv(r'ybarra.csv')

main()

