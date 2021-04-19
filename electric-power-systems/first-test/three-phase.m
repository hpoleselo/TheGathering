% Dados Gerais
format long


% Tensoes de Base
va = 69e3;
vb = 13.8e3;
vc = 0.44e3;

zp = 0.078i;

zs = 0.017i;

zps = zp + zs;

z3 = 6.675*exp(j*27.12*pi/180);

xtg = 0.75i;

i2 = 0.52704*exp(j*-18.43*pi/180);

defasamento = 1.0*exp(j*30*pi/180);

defasamento_neg = 1.0*exp(j*-30*pi/180);

v1 = 1.036231*exp(j*-15*pi/180);

% Dados Especificos

i4 = 0.0667*exp(j*-28.836*pi/180);

zlt = 0.0312275*exp(j*20.33*pi/180);

% Esqueca Tudo

numerador = v1 - zps*(i2 + (i4*defasamento)) - (zlt*i4*defasamento);

denominador = zlt/z3 + 1 + zps/z3;

v3 = numerador/denominador;

v2 = v3*((zlt/z3) + 1) + zlt*i4*defasamento;

v4 = v3*defasamento_neg - i4*xtg;

% Letra b

it = (v1 - v2)/zps;
s1 = v1*it;

disp("Letra b: It, S#1");
[abs(it), rad2deg(angle(it))]
[abs(s1), rad2deg(angle(s1))]


disp("V2, FAMIGLIA:")
[abs(v2), rad2deg(angle(v2))]

disp("V3, FAMIGLIA:")
[abs(v3), rad2deg(angle(v3))]

disp("V4, FAMIGLIA:")
[abs(v4), rad2deg(angle(v4))]

v1 = v1*va;
v2 = v2*vb;
v3 = v3*vb;
v4 = v4*vc;

disp("Tensões nas Barras em kV: V1, V2, V3 e V4, respectivamente:");
[abs(v1), rad2deg(angle(v1))]
[abs(v2), rad2deg(angle(v2))]
[abs(v3), rad2deg(angle(v3))]
[abs(v4), rad2deg(angle(v4))]

