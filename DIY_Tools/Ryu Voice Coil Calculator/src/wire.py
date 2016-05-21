class Wire:
    density_array = {
                   'ECW': 8.96,
                   'ECCAW': 3.7,
                   'EAW': 2.7
                   }
    resistivity_array = {
                       'ECW': 0.017,
                       'ECCAW': 0.0255,
                       'EAW': 0.0282
                       }
    def __init__(self, type):
        self.density = self.density_array[type]
        self.resistivity = self.resistivity_array[type]