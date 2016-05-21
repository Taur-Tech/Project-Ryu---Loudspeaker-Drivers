from numpy import *
from wire import Wire
from steel import Steel
from datetime import datetime
import matplotlib.pyplot as ploter

class Calculator:
    #Calculator Constants
    START_FRQ   = 20
    STOP_FRQ    = 20000
    
    #Report Constants
    HEADER      = "***********************************************************\n"
    HEADER     += "***PROJECT RYU: VOICE COIL CALCULATOR***\n"
    HEADER     += "***********************************************************\n"
    HEADER     += "\n\n" 
    HEADER     += "#DATE: "    
    RETURN      = "\n"
    FOOTER      = "****************************EOF*************************\n"
    
    def __init__(self, window):
        self.window = window        
    
    def setData(self, vc_data, motor_data, cone_data):
        self.vc_data = vc_data
        self.m_data = motor_data
        self.c_data = cone_data
        self.wire = Wire(self.vc_data['in_uifVCWireMat'])
        self.steel = Steel(self.m_data['in_uifMSteel'])
        self.window.log(self.HEADER)
        self.window.log(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
        self.window.log(self.RETURN)
        
    def calcGmVC(self):
        count = 0
        while count < 10:
            for k,v in self.vc_data.iteritems():
                if v == 0:
                    self.run[k](self)
            count = count + 1
        self.window.calc_callback(self.vc_data)
    
    def calcImp(self):
        Le = self.vc_data['in_uifVCLe']/1000
        Re = self.vc_data['in_uifVCDCRes']
        freq_array = self.returnFreqArray(0.33)
        Zmag_array = []
        Zphi_array = []
        for freq in freq_array:
            XL = 2*pi*freq*Le
            #Calculate impedance magnitude
            Zmag = sqrt(power(Re, 2.0) + power(XL, 2.0))
            #Calculate impedance phase
            Zphi = arctan(XL/Re)*180.0/pi
            Zmag_array.append(Zmag)
            Zphi_array.append(Zphi) 
        self.graphLImp(Zmag_array, Zphi_array)
        
    def graphLImp(self, array, array_opt = None):  
        g = ploter.gca() 
        f = ploter.gcf()     
        f.canvas.set_window_title('Locked Voice Coil Impedance')
        g.plot(self.returnFreqArray(0.33), array)
        ploter.title('Locked Voice Coil Impedance')
        g.set_xscale('log')
        g.set_xlabel('Frequency [Hz]')
        g.set_ylabel('Magnitude [Ohms]')
        g.grid(b=True, which='major', color='b', linestyle='-')
        g.grid(b=True, which='minor', color='r', linestyle='--')
        if array_opt != None:
            g_opt = g.twinx()
            g_opt.set_ylabel('Phase [deg]')
            g_opt.plot(self.returnFreqArray(0.33), array_opt, 'r.')
        ploter.show()
        
    def calcMImp(self):
        Mmc = self.c_data['in_uifCMass']
        Cms = self.c_data['in_uifCCms']
        Rms = self.c_data['in_uifCRms']
        B = self.m_data['in_uifMFlux']
        if Mmc == 0 or Cms == 0 or Rms == 0 or B == 0:
            return false
        Cms = Cms/1000        
        Le = self.vc_data['in_uifVCLe']/1000
        Re = self.vc_data['in_uifVCDCRes']
        l = self.vc_data['in_uifVCWireLen']/1000
        Mms = (Mmc + self.vc_data['in_uifVCMass'])/1000
        BL = B*l
        BL_sqr = power(BL, 2)        
        freq_array = self.returnFreqArray(0.33)
        Zmag_array = []
        Zphi_array = []
        for freq in freq_array:
            w = 2*pi*freq            
            #Denominator for mechanical impedance
            Km = power((Rms/BL_sqr),2.0)+power((w*Mms/BL_sqr) - 1/(w*BL_sqr*Cms),2.0)
            #Calculate real part of mechanical impedance
            Rm = (Rms/BL_sqr)/Km
            #Calculate imaginary part of mechanical impedance
            Xm = (1/(w*BL_sqr*Cms) - w*Mms/BL_sqr)/Km
            #Calculate total impedance real and imaginary parts
            R = Re + Rm
            X = w*Le + Xm
            #Calculate total impedance magnitude
            Zmag = sqrt(power(R, 2.0) + power(X, 2.0))
            #Calculate total impedance phase
            Zphi = arctan(X/R)*180.0/pi
            Zmag_array.append(Zmag)
            Zphi_array.append(Zphi) 
        self.graphLImp(Zmag_array, Zphi_array)    
        
    
    #UTILITY FUNCTIONS
    def returnFreqArray(self, smoothing):
        freq = []
        freq.append(self.START_FRQ)
        next_freq = power(2, smoothing)*self.START_FRQ
        while next_freq <= self.STOP_FRQ:
            freq.append(next_freq)
            next_freq = power(2, smoothing)*next_freq
        return freq
    
    def circ_xsection(self, dia):
        return power(dia/2, 2)*pi
        
    #PARAMETER CALCULATIONS    
    def nothing(self):
        print ""
    
    #Calculate voice coil mean diameter
    def c_mDia(self):
        inner_dia = self.vc_data['in_uifVCInDia']
        outer_dia = self.vc_data['in_uifVCOutDia']
        wire_dia = self.vc_data['in_uifVCWireDia']
        vc_layers = int(self.vc_data['in_uifVCLayers'])
        fm_thick = self.vc_data['in_uifVCFormerTh']
        if inner_dia == 0 and outer_dia == 0:
            return
        elif inner_dia != 0 and outer_dia == 0:
            if wire_dia == 0 or vc_layers == 0 or fm_thick == 0:
                return
            else:
                outer_dia = inner_dia + wire_dia*vc_layers*2 + fm_thick*2
        elif inner_dia == 0 and outer_dia != 0:
            if wire_dia == 0 or vc_layers == 0 or fm_thick == 0:
                return
            else:
                inner_dia = outer_dia - (wire_dia*vc_layers*2 + fm_thick*2)                
        self.vc_data['in_uifVCMeanDia'] = (outer_dia + inner_dia)/2
        
    #Calculate former thickness
    def c_fTh(self):
        inner_dia = self.vc_data['in_uifVCInDia']
        outer_dia = self.vc_data['in_uifVCOutDia']
        wire_dia = self.vc_data['in_uifVCWireDia']
        vc_layers = int(self.vc_data['in_uifVCLayers'])
        if inner_dia == 0 or outer_dia == 0 or wire_dia == 0 or vc_layers == 0:
            return
        else:
            self.vc_data['in_uifVCFormerTh'] = (outer_dia - inner_dia)/2 - wire_dia*vc_layers
    
    #Calculate wire diameter
    def c_wDia(self):
        inner_dia = self.vc_data['in_uifVCInDia']
        outer_dia = self.vc_data['in_uifVCOutDia']
        vc_layers = int(self.vc_data['in_uifVCLayers'])
        fm_thick = self.vc_data['in_uifVCFormerTh']
        if inner_dia == 0 or outer_dia == 0 or fm_thick == 0 or vc_layers == 0:
            return
        else: 
            self.vc_data['in_uifVCWireDia'] = ((outer_dia - inner_dia)/2 - fm_thick)/vc_layers
            
    #Calculate the number of turns per layer
    def c_vTurns(self):
        wire_dia = self.vc_data['in_uifVCWireDia']
        vc_height = self.vc_data['in_uifVCWindingHi']
        if wire_dia == 0 or vc_height == 0:
            return
        else:
            self.vc_data['in_uifVCTurns'] = vc_height/wire_dia
            
    #Calculate the number of layers
    def c_vLayers(self):
        inner_dia = self.vc_data['in_uifVCInDia']
        outer_dia = self.vc_data['in_uifVCOutDia']
        wire_dia = self.vc_data['in_uifVCWireDia']
        fm_thick = self.vc_data['in_uifVCFormerTh']
        if inner_dia == 0 or outer_dia == 0 or fm_thick == 0 or wire_dia == 0:
            return
        else: 
            self.vc_data['in_uifVCLayers'] = ((outer_dia - inner_dia)/2 - fm_thick)/wire_dia
    
    #Calculate winding height
    def c_wHi(self):
        wire_dia = self.vc_data['in_uifVCWireDia']
        vc_turns = int(self.vc_data['in_uifVCTurns'])
        if wire_dia == 0 or vc_turns == 0:
            return
        else:
            self.vc_data['in_uifVCWindingHi'] = wire_dia*vc_turns
            
    #Calculate wire length
    def c_wLen(self):        
        wire_length = 0
        inner_dia = self.vc_data['in_uifVCInDia']
        outer_dia = self.vc_data['in_uifVCOutDia']
        wire_dia = self.vc_data['in_uifVCWireDia']
        vc_layers = int(self.vc_data['in_uifVCLayers'])
        vc_height = self.vc_data['in_uifVCWindingHi']
        vc_turns = int(self.vc_data['in_uifVCTurns'])
        fm_height = self.vc_data['in_uifVCFormerHi']
        if inner_dia == 0 or outer_dia == 0 or wire_dia == 0 or vc_layers == 0 or vc_height == 0 or vc_turns == 0:
            return
        #method to calculate length
        def ret_length(dia):
            f_len = pi*dia*vc_turns
            #k factors in the pitch between turns
            k = (1+power((vc_height/f_len),2))
            return f_len*sqrt(k)        
        #Determine average diameter for every layer
        if self.vc_data['in_uifVCWindingTy'] == "Outside":
            for layer_no in range(0, vc_layers-1):
                lm_dia = outer_dia - wire_dia*(2*layer_no+1)
                wire_length = wire_length + ret_length(lm_dia)
        elif self.vc_data['in_uifVCWindingTy'] == "Inside":
            for layer_no in range(0, vc_layers-1):
                lm_dia = inner_dia + wire_dia*(2*layer_no+1)
                wire_length = wire_length + ret_length(lm_dia)
        else:
            #Inside/Outside case
            if vc_layers%2 != 0:
                return
            if vc_layers > 2:
                for layer_no in range(0, vc_layers/2-1):
                    lm_in_dia = inner_dia + wire_dia*(2*layer_no+1)
                    wire_length = wire_length + ret_length(lm_in_dia)
                    lm_out_dia = outer_dia - wire_dia*(2*layer_no+1)
                    wire_length = wire_length + ret_length(lm_out_dia)
            else:
                lm_in_dia = inner_dia + wire_dia
                wire_length = wire_length + ret_length(lm_in_dia)
                lm_out_dia = outer_dia - wire_dia
                wire_length = wire_length + ret_length(lm_out_dia)
        wire_length = wire_length + 2*fm_height
        self.vc_data['in_uifVCWireLen'] = wire_length
        
    #Calculate voice coil inner diameter
    def c_vIDia(self):
        inner_dia = 0
        outer_dia = self.vc_data['in_uifVCOutDia']
        wire_dia = self.vc_data['in_uifVCWireDia']
        vc_layers = int(self.vc_data['in_uifVCLayers'])
        fm_thick = self.vc_data['in_uifVCFormerTh']
        m_dia = self.vc_data['in_uifVCMeanDia']
        if outer_dia == 0 and m_dia == 0:
            return
        elif outer_dia != 0 and m_dia == 0:
            if fm_thick == 0 or vc_layers == 0 or wire_dia == 0:
                return
            inner_dia = outer_dia - (fm_thick + vc_layers*wire_dia)*2
        elif outer_dia == 0 and m_dia != 0:
            if fm_thick == 0 or vc_layers == 0 or wire_dia == 0:
                return
            inner_dia = m_dia - (fm_thick + vc_layers*wire_dia)
        else:
            inner_dia = 2*m_dia - outer_dia
        self.vc_data['in_uifVCInDia'] = inner_dia
        
    #Calculate voice coil outer diameter
    def c_vODia(self):
        inner_dia = self.vc_data['in_uifVCInDia']
        outer_dia = 0
        wire_dia = self.vc_data['in_uifVCWireDia']
        vc_layers = int(self.vc_data['in_uifVCLayers'])
        fm_thick = self.vc_data['in_uifVCFormerTh']
        m_dia = self.vc_data['in_uifVCMeanDia']
        if inner_dia == 0 and m_dia == 0:
            return
        elif inner_dia != 0 and m_dia == 0:
            if fm_thick == 0 or vc_layers == 0 or wire_dia == 0:
                return
            outer_dia = inner_dia + (fm_thick + wire_dia*vc_layers)*2
        elif inner_dia == 0 and m_dia != 0:
            if fm_thick == 0 or vc_layers == 0 or wire_dia == 0:
                return
            outer_dia = m_dia + (fm_thick + vc_layers*wire_dia)
        else:
            outer_dia = 2*m_dia - inner_dia
        self.vc_data['in_uifVCOutDia'] = outer_dia
        
    #Calculate voice coil mass
    def c_vMass(self):
        wire_dia = self.vc_data['in_uifVCWireDia']
        wire_len = self.vc_data['in_uifVCWireLen']
        if wire_dia == 0 or wire_len == 0:
            return
        wire_xsec = self.circ_xsection(wire_dia)
        self.vc_data['in_uifVCMass'] = wire_xsec*(wire_len/1000)*self.wire.density
        
    #Calculate voice coil rdc
    def c_vRdc(self):
        wire_dia = self.vc_data['in_uifVCWireDia']
        wire_len = self.vc_data['in_uifVCWireLen']
        if wire_dia == 0 or wire_len == 0:
            return
        wire_xsec = self.circ_xsection(wire_dia)
        self.vc_data['in_uifVCDCRes'] = self.wire.resistivity*(wire_len/1000)/wire_xsec
        
    #Calculate voice coil le
    def c_vLe(self):
        wire_dia = self.vc_data['in_uifVCWireDia']/1000
        vc_layers = int(self.vc_data['in_uifVCLayers'])
        vc_turns = int(self.vc_data['in_uifVCTurns'])
        vc_rad = self.vc_data['in_uifVCInDia']/1000
        L = 0
        l_pitch = wire_dia
        t_pitch = wire_dia
        core_mu = self.steel.getMu(self.m_data['in_uifMFlux'])
        if vc_rad == 0:
            return
        def Mod(m, n, j, k):
            mod = 4.0*(vc_rad+k*l_pitch)*(vc_rad+n*l_pitch)
            p1 = power((2.0*vc_rad+l_pitch*(k+n)), 2.0)
            p2 = power((m-j), 2.0)
            return mod/(p1+p2*power((t_pitch), 2.0))      
        
        def EllipIntegrals(m, n, j, k):
            k_mod = Mod(m, n, j, k)
            return (2.0-k_mod)*ellipk(k_mod) - 2*ellipe(k_mod)    
                
        # Calculate Mutual inductance for wire loop 
        # on the m-th turn and n-th layer
        def M_ind(m, n):
            M = 0
            for j in range(0, vc_turns-1):
                for k in range(0, vc_layers-1):
                    if j != m and k != n:
                        p1 = power((2.0*vc_rad+l_pitch*(k+n)), 2.0)
                        p2 = power((m-j), 2.0)
                        M = M + sqrt(p1+p2*power((t_pitch), 2.0))*EllipIntegrals(m, n, j, k)
            return M*core_mu/2.0
        
        # Calculate Self inductance for wire loop 
        # on the m-th turn and n-th layer
        def S_ind(m, n):
            p1 = vc_rad+n*l_pitch
            p2 = log(8.0*p1/(wire_dia/2.0))
            return core_mu*p1*(p2-7.0/4.0)
            
        for x in range(0, vc_turns-1):
            for y in range(0, vc_layers-1):
                L = L + S_ind(x, y) + M_ind(x, y)
                
        self.vc_data['in_uifVCLe'] = L*1000
            
    run = {
            "in_uifVCTypeNo": nothing,  
            "in_uifVCMeanDia": c_mDia,        
            "in_uifVCFormerTh": c_fTh,
            "in_uifVCFormerMAt": nothing,
            "in_uifVCFormerIn": nothing,
            "in_uifVCFormerOut": nothing,
            "in_uifVCFormerHi": nothing,
            "in_uifVCFormerMass": nothing,
            "in_uifVCWireMat": nothing,
            "in_uifVCWireDia": c_wDia,
            "in_uifVCTurns": c_vTurns,
            "in_uifVCLayers": c_vLayers,
            "in_uifVCWindingHi": c_wHi,
            "in_uifVCWindingTy": nothing,
            "in_uifVCWireLen": c_wLen,
            "in_uifVCInDia": c_vIDia,
            "in_uifVCOutDia": c_vODia,
            "in_uifVCMass": c_vMass,
            "in_uifVCDCRes": c_vRdc,
            "in_uifVCLe": c_vLe,
            "in_uifMType": nothing,
            "in_uifMSteel": nothing,
            "in_uifMGapType": nothing,
            "in_uifMGapW": nothing,
            "in_uifMGapH": nothing,
            "in_uifMGapRing": nothing,
            "in_uifMFlux": nothing,
            "in_uifCMass": nothing,
            "in_uifCSurrComp": nothing
        }