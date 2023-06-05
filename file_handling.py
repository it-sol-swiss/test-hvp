import pandas as pd

from app.utils import logger as logger

log = logger.Logger()


class BatterySelection:
    """
    This module defines the battery according to a csv file
    """

    def __init__(self, file_path):
        self.battery_config = pd.read_csv(file_path)

        self.Aircraft = self.battery_config['Aircraft'].iloc[0]
        self.Battery_Type = self.battery_config['Battery Type'].iloc[0]
        self.Cell_Configuration = self.battery_config['Cell Configuration'].iloc[0]
        self.BMS = self.battery_config['BMS'].iloc[0]
        self.Nominal_Capacity = self.battery_config['Nominal Capacity'].iloc[0]
        self.V_max = self.battery_config['V max'].iloc[0]
        self.V_min = self.battery_config['V min'].iloc[0]
        self.I_max = self.battery_config['I max'].iloc[0]
        self.Cell_V_max = self.battery_config['Cell V max'].iloc[0]
        self.Cell_V_min = self.battery_config['Cell V min'].iloc[0]
        self.T_max_Discharge = self.battery_config['T max Discharge'].iloc[0]
        self.T_min = self.battery_config['T min'].iloc[0]
        self.Test_V_max = self.battery_config['Test V max'].iloc[0]
        self.Test_V_min = self.battery_config['Test V min'].iloc[0]
        self.Test_I = self.battery_config['Test I'].iloc[0]
        self.Break = self.battery_config['Break'].iloc[0]
        self.Remark = self.battery_config['Remark'].iloc[0]
        




    def log(self, level=0):
        if level == 0:
            pass
        elif level == 1:
            log.log('\nAircraft ' + str(self.Aircraft) + ', \n' +
                    'Battery Type ' + str(self.Battery_Type) + ', \n' +
                    'Cell Configuration ' + str(self.Cell_Configuration) + ', \n' +
                    'BMS ' + str(self.BMS) + ', \n' +
                    'Nominal Capacity  ' + str(self.Nominal_Capacity) + ' [kWh], \n' +
                    'V max ' + str(self.V_max) + '[V], \n' +
                    'V_min  ' + str(self.V_min) + ' [V], \n' +
                    'I_max  ' + str(self.I_max) + ' [A], \n' +
                    'Cell_V_max  ' + str(self.Cell_V_max) + ' [V], \n' +
                    'Cell_V_min  ' + str(self.Cell_V_min) + ' [V], \n' +
                    'T_max_[°C]_Discharge  ' + str(self.T_max_Discharge) + ' [°C], \n' +
                    'T_min  ' + str(self.T_min) + ' [°C], \n' +
                    'Test_V_max  ' + str(self.Test_V_max) + ' [V], \n' +
                    'Test_V_min  ' + str(self.Test_V_min) + ' [V], \n' +
                    'Test_I  ' + str(self.Test_I) + ' [A], \n' +
                    'Break  ' + str(self.Break) + ' [h], \n' +
                    'Remark  ' + str(self.Remark) 
                    
                    )
        else:
            pass



    # Getters
    @property
    def Cell_Configuration(self):
        return self._Cell_Configuration

    @property
    def Nominal_Capacity(self):
        return self._Nominal_Capacity

    @property
    def V_max(self):
        return self._V_max

    @property
    def V_min(self):
        return self._V_min

    @property
    def Test_V_max(self):
        return self._Test_V_max

    @property
    def Test_V_min(self):
        return self._Test_V_min

    @property
    def Test_I(self):
        return self._Test_I

    # Setters
    @Cell_Configuration.setter
    def Cell_Configuration(self, value):
        self._Cell_Configuration = value

    @Nominal_Capacity.setter
    def Nominal_Capacity(self, value):
        self._Nominal_Capacity = value

    @V_max.setter
    def V_max(self, value):
        self._V_max = value

    @V_min.setter
    def V_min(self, value):
        self._V_min = value

    @Test_V_max.setter
    def Test_V_max(self, value):
        self._Test_V_max = value

    @Test_V_min.setter
    def Test_V_min(self, value):
        self._Test_V_min = value

    @Test_I.setter
    def Test_I(self, value):
        self._Test_I = value