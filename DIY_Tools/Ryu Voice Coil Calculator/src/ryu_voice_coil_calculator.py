# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import wx
from gui import *

class RyuVCCalculator(wx.App):
    def OnInit(self):
        frame = MainWindow(None)
        frame.Show(True)
        return True
    
def main():  
    app = RyuVCCalculator(0)
    app.MainLoop()

if __name__ == "__main__":
    main()
