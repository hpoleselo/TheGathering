from math import sqrt
import numpy as np

""" Programa para o Trabalho sobre Ensaio de Motor de Indução Trifásico.
    Docente: Eudemario
    Discentes: Ana Beatriz e Henrique Poleselo
    Código feito em 07.07.2021 """

def calculoDosParametrosDoMIT(R, classe):
    """ Função que calcula os parâmetros do do Motor de Indução Trifásico dado os ensaios
    a vazio, rotor bloqueado e da medição de corrente contínua da resistência do estator.
    
    Essa função é apenas auxiliar de forma a receber o parâmetro R de forma a facilitar o
    cálculo de forma repetida para diferentes classes já que o R está relacionado de forma aproximada
    entre a classe do motor, a reatância do estator e a reatância do rotor referida ao estator.

    A mesma retorna os parâmetros do MIT (Rs, Xls, Xlrl, Rrl e Xm ) printados na tela do terminal.
    """

    print(f"----- Utilizando classe {classe} e valor de R de {round(R,3)} para o cálculo dos parâmetros -----")
    vf = 440    # V, tensão de linha
    fe = 60     # Hz
    torque = 94 # hp

    # ------- Dados Obtidos no Ensaio -------
    # Rs, o valor que foi medido vai ser dividido por 2, pois Rs = Rmed/2; E POR FASE
    #Rmedido = 0.03
    Rs = 0.03
    #Rs = Rmedido/2

    # ------- A Vazio -------
    # Lembrando que esses valores medidos são de linha, por isso passamos para fase pois
    # O modelo equivalente do circuito é monofásico.
    Vvazio = vf
    # Tensão por fase já que o modelo é monofásico
    Vvazio = Vvazio/sqrt(3)

    Ivazio = 32.6  # Amperes, corrente nominal

    Pvazio = 1200  # Watts, potência trifásica 
    #Pvazio = Pvazio/3

    # ------- A Rotor Bloqueado -------
    Vbloq = 40.5
    # Tensão por fase
    Vbloq = Vbloq/sqrt(3) 
    Ibloq = 162.7
    Pbloq = 4200
    # Frequência 25% da nominal para que o motor opere com s=1
    Fbloq = 15

    # -------- Cálculo dos Parâmetros a Vazio -------
    Zvazio = Vvazio/Ivazio
    Rvazio = Pvazio/(3*Ivazio**2)
    Xvazio = sqrt(Zvazio**2 - Rvazio**2)

    # * Outra forma de calcular o Xvazio
    """
    PotPerdasRotacionais = Pvazio - 3*Rs*(Ivazio**2) # inclui as perdas magneticas no nucleo
    Svazio = sqrt(3)*Vvazio*Ivazio
    Qvazio = sqrt(Svazio**2 - Pvazio**2)
    Xvazio = Qvazio/(3*Ivazio**2)
    print("Xvazio Original: ")
    print(Xvazio)

    -- Para Rot. Bloqueado --
    Rbloq = Pbloq/(3*Ibloq**2)
    Sbloq = sqrt(3)*Vbloq*Ibloq
    Qbloq = sqrt(Sbloq**2 - Pbloq**2)
    Xbloq_freqDeEnsaio = Qbloq/(3*Ibloq**2)
    Xbloq = (fe/Fbloq)*Xbloq_freqDeEnsaio
    """

    # ------- Cálculo dos Parâmetros a Rot. Bloq. -------
    Rbloq = Pbloq / (3*Ibloq**2)
    Zbloq = Vbloq / Ibloq
    # Xbloq em 15Hz!
    Xbloq_freqDeEnsaio = sqrt( Zbloq**2 - Rbloq**2 )
    # Para calcularmos o Xbloq na freq de ensaio:
    Xbloq = Xbloq_freqDeEnsaio * (fe/Fbloq)

    coeficiente_quadratico = 1
    coeficiente_grau_1 = ((Xbloq - Xvazio) - R*(Xbloq + Xvazio)) / R**2
    coeficiente_grau_0 = (Xbloq * Xvazio) / R**2
    polinomio = np.poly1d([coeficiente_quadratico, coeficiente_grau_1, coeficiente_grau_0])
    raizes = polinomio.roots

    for raiz in raizes:
        if ((raiz/Rs) >= 6) and ((raiz/Rs) <= 30):
            Xlrl = raiz
            print(f"O programa optou pela raiz {round(raiz,4)} para o valor de Xlrl, pois Xlrl é {round(raiz/Rs,0)} vezes maior que a resistência do estator.")
            print("Considera-se uma faixa de de 6 a 30 vezes maior.")
            break

    # Trazendo de volta a relação que foi usada para simplificar a expressão e que auxiliou no cálculo das raízes
    # A relação inclusive que relaciona as reatâncias de dispersão com a classe do motor
    Xs = R * Xlrl
    # Xvazio = Xs + Xm -> Xm = Xvazio - Xs
    Xm = Xvazio - Xs
    Rrl = (Rbloq - Rs) * ( (Xlrl + Xm) / Xm)**2

    print('\n------- Parâmetros do MIT ---------')
    print(f'Resistência do estator Rs: {Rs}')
    print(f'Resistência do rotor Rrl: {Rrl}')
    print(f'Reatância de dispersão do estator Xls: {Xs}')
    print(f'Reatância de dispersão do estator Xlrl: {Xlrl}')
    print(f'Reatância de magnetização Xm: {Xm}\n')

# Classes segundo a NEMA
# Dicionário que contém o valor das resistências do circuito do rotor de acordo com a classe
# Onde R é a razão entre Xs e Xlrl: R=Xs/Xrlr, ou seja: Classe A: Xs=0.5 e Xrlr=0.5, por isso R=1.
classes = {'A': 1, 'B': 2/3, 'C': 3/7, 'D': 1, 'Rotor Bobinado': 1}

classe = input("\nSelecione a classe desejada: A, B, C, D ou Rotor Bobinado:\n")

if classe == 'A':
    R = classes['A']
    calculoDosParametrosDoMIT(R, classe)
elif classe == 'B':
    R = classes['B']
    calculoDosParametrosDoMIT(R, classe)
elif classe == 'C':
    R = classes['C']
    calculoDosParametrosDoMIT(R, classe)
elif classe == 'D':
    R = classes['D']
    calculoDosParametrosDoMIT(R, classe)
elif classe == 'Rotor Bobinado':
    R = classes['Rotor Bobinado']
    calculoDosParametrosDoMIT(R, classe)
else:
    print("Nenhuma opção dentre as fornecidas foi escolhida. Assumindo que o usuário queira o cálculo para todas as classes.")
    for classe in classes:
        calculoDosParametrosDoMIT(classes[classe], classe)









