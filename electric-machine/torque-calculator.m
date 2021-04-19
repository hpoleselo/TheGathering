% Henrique Poleselo
% Calculates Torque without the use of the Rotor Current (Ir), i.e using Thevenin's Theorem deduction

format long

Rs = 0.5;
xls = 2i;

% Resistencia no rotor referida ao estator
Rrl = 0.6;
xlr = 1.5i;
xm = 22i;

% Escorregamento
s = 1;

% Numero de fases
q = 3;

polos = 14;
f = 60;
we = f*2*pi;

Vs = 380;
Vs = Vs/sqrt(3);


zth = ((Rs+xls)*xm)/(Rs+xls+xm)

% Supondo que seja um divisor de tensão na reatância de magnetização
Vth = (Vs*xm)/(xls+xm+Rs)
rth = real(zth);
xth = imag(zth);

% (abs(vth))**2  % * (Rrl/s)
numerador = q * (abs(Vth)**2)* (Rrl/s);

%
denominador = (rth+(Rrl/s))**2 + (abs(xth) + abs(xlr))**2

mult = (polos/(2*we))
tmec = mult*(numerador/denominador);

numerador2 = 0.5 * q * (abs(Vth)**2);
denominador2 = rth + sqrt(rth**2 + (abs(xth)+abs(xlr))**2);
tmax = mult*(numerador2/denominador2);

display("Tnominal: ");
display(tmec)

display("Tmax: ");
display(tmax)
