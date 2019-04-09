// Project Ryu
// Compression Driver Design
// (c)2019 Stefan Andrei Chelariu
// andrei.chelariu@projectryu.com

// Constants
rho = 1.225
c = 343
p0 = 2*(10^-5)

// Parameters
a = 0.1 //Diaphragm diameter in m
Eg = 2.83 // Generator Voltage
Re = 3.655 // DC Resistance of the voice coil
Le = 0.0001466 // Impedance of the voice coil (either 1Khz or 10Khz)
BL = 10 //Motor force factor 
Mmd = 0.0044 //Mass of the diaphragm in kg
Cms = 0.03*(10^-3) //Compliance of suspension in m/N
Rms = 9 //Mechanical resistance in mechanical ohms
SD = 0.00911 //Radiating surface area in m^2
Vaf = 0.00911 //Volume of the compression chamber
Laf = 0.001 //distance between diaphragm and phase plug
Wpp = 3 //width of phaseplug slit
Rpp = 2 //ration between area of phaseplug entry and exit
Vab = 0.0002355 //Volume of the back chamber
ST = 0.0000491 //Phase Plug throat area


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
xtitle("Z vs Cab");
xlabel("Frequency [Hz]");
ylabel("Impedance Magnitude [ohms]");
for k=1:10
    x=[20:20000];
    //plot2d(x,acoustic_pressure(x), logflag="ln");
    plot2d(x,impedance_vb(x,k/10000), logflag="ln");
    xgrid(2);
end
subplot(212);
xtitle("Z vs BL");
xlabel("Frequency [Hz]");
ylabel("Impedance Magnitude [ohms]");
for k=5:20
    x=[20:20000];
    //plot2d(x,acoustic_pressure(x), logflag="ln");
    plot2d(x,impedance_bl(x,k), logflag="ln");
    xgrid(2);
end
