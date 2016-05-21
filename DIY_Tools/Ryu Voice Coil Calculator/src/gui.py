import wx
from calculator import *

class MainWindow(wx.Frame):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Project Ryu Voice Coil Calculator", pos = wx.DefaultPosition, size = wx.Size( 1024,720 ), style = wx.DEFAULT_FRAME_STYLE|wx.HSCROLL )
        self.drawMenu()
        self.proc = Calculator(self)
   
    #GUI Functions
    def drawMenu(self):
        self.SetSizeHintsSz( wx.Size( 800,600 ), wx.DefaultSize )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
        
        self.topMenu = wx.MenuBar( 0 )
        self.fileMenu = wx.Menu()
        self.mNew = wx.MenuItem( self.fileMenu, wx.ID_ANY, u"New", wx.EmptyString, wx.ITEM_NORMAL )
        self.fileMenu.AppendItem( self.mNew )
        
        self.mOpen = wx.MenuItem( self.fileMenu, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
        self.fileMenu.AppendItem( self.mOpen )
        
        self.mSave = wx.MenuItem( self.fileMenu, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
        self.fileMenu.AppendItem( self.mSave )
        
        self.fileMenu.AppendSeparator()
        
        self.mExit = wx.MenuItem( self.fileMenu, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
        self.fileMenu.AppendItem( self.mExit )
        
        self.topMenu.Append( self.fileMenu, u"File" ) 
        
        self.helpMenu = wx.Menu()
        self.mHelp = wx.MenuItem( self.helpMenu, wx.ID_ANY, u"Online Help", wx.EmptyString, wx.ITEM_NORMAL )
        self.helpMenu.AppendItem( self.mHelp )
        
        self.mAbout = wx.MenuItem( self.helpMenu, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL )
        self.helpMenu.AppendItem( self.mAbout )
        
        self.topMenu.Append( self.helpMenu, u"Help" ) 
        
        self.SetMenuBar( self.topMenu )  
        
        self.Bind( wx.EVT_MENU, self.OnQuit, id = self.mExit.GetId() )
        self.Bind( wx.EVT_MENU, self.OnNew, id = self.mNew.GetId() )
        
        self.Layout()
        
        self.Centre( wx.BOTH )  
        
    def drawMainPanel(self):
        mainFrameSizer = wx.GridBagSizer( 0, 0 )
        mainFrameSizer.SetFlexibleDirection( wx.BOTH )
        mainFrameSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )
        
        self.userInputVC = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer2 = wx.GridSizer( 0, 4, 0, 0 )
        
        self.uifTitle = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Voice Coil Parameters", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifTitle.Wrap( -1 )
        gSizer2.Add( self.uifTitle, 0, wx.ALL, 5 )
        
        self.uifName = wx.StaticText( self.userInputVC, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifName.Wrap( -1 )
        gSizer2.Add( self.uifName, 0, wx.ALL, 5 )
        
        self.m_staticText14 = wx.StaticText( self.userInputVC, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )
        gSizer2.Add( self.m_staticText14, 0, wx.ALL, 5 )
        
        self.m_staticText15 = wx.StaticText( self.userInputVC, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )
        gSizer2.Add( self.m_staticText15, 0, wx.ALL, 5 )
        
        self.uifVCTypeNo = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Voice Coil Number", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCTypeNo.Wrap( -1 )
        gSizer2.Add( self.uifVCTypeNo, 0, wx.ALL, 5 )
        
        in_uifVCTypeNoChoices = [ u"Single", u"Dual" ]
        self.in_uifVCTypeNo = wx.Choice( self.userInputVC, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, in_uifVCTypeNoChoices, 0 )
        self.in_uifVCTypeNo.SetSelection( 0 )
        gSizer2.Add( self.in_uifVCTypeNo, 0, wx.ALL, 5 )
        
        self.uifVCMeanDia = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Average Diameter", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCMeanDia.Wrap( -1 )
        gSizer2.Add( self.uifVCMeanDia, 0, wx.ALL, 5 )
        
        self.in_uifVCMeanDia = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0",  wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCMeanDia, 0, wx.ALL, 5 )
        
        self.uifVCFormerTh = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Former Thickness", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCFormerTh.Wrap( -1 )
        gSizer2.Add( self.uifVCFormerTh, 0, wx.ALL, 5 )
        
        self.in_uifVCFormerTh = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCFormerTh, 0, wx.ALL, 5 )
        
        self.uifVCFormerMat = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Former Material", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCFormerMat.Wrap( -1 )
        gSizer2.Add( self.uifVCFormerMat, 0, wx.ALL, 5 )
        
        in_uifVCFormerMAtChoices = [ u"Kapton", u"Aluminum", u"Paper" ]
        self.in_uifVCFormerMAt = wx.Choice( self.userInputVC, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, in_uifVCFormerMAtChoices, 0 )
        self.in_uifVCFormerMAt.SetSelection( 0 )
        gSizer2.Add( self.in_uifVCFormerMAt, 0, wx.ALL, 5 )
        
        self.uifVCFormerIn = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Former Inner Diameter", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCFormerIn.Wrap( -1 )
        gSizer2.Add( self.uifVCFormerIn, 0, wx.ALL, 5 )
        
        self.in_uifVCFormerIn = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.in_uifVCFormerIn, 0, wx.ALL, 5 )
        
        self.uifVCFormerOut = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Former Outer Diameter", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCFormerOut.Wrap( -1 )
        gSizer2.Add( self.uifVCFormerOut, 0, wx.ALL, 5 )
        
        self.in_uifVCFormerOut = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.in_uifVCFormerOut, 0, wx.ALL, 5 )
        
        self.uifVCFormerHi = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Former Height", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCFormerHi.Wrap( -1 )
        gSizer2.Add( self.uifVCFormerHi, 0, wx.ALL, 5 )
        
        self.in_uifVCFormerHi = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCFormerHi, 0, wx.ALL, 5 )
        
        self.uifVCFormerMass = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Former Mass", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCFormerMass.Wrap( -1 )
        gSizer2.Add( self.uifVCFormerMass, 0, wx.ALL, 5 )
        
        self.in_uifVCFormerMass = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCFormerMass, 0, wx.ALL, 5 )
        
        self.uifVCWireMat = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Wire Material", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCWireMat.Wrap( -1 )
        gSizer2.Add( self.uifVCWireMat, 0, wx.ALL, 5 )
        
        in_uifVCWireMatChoices = [ u"ECW", u"ECCAW", u"EAW" ]
        self.in_uifVCWireMat = wx.Choice( self.userInputVC, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, in_uifVCWireMatChoices, 0 )
        self.in_uifVCWireMat.SetSelection( 0 )
        gSizer2.Add( self.in_uifVCWireMat, 0, wx.ALL, 5 )
        
        self.uifVCWireDia = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Wire Diameter", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCWireDia.Wrap( -1 )
        gSizer2.Add( self.uifVCWireDia, 0, wx.ALL, 5 )
        
        self.in_uifVCWireDia = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCWireDia, 0, wx.ALL, 5 )
        
        self.uifVCTurns = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Turns per Coil", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCTurns.Wrap( -1 )
        gSizer2.Add( self.uifVCTurns, 0, wx.ALL, 5 )
        
        self.in_uifVCTurns = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCTurns, 0, wx.ALL, 5 )
        
        self.uifVCLayers = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Layers per Coil", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCLayers.Wrap( -1 )
        gSizer2.Add( self.uifVCLayers, 0, wx.ALL, 5 )
        
        self.in_uifVCLayers = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCLayers, 0, wx.ALL, 5 )
        
        self.uifVCWindingHi = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Winding Height", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCWindingHi.Wrap( -1 )
        gSizer2.Add( self.uifVCWindingHi, 0, wx.ALL, 5 )
        
        self.in_uifVCWindingHi = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCWindingHi, 0, wx.ALL, 5 )
        
        self.uifVCWindingTy = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Winding Type", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCWindingTy.Wrap( -1 )
        gSizer2.Add( self.uifVCWindingTy, 0, wx.ALL, 5 )
        
        in_uifVCWindingTyChoices = [ u"Outside", u"Inside", u"Inside/Outside" ]
        self.in_uifVCWindingTy = wx.Choice( self.userInputVC, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, in_uifVCWindingTyChoices, 0 )
        self.in_uifVCWindingTy.SetSelection( 0 )
        gSizer2.Add( self.in_uifVCWindingTy, 0, wx.ALL, 5 )
        
        self.uifVCWireLen = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Wire Length per Coil", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCWireLen.Wrap( -1 )
        gSizer2.Add( self.uifVCWireLen, 0, wx.ALL, 5 )
        
        self.in_uifVCWireLen = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCWireLen, 0, wx.ALL, 5 )
        
        self.uifVCInDia = wx.StaticText( self.userInputVC, wx.ID_ANY, u"VC Inner Diameter", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCInDia.Wrap( -1 )
        gSizer2.Add( self.uifVCInDia, 0, wx.ALL, 5 )
        
        self.in_uifVCInDia = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCInDia, 0, wx.ALL, 5 )
        
        self.uifVCOutDia = wx.StaticText( self.userInputVC, wx.ID_ANY, u"VC Outer Diameter", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCOutDia.Wrap( -1 )
        gSizer2.Add( self.uifVCOutDia, 0, wx.ALL, 5 )
        
        self.in_uifVCOutDia = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCOutDia, 0, wx.ALL, 5 )
        
        self.uifVCMass = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Total Mass", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCMass.Wrap( -1 )
        gSizer2.Add( self.uifVCMass, 0, wx.ALL, 5 )
        
        self.in_uifVCMass = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCMass, 0, wx.ALL, 5 )
        
        self.uifVCDCRes = wx.StaticText( self.userInputVC, wx.ID_ANY, u"DC Resistance per Coil", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCDCRes.Wrap( -1 )
        gSizer2.Add( self.uifVCDCRes, 0, wx.ALL, 5 )
        
        self.in_uifVCDCRes = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer2.Add( self.in_uifVCDCRes, 0, wx.ALL, 5 )
        
        self.uifVCLe = wx.StaticText( self.userInputVC, wx.ID_ANY, u"Inductance ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifVCLe.Wrap( -1 )
        gSizer2.Add( self.uifVCLe, 0, wx.ALL, 5 )
        
        self.in_uifVCLe = wx.TextCtrl( self.userInputVC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize,wx.TE_PROCESS_ENTER)
        gSizer2.Add( self.in_uifVCLe, 0, wx.ALL, 5 )
        
        
        self.userInputVC.SetSizer( gSizer2 )
        self.userInputVC.Layout()
        gSizer2.Fit( self.userInputVC )
        mainFrameSizer.Add( self.userInputVC, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )
        
        self.userInputM = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer4 = wx.GridSizer( 0, 4, 0, 0 )
        
        self.uifMTitle = wx.StaticText( self.userInputM, wx.ID_ANY, u"Motor Parameters", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifMTitle.Wrap( -1 )
        gSizer4.Add( self.uifMTitle, 0, wx.ALL, 5 )
        
        self.m_staticText23 = wx.StaticText( self.userInputM, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText23.Wrap( -1 )
        gSizer4.Add( self.m_staticText23, 0, wx.ALL, 5 )
        
        self.m_staticText24 = wx.StaticText( self.userInputM, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText24.Wrap( -1 )
        gSizer4.Add( self.m_staticText24, 0, wx.ALL, 5 )
        
        self.m_staticText25 = wx.StaticText( self.userInputM, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText25.Wrap( -1 )
        gSizer4.Add( self.m_staticText25, 0, wx.ALL, 5 )
        
        self.uifMType = wx.StaticText( self.userInputM, wx.ID_ANY, u"Motor Type", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifMType.Wrap( -1 )
        gSizer4.Add( self.uifMType, 0, wx.ALL, 5 )
        
        in_uifMTypeChoices = [ u"Field Coil", u"PM", wx.EmptyString ]
        self.in_uifMType = wx.Choice( self.userInputM, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, in_uifMTypeChoices, 0 )
        self.in_uifMType.SetSelection( 0 )
        gSizer4.Add( self.in_uifMType, 0, wx.ALL, 5 )
        
        self.uifMSteel = wx.StaticText( self.userInputM, wx.ID_ANY, u"Pole Piece Steel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifMSteel.Wrap( -1 )
        gSizer4.Add( self.uifMSteel, 0, wx.ALL, 5 )
        
        in_uifMSteelChoices = [ u"1010", u"1008", u"1006" ]
        self.in_uifMSteel = wx.Choice( self.userInputM, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, in_uifMSteelChoices, 0 )
        self.in_uifMSteel.SetSelection( 0 )
        gSizer4.Add( self.in_uifMSteel, 0, wx.ALL, 5 )
        
        self.uifMGapType = wx.StaticText( self.userInputM, wx.ID_ANY, u"Magnetic Gap Type", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifMGapType.Wrap( -1 )
        gSizer4.Add( self.uifMGapType, 0, wx.ALL, 5 )
        
        in_uifMGapTypeChoices = [ u"Underhung", u"Overhung" ]
        self.in_uifMGapType = wx.Choice( self.userInputM, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, in_uifMGapTypeChoices, 0 )
        self.in_uifMGapType.SetSelection( 0 )
        gSizer4.Add( self.in_uifMGapType, 0, wx.ALL, 5 )
        
        self.uifMGapW = wx.StaticText( self.userInputM, wx.ID_ANY, u"Magnetic Gap Width", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifMGapW.Wrap( -1 )
        gSizer4.Add( self.uifMGapW, 0, wx.ALL, 5 )
        
        self.in_uifMGapW = wx.TextCtrl( self.userInputM, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer4.Add( self.in_uifMGapW, 0, wx.ALL, 5 )
        
        self.uifMGapH = wx.StaticText( self.userInputM, wx.ID_ANY, u"Magnetic Gap Height", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifMGapH.Wrap( -1 )
        gSizer4.Add( self.uifMGapH, 0, wx.ALL, 5 )
        
        self.in_uifMGapH = wx.TextCtrl( self.userInputM, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer4.Add( self.in_uifMGapH, 0, wx.ALL, 5 )
        
        self.uifMGapRing = wx.StaticText( self.userInputM, wx.ID_ANY, u"Shorting Ring?", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifMGapRing.Wrap( -1 )
        gSizer4.Add( self.uifMGapRing, 0, wx.ALL, 5 )
        
        self.in_uifMGapRing = wx.CheckBox( self.userInputM, wx.ID_ANY, u"Yes", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer4.Add( self.in_uifMGapRing, 0, wx.ALL, 5 )
        
        self.uifMFlux = wx.StaticText( self.userInputM, wx.ID_ANY, u"Flux Density", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifMFlux.Wrap( -1 )
        gSizer4.Add( self.uifMFlux, 0, wx.ALL, 5 )
        
        self.in_uifMFlux = wx.TextCtrl( self.userInputM, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer4.Add( self.in_uifMFlux, 0, wx.ALL, 5 )
        
        
        self.userInputM.SetSizer( gSizer4 )
        self.userInputM.Layout()
        gSizer4.Fit( self.userInputM )
        mainFrameSizer.Add( self.userInputM, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )
        
        self.userInputC = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        gSizer5 = wx.GridSizer( 0, 4, 0, 0 )
        
        self.uifCTitle = wx.StaticText( self.userInputC, wx.ID_ANY, u"Moving Mass Parameters", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifCTitle.Wrap( -1 )
        gSizer5.Add( self.uifCTitle, 0, wx.ALL, 5 )
        
        self.m_staticText35 = wx.StaticText( self.userInputC, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText35.Wrap( -1 )
        gSizer5.Add( self.m_staticText35, 0, wx.ALL, 5 )
        
        self.m_staticText36 = wx.StaticText( self.userInputC, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText36.Wrap( -1 )
        gSizer5.Add( self.m_staticText36, 0, wx.ALL, 5 )
        
        self.m_staticText37 = wx.StaticText( self.userInputC, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText37.Wrap( -1 )
        gSizer5.Add( self.m_staticText37, 0, wx.ALL, 5 )
        
        self.uifCMass = wx.StaticText( self.userInputC, wx.ID_ANY, u"Cone Mass", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifCMass.Wrap( -1 )
        gSizer5.Add( self.uifCMass, 0, wx.ALL, 5 )
        
        self.in_uifCMass = wx.TextCtrl( self.userInputC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer5.Add( self.in_uifCMass, 0, wx.ALL, 5 )
        
        self.uifCRms = wx.StaticText( self.userInputC, wx.ID_ANY, u"Rms", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifCRms.Wrap( -1 )
        gSizer5.Add( self.uifCRms, 0, wx.ALL, 5 )
        
        self.in_uifCRms = wx.TextCtrl( self.userInputC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer5.Add( self.in_uifCRms, 0, wx.ALL, 5 )
        
        self.uifCCms = wx.StaticText( self.userInputC, wx.ID_ANY, u"Cms", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.uifCCms.Wrap( -1 )
        gSizer5.Add( self.uifCCms, 0, wx.ALL, 5 )
        
        self.in_uifCCms = wx.TextCtrl( self.userInputC, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        gSizer5.Add( self.in_uifCCms, 0, wx.ALL, 5 )
        
        
        self.userInputC.SetSizer( gSizer5 )
        self.userInputC.Layout()
        gSizer5.Fit( self.userInputC )
        mainFrameSizer.Add( self.userInputC, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )
        
        self.userInputBut = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer41 = wx.GridSizer( 0, 3, 0, 0 )
        
        self.in_bRunGm = wx.Button( self.userInputBut, wx.ID_ANY, u"Run Geometry", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer41.Add( self.in_bRunGm, 0, wx.ALL, 5 )
        
        self.in_bRunCmp = wx.Button( self.userInputBut, wx.ID_ANY, u"Run Solution", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer41.Add( self.in_bRunCmp, 0, wx.ALL, 5 )
        
        self.in_bRunClear = wx.Button( self.userInputBut, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer41.Add( self.in_bRunClear, 0, wx.ALL, 5 )
        
        
        self.userInputBut.SetSizer( gSizer41 )
        self.userInputBut.Layout()
        gSizer41.Fit( self.userInputBut )
        mainFrameSizer.Add( self.userInputBut, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )
        
        self.userOutput = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText44 = wx.StaticText( self.userOutput, wx.ID_ANY, u"Output", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText44.Wrap( -1 )
        bSizer2.Add( self.m_staticText44, 0, wx.ALL, 5 )
        
        self.out_uifReport = wx.StaticText( self.userOutput, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,580 ), 0|wx.SUNKEN_BORDER|wx.VSCROLL )
        self.out_uifReport.Wrap( -1 )
        self.out_uifReport.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
        self.out_uifReport.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        font = wx.Font(12, wx.SCRIPT, wx.NORMAL, wx.NORMAL)
        self.out_uifReport.SetFont(font)
        
        bSizer2.Add( self.out_uifReport, 0, wx.ALL, 5 )
        
        
        self.userOutput.SetSizer( bSizer2 )
        self.userOutput.Layout()
        bSizer2.Fit( self.userOutput )
        mainFrameSizer.Add( self.userOutput, wx.GBPosition( 0, 1 ), wx.GBSpan( 3, 1 ), wx.EXPAND |wx.ALL, 5 )
        
        self.userOutputB = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER )
        gSizer51 = wx.GridSizer( 0, 0, 0, 0 )
        
        self.in_uifSaveReport = wx.Button( self.userOutputB, wx.ID_ANY, u"Save Report", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer51.Add( self.in_uifSaveReport, 0, wx.ALL, 5 )
        
        
        self.userOutputB.SetSizer( gSizer51 )
        self.userOutputB.Layout()
        gSizer51.Fit( self.userOutputB )
        mainFrameSizer.Add( self.userOutputB, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND |wx.ALL, 5 )
        
        
        self.SetSizer( mainFrameSizer )
        
        # Names
        self.in_uifVCTypeNo.SetName(u"in_uifVCTypeNo")
        self.in_uifVCMeanDia.SetName(u"in_uifVCMeanDia")
        self.in_uifVCFormerTh.SetName(u"in_uifVCFormerTh")
        self.in_uifVCFormerMAt.SetName(u"in_uifVCFormerMAt")
        self.in_uifVCFormerIn.SetName(u"in_uifVCFormerIn")
        self.in_uifVCFormerOut.SetName(u"in_uifVCFormerOut")
        self.in_uifVCFormerHi.SetName(u"in_uifVCFormerHi")
        self.in_uifVCFormerMass.SetName(u"in_uifVCFormerMass")
        self.in_uifVCWireMat.SetName(u"in_uifVCWireMat")
        self.in_uifVCWireDia.SetName(u"in_uifVCWireDia")
        self.in_uifVCTurns.SetName(u"in_uifVCTurns")
        self.in_uifVCLayers.SetName(u"in_uifVCLayers")
        self.in_uifVCWindingHi.SetName(u"in_uifVCWindingHi")
        self.in_uifVCWindingTy.SetName(u"in_uifVCWindingTy")
        self.in_uifVCWireLen.SetName(u"in_uifVCWireLen")
        self.in_uifVCInDia.SetName(u"in_uifVCInDia")
        self.in_uifVCOutDia.SetName(u"in_uifVCOutDia")
        self.in_uifVCMass.SetName(u"in_uifVCMass")
        self.in_uifVCDCRes.SetName(u"in_uifVCDCRes")
        self.in_uifVCLe.SetName(u"in_uifVCLe")
        self.in_uifMType.SetName(u"in_uifMType")
        self.in_uifMSteel.SetName(u"in_uifMSteel")
        self.in_uifMGapType.SetName(u"in_uifMGapType")
        self.in_uifMGapW.SetName(u"in_uifMGapW")
        self.in_uifMGapH.SetName(u"in_uifMGapH")
        self.in_uifMGapRing.SetName(u"in_uifMGapRing")
        self.in_uifMFlux.SetName(u"in_uifMFlux")
        self.in_uifCMass.SetName(u"in_uifCMass")
        self.in_uifCRms.SetName(u"in_uifCRms")             
        self.in_uifCCms.SetName(u"in_uifCCms")  
                
        # Connect Events
        self.Bind( wx.EVT_MENU, self.OnQuit, id = self.mExit.GetId() )
        #self.in_uifVCTypeNo.Bind( wx.EVT_CHOICE, self.updFields )
        self.in_uifVCMeanDia.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCFormerTh.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        #self.in_uifVCFormerMAt.Bind( wx.EVT_CHOICE, self.updFields )
        self.in_uifVCFormerIn.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCFormerOut.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCFormerHi.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCFormerMass.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        #self.in_uifVCWireMat.Bind( wx.EVT_CHOICE, self.updFields )
        self.in_uifVCWireDia.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCTurns.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCLayers.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCWindingHi.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        #self.in_uifVCWindingTy.Bind( wx.EVT_CHOICE, self.updFields )
        self.in_uifVCWireLen.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCInDia.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCOutDia.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCMass.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCDCRes.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_uifVCLe.Bind( wx.EVT_TEXT_ENTER, self.updFields )
        self.in_bRunGm.Bind( wx.EVT_BUTTON, self.OnGeometry )
        self.in_bRunCmp.Bind( wx.EVT_BUTTON, self.OnCompute )
        
        self.Layout()    
        
    def calc_callback(self, data):
        for k,v in data.iteritems():
            field = getattr(self, k)
            if isinstance(field, wx.TextCtrl):
                field.SetValue(str(v))
    def log(self, text):
        cur_text = self.out_uifReport.GetLabel()
        self.out_uifReport.SetLabel(cur_text+"\n"+text)
            
    def OnQuit(self, event):
        self.Close()  
        
    def OnNew(self, event):
        self.drawMainPanel()
        
    def OnGeometry(self, event):
        self.proc.setData(self.fetchVCData(), self.fetchMotorData(), self.fetchConeData())
        self.proc.calcGmVC()
        
    def OnCompute(self, event):
        self.proc.calcMImp()
        
    def updFields(self, event):
        ev_source = event.GetEventObject().GetName()    
        print ev_source
        controls = [widget.GetName() for widget in self.userInputVC.GetChildren() if isinstance(widget, wx.TextCtrl)]
        next_ctrl_index = controls.index(ev_source)+1        
        if next_ctrl_index == len(controls):
            next_ctrl_index = 0
        next_ctrl = getattr(self, controls[next_ctrl_index])    
        next_ctrl.SetFocus()        
        
    def fetchVCData(self):
        data = {}
        dataforms = [widget for widget in self.userInputVC.GetChildren() if isinstance(widget, wx.TextCtrl) or isinstance(widget, wx.Choice)]
        for entry in dataforms:
            if isinstance(entry, wx.TextCtrl):
                data[entry.GetName()] = float(entry.GetValue())
            else:
                data[entry.GetName()] = entry.GetString(entry.GetSelection())
        return data
            
    def fetchMotorData(self):
        data = {}
        dataforms = [widget for widget in self.userInputM.GetChildren() if isinstance(widget, wx.TextCtrl) or isinstance(widget, wx.Choice)]
        for entry in dataforms:
            if isinstance(entry, wx.TextCtrl):
                data[entry.GetName()] = float(entry.GetValue())
            else:
                data[entry.GetName()] = entry.GetString(entry.GetSelection())
        return data
    
    def fetchConeData(self):
        data = {}
        dataforms = [widget for widget in self.userInputC.GetChildren() if isinstance(widget, wx.TextCtrl) or isinstance(widget, wx.Choice)]
        for entry in dataforms:
            if isinstance(entry, wx.TextCtrl):
                data[entry.GetName()] = float(entry.GetValue())
            else:
                data[entry.GetName()] = entry.GetString(entry.GetSelection())
        return data