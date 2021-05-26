import numpy as np
from math import pi


def ret2pol(z):
    x = z.real
    y = z.imag
    modulo = np.sqrt(x**2 + y**2)
    theta = (180/pi)*(np.arctan2(y, x))
    return(modulo, theta)

def pol2ret(modulo, theta):
    x = modulo * np.cos(theta)
    y = modulo * np.sin(theta)
    return(x, y)

p = 4
fe = 60
vs = 230
ns = fe*120/p
Ws = ns*2*pi/60

rs = 9.5 # ou r1
rrl = 10.8 # ou r2l
xlr = 12j # x1 ou x2
xls = 12j
xm = 260j

sf = 0.05

sb = 2 - sf

num_zf = ((rrl/sf) + xlr) * xm
print(f'\nNumerador Zf: {num_zf}')

den_zf = (rrl/sf) + xlr + xm
print(f'\nDenominador Zf: {den_zf}')

zf = 0.5*(num_zf/den_zf)
rf = zf.real
print(f'\nZf: {zf}')

num_zb = (rrl/sb + xlr) * xm
print(f'\nNumerador Zb: {num_zb}')

den_zb = rrl/sb + xlr + xm
print(f'\nDenominador Zb: {den_zb}')

zb = 0.5*(num_zb/den_zb)
rb = zb.real
print(f'\nZb: {zb}')

zs = rs + xls
print(f'\nZs: {zs}')

Is = vs / (zs + zb + zf)
print(f'\nIs: {Is}')

Is_pol = ret2pol(Is)
print(f'\nIs polar: {Is_pol}')

PotEntrada = vs*np.conjugate(Is)
PotEntrada_pol = ret2pol(PotEntrada)
print(PotEntrada)
print(PotEntrada_pol)
print(np.arccos(44.615*pi/180))

# Potência de entreferro
Pgf = rf*(abs(Is))**2
Pgb = rb*(abs(Is))**2
print(f'\nPot. Entreferro forward: {Pgf}')
print(f'\nPot. Entreferro backward: {Pgb}')

Tem = (Pgf - Pgb)/Ws
print(f'\nVelocidade Síncrona em rad/s: {Ws} ')
print(f'\nTorque desenvolvido (eletromagnético): {Tem}')

Prot = AlgumaPot - (abs(Is)**2 * (rs+rrl))
#Teixo = Tem - Trot
#Peixo = Pem - Prot

Pmech = Tem*Ws*(1-sf)

PotSaida = Pmech - Prot
print(f'\nPotência de Saída: {PotSaida}')

eficiencia = PotSaida/PotEntrada
print(f'\nEficiência: {eficiencia}')
