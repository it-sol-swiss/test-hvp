import re
import time
import warnings

from app.utils import logger as logger

log = logger.Logger()




# Testing with file

class Battery:
    """
    This module provides safe methods to initialize, charge and discharge the batteries,
    based on given battery parameters (values in mAh)
    """

    def __init__(self, batterySelection, charger):
        """
        Creates battery with methods to load and charge, capacity given in mAh
        :param batterySelection: BatterySelection object containing battery parameters
        """

        time.sleep(1.0)

        self.charger = charger

        self.Cell_Configuration = batterySelection.Cell_Configuration
        self.Nominal_Capacity = batterySelection.Nominal_Capacity
        self.V_max = batterySelection.V_max
        self.V_min = batterySelection.V_min
        self.Test_V_max = batterySelection.Test_V_max
        self.Test_V_min = batterySelection.Test_V_min
        self.Test_I = batterySelection.Test_I

        self.charge_limit = self.Test_I  # [A]
        self.discharge_limit = self.Test_I  # [A]

        config = re.split('[SP]', batterySelection.Cell_Configuration)
        self.serial_cells = int(config[0])
        self.parallel_cells = int(config[1])

        batterySelection.log(1)


    def print_battery_values(self):
        print("Cell Configuration:", self.Cell_Configuration)
        print("Nominal Capacity:", self.Nominal_Capacity)
        print("V max:", self.V_max)
        print("V min:", self.V_min)
        print("Test V max:", self.Test_V_max)
        print("Test V min:", self.Test_V_min)
        print("Test I:", self.Test_I)
        print("Charge Limit:", self.charge_limit)
        print("Discharge Limit:", self.discharge_limit)
        print("serial_cells:", self.serial_cells)
        print("parallel_cells:", self.parallel_cells)

    """
    def __init__(self, config="1s1p", cell_capacity=3120.0, max_charge_cell=5.0, max_discharge_cell=30.0):
    
    Creates battery with methods to load and charge, capacity given in mAh
    :param config: Cell configuration, i.e. 38s5p for 38 serial packs of 5 parallel cells
    :param cell_capacity: Capacity per cell in [mAh]
    :param max_charge_cell: Continuous maximum charge current in [A]
    :param max_discharge_cell: Continuous maximum discharge current in [A]
    

    time.sleep(1.0)


    self.configuration = config
    config = re.split('[sp]', config)
    self.serial_cells = int(config[0])
    self.parallel_cells = int(config[1])

    self.nominal_voltage = 3.6 * int(self.serial_cells)  # [V]
    #self.nominal_capacity = cell_capacity / 1000 * self.parallel_cells  # [Ah]
    #self.nominal_capacity = nominal_capacity
    self.charge_limit = max_charge_cell * self.parallel_cells  # [A]
    self.discharge_limit = max_discharge_cell * self.parallel_cells  # [A]
    """

    def cap_test_charge(self):
        self.charge(charger=self.charger, u_end=self.Test_V_max*0.9, i_max=self.Test_I)

    def cap_test_discharge(self):
        self.discharge(charger=self.charger, u_end= self.Test_V_min, i_max= -self.Test_I)

    def cap_test_balancing(self):
        self.charge(charger=self.charger, u_end=self.Test_V_max, i_max=1)

    def cap_test(self):
        time.sleep(1)
        self.cap_test_discharge()
        self.cap_test_charge()
        self.cap_test_balancing()
        self.cap_test_discharge()

    def full_charge(self):
        time.sleep(1)
        self.cap_test_charge()

    def storage_charge(self):
        time.sleep(1)
        storage_capacity = self.Nominal_Capacity * 0.6

    def charge(self, charger, u_end, i_max):
        # Define cell limits
        max_charge_voltage = self.V_max  # [V]
        min_cutoff_voltage = self.V_min  # [V]
        cell_end_current = 0.1  # [A]

        # Check limits and adjust input
        if u_end > max_charge_voltage:
            u_end = max_charge_voltage
            warnings.warn('Charge end voltage exceeding limit!\n'
                          'Value reduced to limit at ' + str(round(u_end, 2)) + ' [V]')
        if u_end < min_cutoff_voltage:
            u_end = min_cutoff_voltage
            warnings.warn('Charge end voltage exceeding limit!\n'
                          'Value reduced to limit at ' + str(round(u_end, 2)) + ' [V]')

        if i_max > self.charge_limit:
            i_max = self.charge_limit
            warnings.warn('Maximum current exceeding limit!\n'
                          'Value reduced to limit at ' + str(round(self.charge_limit, 2)) + ' [A]')

        # Check idle voltage
        charger.set_output(state=False)
        time.sleep(1)  # Wait n seconds to relax voltage
        idle_voltage = charger.measure_voltage()  # momentane Volt auf battery

        # Config charger
        charger.set_current(i=i_max)
        charger.set_current_neg(i=0)

        power_tolerance = 1.1  # [1] Power limit is set higher with minimal tolerance (current guided charging)
        p_max = power_tolerance * u_end * i_max
        charger.set_power(p=p_max)
        charger.set_power_neg(p=0)

        charge_voltage = u_end
        charger.set_voltage(u=charge_voltage)  #

        # Reset instruments
        charger.instrument(inst='Ah', op='ON')
        charger.instrument(inst='Wh', op='ON')

        # Start charging
        start_time = time.time()
        charge = True

        log.log('=================================================')
        log.log('Starting charging process')
        log.log('Start voltage ' + str(round(idle_voltage, 2)) + ' [V]')
        log.log('End voltage ' + str(round(u_end, 2)) + ' [V]')
        log.log('Current ' + str(round(i_max, 2)) + ' [A]')
        log.log('-------------------------------------------------')
        log.log('Time [s] | Voltage [V] | Current [A] ')

        charger.set_output(state=True)
        time.sleep(0.1)
        log.log(str(round(time.time() - start_time)) + ' ' +
                str(round(idle_voltage, 2)) + ' ' +
                str(round(charger.measure_current(), 2)))

        cycle_time = time.time()

        try:
            while charge:
                # Every 10 seconds, check voltage
                if time.time() - cycle_time >= 10:
                    cycle_time = time.time()
                    charge_current = charger.measure_current()
                    charger.set_output(state=False)
                    time.sleep(0.2)  # Wait n seconds for voltage to relax
                    idle_voltage = charger.measure_voltage()
                    charger.set_output(state=True)
                    if idle_voltage >= u_end or charge_current < cell_end_current * self.parallel_cells:
                        charge = False
                    log.log(str(round(time.time() - start_time)) + '  ' +
                            str(round(idle_voltage, 2)) + ' ' +
                            str(round(charge_current, 2)))


                else:
                    charger.feed_watchdog()

        except KeyboardInterrupt:
            pass

        charger.set_output(state=False)

        # Read and stop instruments
        # charge_ah_pos = charger.instrument(inst='Ah', op='READ_POS')
        charge_wh_pos = charger.instrument(inst='Wh', op='READ_POS')
        # charge_ah_neg = charger.instrument(inst='Ah', op='READ_NEG')
        # charge_wh_neg = charger.instrument(inst='Wh', op='READ_NEG')

        charger.instrument(inst='Ah', op='OFF')
        charger.instrument(inst='Wh', op='OFF')

        log.log('-------------------------------------------------')
        log.log('Stopping charging process')
        log.log('Charged ' + str(round(charge_wh_pos, 3)) + ' Wh')


    def discharge(self, charger, u_end=2.5, i_max=1.0):
        # Define cell limits
        max_charge_voltage = self.V_max  # [V]
        min_cutoff_voltage = self.V_min  # [V]
        cell_end_current = 0.1  # [A]

        # Check limits and adjust input
        if u_end > max_charge_voltage:
            u_end = max_charge_voltage
            warnings.warn('Cutoff voltage exceeding limit!\n'
                          'Value relaxed to limit at ' + str(round(u_end, 2)) + ' [V]')
        if u_end < min_cutoff_voltage:
            u_end = min_cutoff_voltage
            warnings.warn('Cutoff voltage exceeding limit!\n'
                          'Value relaxed to limit at ' + str(round(u_end, 2)) + ' [V]')

        if -i_max > self.discharge_limit:
            i_max = -self.discharge_limit
            warnings.warn('Maximum current exceeding limit!\n'
                          'Value reduced to limit at ' + str(round(self.discharge_limit, 2)) + ' [A]')

        # Check idle voltage
        charger.set_output(state=False)
        time.sleep(1)  # Wait n seconds to relax voltage
        idle_voltage = charger.measure_voltage()

        # Config charger
        charger.set_current(i=0)
        charger.set_current_neg(i=i_max)

        power_tolerance = 1.1  # [1] Power limit is set higher with minimal tolerance (current guided charging)
        p_max = power_tolerance * max_charge_voltage * i_max
        charger.set_power(p=0)
        charger.set_power_neg(p=p_max)

        discharge_voltage = u_end
        charger.set_voltage(u=discharge_voltage)

        # Reset instruments
        charger.instrument(inst='Ah', op='ON')
        charger.instrument(inst='Wh', op='ON')

        # Start discharging
        start_time = time.time()
        discharge = True

        log.log('=================================================')
        log.log('Starting discharging process')
        log.log('Start voltage ' + str(round(idle_voltage, 2)) + ' [V]')
        log.log('End voltage ' + str(round(u_end, 2)) + ' [V]')
        log.log('Current ' + str(round(i_max, 2)) + ' [A]')
        log.log('-------------------------------------------------')
        log.log('Time [s] | Voltage [V] | Current [A] ')

        charger.set_output(state=True)
        log.log(str(round(time.time() - start_time)) + ' ' +
                str(round(idle_voltage, 2)) + ' ' +
                str(round(charger.measure_current(), 2)))

        cycle_time = time.time()
        try:
            while discharge:
                # Every 10 seconds, check voltage
                if time.time() - cycle_time >= 10:
                    cycle_time = time.time()
                    discharge_current = charger.measure_current()
                    charger.set_output(state=False)
                    time.sleep(0.2)  # Wait n seconds for voltage to relax
                    idle_voltage = charger.measure_voltage()
                    charger.set_output(state=True)
                    if idle_voltage <= u_end or discharge_current > cell_end_current * self.parallel_cells:
                        discharge = False
                    log.log(str(round(time.time() - start_time)) + ' ' +
                            str(round(idle_voltage, 2)) + ' ' +
                            str(round(discharge_current, 2)))
                    # cycle_time * idle_voltage * discharge ----> um eine genauere berechnung zu erhalten als nur vom netzteil.

                else:
                    charger.feed_watchdog()

        except KeyboardInterrupt:
            pass

        charger.set_output(state=False)

        # Read and stop instruments
        # charge_ah_pos = charger.instrument(inst='Ah', op='READ_POS')
        # charge_wh_pos = charger.instrument(inst='Wh', op='READ_POS')
        # charge_ah_neg = charger.instrument(inst='Ah', op='READ_NEG')
        charge_wh_neg = charger.instrument(inst='Wh', op='READ_NEG')

        charger.instrument(inst='Ah', op='OFF')
        charger.instrument(inst='Wh', op='OFF')

        log.log('-------------------------------------------------')
        log.log('Stopping discharging process')
        log.log('Discharged ' + str(round(charge_wh_neg, 3)) + ' Wh')
