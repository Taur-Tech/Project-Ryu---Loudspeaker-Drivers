// Project Ryu
// Compression Driver Design
// (c)2019 Stefan Andrei Chelariu
// andrei.chelariu@projectryu.com

// Constants
rho = 1.225
c = 343
p0 = 2*(10^-5)

// Parameters
a = 0.025
Eg = 2.83
Re = 6.2
Le = 0.0002
BL = 10
Mmd = 0.003
Cms = 0.03*(10^-3)
Rms = 9
SD = 0.00911
Vaf = 0.00911
Laf = 0.001 //distance between diaphragm and phase plug
Wpp = 3 //width of phaseplug slit
Rpp = 2 //ration between area of phaseplug entry and exit
Vab = 0.0002355
ST = 0.0000491


function y=impedance_bl(f,bl)
    //Mechanical to Electric
    Cmes = Mmd./(bl^2)
    Res = bl^2./Rms
    Lces = Cms.*(bl^2)
    //Acoustic
    Cab = Vab./(rho*(c^2))
    Caf = Vaf./(rho*(c^2))
    Maf = (rho*Laf)/(%pi*((Wpp/2)^2))
    //Acoustic to Electric
    Lceb = (Cab./SD^2).*bl^2
    Lcef = (Caf./SD^2).*bl^2
    Cmef = (Maf.*SD^2)./(bl^2)
    
    w = 2*%pi*f;
    ka = w.*a/c;
    //Acoustic Radiation
    Zar = w^4.*(16.*rho.*(a&2)./(27*%pi^3*c^3))+%i.*w.*(8*rho/(3*%pi^3*a));
    //Mechanical Impedance
    Zm = Res./(1+%i.*w.*Res.*(Cmes-1./(w^2.*(Lces+Lceb))));
    //Acoustic Impedance
    Za = (SD./ST)^2*Zar./(%i.*w.*Cmef.*((SD./ST)^2*Zar + 1./(%i.*w.*Cmef)));
    //Compute parallel mechanical and acoustic impedances
    Zp = Zm.*Za./(Zm + Za);
    //Compute total impedance
    y = abs(Re + %i.*w.*Le + Zp);
endfunction


function y=impedance_vb(f,vb)
    //Acoustic
    Cab = vb./(rho*(c^2))
    Caf = Vaf./(rho*(c^2))
    Maf = (rho*Laf)/(%pi*((Wpp/2)^2))
    //Mechanical to Electric
    Cmes = Mmd./(BL^2)
    Res = BL^2./Rms
    Lces = Cms.*(BL^2)
    //Acoustic to Electric
    Lceb = (Cab./SD^2).*BL^2
    Lcef = (Caf./SD^2).*BL^2
    Cmef = (Maf.*SD^2)./(BL^2)

    w = 2*%pi*f;
    ka = w.*a/c;
    //Acoustic Radiation
    Zar = w^4.*(16.*rho.*(a&2)./(27*%pi^3*c^3))+%i.*w.*(8*rho/(3*%pi^3*a));
    //Mechanical Impedance
    Zm = Res./(1+%i.*w.*Res.*(Cmes-1./(w^2.*(Lces+Lceb))));
    //Acoustic Impedance    
    Za = (SD./ST)^2*Zar./(%i.*w.*Cmef.*((SD./ST)^2*Zar + 1./(%i.*w.*Cmef)));
    //Compute parallel mechanical and acoustic impedances
    Zp = Zm.*Za./(Zm + Za);
    //Compute total impedance
    y = abs(Re + %i.*w.*Le + Zp);
endfunction

function y=zar(f)
    w = 2*%pi*f;
    ka = w.*a/c;
    Zar = w^4.*(16.*rho.*(a&2)./(27*%pi^3*c^3))+%i.*w.*(8*rho/(3*%pi^3*a));
    y = abs(Zar);
endfunction

clf();
subplot(211);
for k=1:10
    x=[20:20000];
    //plot2d(x,acoustic_pressure(x), logflag="ln");
    plot2d(x,impedance_vb(x,k/10000), logflag="ln");
    xgrid(2);
end
subplot(212);
for k=1:10
    x=[20:20000];
    //plot2d(x,acoustic_pressure(x), logflag="ln");
    plot2d(x,impedance_bl(x,k), logflag="ln");
    xgrid(2);
end
