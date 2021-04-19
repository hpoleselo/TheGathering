format long
zlt1 = 0.0458843*exp(j*68.4168*pi/180);
zlt2 = 0.276345*exp(j*62.8152*pi/180);
zt1 = 0.01667+0.2667i;
zt2 = 0.02045+0.5391745i;
xg = 0.149971i;
defasamento = 1*exp(j*30*pi/180);

display("ztotal:");
zt = zlt1 + zlt2 + zt1 + zt2;
[abs(zt), rad2deg(angle(zt))]

ig = 0.1143458*exp(j*27.1267*pi/180);
v5 = 0.87454*exp(0);

v1 = ig*zt + v5;

vbase = 13.8e3;
vbase2 = 138e3;
vbase3 = 12.578e3;

fem = v1 + xg*ig
display("fem");
[abs(fem), rad2deg(angle(fem))]

display("fem em kV");
fem = fem*vbase;
[abs(fem), rad2deg(angle(fem))]


display("v1 em pu");
[abs(v1), rad2deg(angle(v1))]

display("v1 em kV");
v1 = v1*vbase;
[abs(v1), rad2deg(angle(v1))]


display("pmax");
pmax = abs(fem)*abs(v1)/0.285604

display("delta1 em pu");
delta1 = zlt1*ig*defasamento

display("delta2 em pu");
delta2 = zlt2*ig;
[abs(delta2), rad2deg(angle(delta2))]

display("delta1 em kV");
delta1 = delta1*vbase2
[abs(delta1), rad2deg(angle(delta1))]

display("delta2 em kV");
delta2 = delta2*vbase3
[abs(delta2), rad2deg(angle(delta2))]