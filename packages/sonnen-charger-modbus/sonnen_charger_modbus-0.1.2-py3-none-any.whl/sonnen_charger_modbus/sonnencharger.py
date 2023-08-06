
import datetime
import time
from struct import *

from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from pymodbus.constants import Endian
from enum import Enum

# Real time values
ADDR_CONNNECTOR_STATUS_BASE = 0
ADDR_MEASURED_VEHICLE_NUMBER_OF_PHASES_BASE = 1
ADDR_EV_MAX_PHASE_CURRENT_BASE = 2
ADDR_TARGET_CURRENT_FROM_POWER_MGM_OR_MODBUS_BASE = 4
ADDR_FREQUENCY_BASE = 6
ADDR_L_N_VOLTAGE_L1_BASE = 8
ADDR_L_N_VOLTAGE_L2_BASE = 10
ADDR_L_N_VOLTAGE_L3_BASE = 12
ADDR_CURENT_L1_BASE = 14
ADDR_CURENT_L2_BASE = 16
ADDR_CURENT_L3_BASE = 18
ADDR_ACTIVE_POWER_L1_BASE = 20
ADDR_ACTIVE_POWER_L2_BASE = 22
ADDR_ACTIVE_POWER_L3_BASE = 24
ADDR_ACTIVE_POWER_TOTAL_BASE = 26
ADDR_POWER_FACTOR_BASE = 28
ADDR_TOTAL_IMPORTED_ACTIVE_ENERGY_IN_RUNNING_SESSION_BASE = 30
ADDR_RUNNING_SESSION_DURATION_BASE = 32
ADDR_RUNNING_SESSION_DEPARTURE_TIME_BASE = 36
ADDR_RUNNING_SESSION_ID_BASE = 40
ADDR_EV_MAX_POWER_BASE = 44
ADDR_EV_PLANNED_ENERGY_BASE = 46

# Charger Settings
ADDR_SERIAL_NUMBER = 990
ADDR_MODEL = 1000
ADDR_HW_VERSION = 1010
ADDR_SW_VERSION = 1015
ADDR_NUMBER_OF_CONNECTORS = 1020
ADDR_CONNECTOR_TYPE_BASE = 1022
ADDR_NUMBER_PHASES_BASE = 1023
ADDR_L1_CONNECTED_TO_PHASE_BASE = 1024
ADDR_L2_CONNECTED_TO_PHASE_BASE = 1025
ADDR_L3_CONNECTED_TO_PHASE_BASE = 1026
ADDR_CUSTOM_MAX_CURRENT_BASE = 1028

# Write Registers
ADDR_STOP_CHARGING_BASE = 1
ADDR_PAUSE_CHARGING_BASE = 2
ADDR_SET_DEPARTURE_TIME_BASE = 4
ADDR_SET_CURRENT_SETPOINT_BASE = 8
ADDR_CANCEL_CURRENT_SETPOINT_BASE = 10
ADDR_SET_POWER_SETPOINT_BASE = 11
ADDR_CANCEL_POWER_SETPOINT_BASE = 13
ADDR_SET_TIME = 1000
ADDR_RESTART = 1004

class ChargerConnector(Enum):
    SocketType2 = 1
    CableType2 = 2
    UnknownConnectorType = 3

class ChargerConnectorStatus(Enum):
    Available = 1
    ConnectTheCable = 2
    WaitingForVehicleToRespond = 3
    Charging = 4
    VehicleHasPausedCharging = 5
    EVSEHasPausedCharging = 6
    ChargingHasBeenEnded = 7
    ChargingFault = 8
    UnpausingCharging = 9
    Unavailable = 10
    UnknownStatus = 11

class ChargerPhaseCount(Enum):
    ThreePhases = 1
    SinglePhaseL1 = 2
    SinglePhaseL2 = 3
    SinglePhaseL3 = 4
    TwoPhases = 5
    UnknownNumberOfPhases = 6


def toFloat(reg) -> float:
    return unpack('>f', pack('>HH', reg[0], reg[1]))[0]

def toString(reg, size = 20) -> str:
    decoder = BinaryPayloadDecoder.fromRegisters(reg)
    return str(decoder.decode_string(size).decode("utf-8"))

def wrapInt64(self, value):
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
    builder.add_64bit_int(value)
    return builder.build()

def wrapFloat(self, value):
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
    builder.add_32bit_float(value)
    return builder.build()
    

class Charger:
    """
    Connection to charger using Modbus.
    NOTE: Make sure to wrap all calls inside try: except clause as all methods might throw on connection issues.
    Clean up on end: close()
    """
    def __init__(self, ip, port = 502):
        self.ip = ip
        self.port = port
        self.client = ModbusTcpClient(ip, port)

    def readSerialNumber(self) -> str:
        """ Serial number """
        response = self.client.read_input_registers(address=ADDR_SERIAL_NUMBER, count=10)
        return toString(response.registers)

    def readModel(self) -> str:
        """ Model """
        response = self.client.read_input_registers(address=ADDR_MODEL, count=10)
        return toString(response.registers)

    def readHWVersion(self) -> str:
        """ HW version """
        response = self.client.read_input_registers(address=ADDR_HW_VERSION, count=5)
        return toString(response.registers)

    def readSWVersion(self) -> str:
        """ SW version """
        response = self.client.read_input_registers(address=ADDR_SW_VERSION, count=5)
        return toString(response.registers)

    def readNumberOfConnectors(self) -> int:
        """ Number of connectors """
        response = self.client.read_input_registers(address=ADDR_NUMBER_OF_CONNECTORS, count=2)
        return int(response.registers[0])

    def readConnectorType(self, connector = 0) -> ChargerConnector:
        """ Connector Connector type """
        response = self.client.read_input_registers(address=ADDR_CONNECTOR_TYPE_BASE + connector * 100, count=1)

        if str(response.registers) == str([1]):
            return ChargerConnector.SocketType2
        elif str(response.registers) == str([2]):
            return ChargerConnector.CableType2
        else:
            return ChargerConnector.UnknownConnectorType

    def readNumberOfPhases(self, connector = 0) -> int:
        """ Connector Number phases """
        response = self.client.read_input_registers(address=ADDR_NUMBER_PHASES_BASE + connector*100, count=1)
        return int(response.registers[0])

    def readL1ConToPhase(self, connector = 0) -> int:
        """ Connector L1 connected to phase """
        response = self.client.read_input_registers(address=ADDR_L1_CONNECTED_TO_PHASE_BASE + connector*100, count=1)
        return int(response.registers[0])

    def readL2ConToPhase(self, connector = 0) -> int:
        """ Connector L2 connected to phase """
        response = self.client.read_input_registers(address=ADDR_L2_CONNECTED_TO_PHASE_BASE + connector*100, count=1)
        return int(response.registers[0])

    def readL3ConToPhase(self, connector = 0) -> int:
        """ Connector L3 connected to phase """
        response = self.client.read_input_registers(address=ADDR_L3_CONNECTED_TO_PHASE_BASE + connector*100, count=1)
        return int(response.registers[0])

    def readCustomMaxCurrent(self, connector = 0) -> float:
        """ Connector Custom max current in A """
        response = self.client.read_input_registers(address=ADDR_CUSTOM_MAX_CURRENT_BASE + connector*100, count=2)
        return toFloat(response.registers)

    def readConStatus(self, connector = 0) -> ChargerConnectorStatus:
        """ Connector status """
        response = self.client.read_input_registers(address=ADDR_CONNNECTOR_STATUS_BASE + connector * 100, count=1)

        if str(response.registers) == str([1]):
            return ChargerConnectorStatus.Available
        elif str(response.registers) == str([2]):
            return ChargerConnectorStatus.ConnectTheCable
        elif str(response.registers) == str([3]):
            return ChargerConnectorStatus.WaitingForVehicleToRespond
        elif str(response.registers) == str([4]):
            return ChargerConnectorStatus.Charging
        elif str(response.registers) == str([5]):
            return ChargerConnectorStatus.VehicleHasPausedCharging
        elif str(response.registers) == str([6]):
            return ChargerConnectorStatus.EVSEHasPausedCharging
        elif str(response.registers) == str([7]):
            return ChargerConnectorStatus.ChargingHasBeenEnded
        elif str(response.registers) == str([8]):
            return ChargerConnectorStatus.ChargingFault
        elif str(response.registers) == str([9]):
            return ChargerConnectorStatus.UnpausingCharging
        elif str(response.registers) == str([10]):
            return ChargerConnectorStatus.Unavailable
        else:
            return ChargerConnectorStatus.UnknownStatus

    def readVehiclePhaseCount(self, connector = 0) -> ChargerPhaseCount:
        """ Connector Measured vehicle number of phases """
        response = self.client.read_input_registers(address=ADDR_MEASURED_VEHICLE_NUMBER_OF_PHASES_BASE + connector * 100, count=1)

        if str(response.registers) == str([0]):
            return ChargerPhaseCount.ThreePhases
        elif str(response.registers) == str([1]):
            return ChargerPhaseCount.SinglePhaseL1
        elif str(response.registers) == str([2]):
            return ChargerPhaseCount.SinglePhaseL2
        elif str(response.registers) == str([3]):
            return ChargerPhaseCount.SinglePhaseL3
        elif str(response.registers) == str([4]):
            return ChargerPhaseCount.UnknownNumberOfPhases
        elif str(response.registers) == str([5]):
            return ChargerPhaseCount.TwoPhases
        else:
            return ChargerPhaseCount.UnknownNumberOfPhases

    def readVehicleMaxCurrent(self, connector = 0) -> float:
        """ Connector EV max phase current in A """
        response = self.client.read_input_registers(address=ADDR_EV_MAX_PHASE_CURRENT_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readTargetCurrentFromPowerMgmOrModbus(self, connector = 0) -> float:
        """ Connector Target current from power mgm or modbus in A """
        response = self.client.read_input_registers(address=ADDR_TARGET_CURRENT_FROM_POWER_MGM_OR_MODBUS_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readFrequency(self, connector = 0) -> float:
        """ Frequency in Hz """
        response = self.client.read_input_registers(address=ADDR_FREQUENCY_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readLNVoltageL1(self, connector = 0) -> float:
        """ Connector L-N voltage (L1) in V """
        response = self.client.read_input_registers(address=ADDR_L_N_VOLTAGE_L1_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readLNVoltageL2(self, connector = 0) -> float:
        """ Connector L-N voltage (L2) in V """
        response = self.client.read_input_registers(address=ADDR_L_N_VOLTAGE_L2_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readLNVoltageL3(self, connector = 0) -> float:
        """ Connector L-N voltage (L3) in V """
        response = self.client.read_input_registers(address=ADDR_L_N_VOLTAGE_L3_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readCurrentL1(self, connector = 0) -> float:
        """ Connector Current (L1) in A """
        response = self.client.read_input_registers(address=ADDR_CURENT_L1_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readCurrentL2(self, connector = 0) -> float:
        """ Connector Current (L2) in A """
        response = self.client.read_input_registers(address=ADDR_CURENT_L2_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readCurrentL3(self, connector = 0) -> float:
        """ Connector Current (L3) in A """
        response = self.client.read_input_registers(address=ADDR_CURENT_L3_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readActivePowerL1(self, connector = 0) -> float:
        """ Connector Active power (L1) in kW """
        response = self.client.read_input_registers(address=ADDR_ACTIVE_POWER_L1_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readActivePowerL2(self, connector = 0) -> float:
        """ Connector Active power (L2) in kW """
        response = self.client.read_input_registers(address=ADDR_ACTIVE_POWER_L2_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readActivePowerL3(self, connector = 0) -> float:
        """ Connector Active power (L3) in kW """
        response = self.client.read_input_registers(address=ADDR_ACTIVE_POWER_L3_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readActivePowerTotal(self, connector = 0) -> float:
        """ Connector Active power (total) in kW """
        response = self.client.read_input_registers(address=ADDR_ACTIVE_POWER_TOTAL_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readPowerFactor(self, connector = 0) -> float:
        """ Connector Power factor """
        response = self.client.read_input_registers(address=ADDR_POWER_FACTOR_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readEnergyInActiveSession(self, connector = 0) -> float:
        """ Connector Total imported active energy in running session in kWh """
        response = self.client.read_input_registers(address=ADDR_TOTAL_IMPORTED_ACTIVE_ENERGY_IN_RUNNING_SESSION_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readSessionDuration(self, connector = 0) -> datetime.timedelta:
        """ Connector Running session duration """
        response = self.client.read_input_registers(address=ADDR_RUNNING_SESSION_DURATION_BASE + connector * 100, count=4)
        return datetime.timedelta(seconds=response.registers[3])

    def readSessionDepartureTime(self, connector = 0) -> datetime.datetime:
        """ Connector Running session departure time """
        response = self.client.read_input_registers(address=ADDR_RUNNING_SESSION_DEPARTURE_TIME_BASE + connector * 100, count=4)
        unixTime = BinaryPayloadDecoder.fromRegisters(response.registers, Endian.Big).decode_64bit_int()
        return datetime.datetime.fromtimestamp(unixTime)

    def readSessionID(self, connector = 0) -> int:
        """ Connector Running session ID """
        response = self.client.read_input_registers(address=ADDR_RUNNING_SESSION_ID_BASE + connector * 100, count=4)
        return BinaryPayloadDecoder.fromRegisters(response.registers, Endian.Big).decode_64bit_int()

    def readEVMaxPower(self, connector = 0) -> float:
        """ Connector EV max power in kW """
        response = self.client.read_input_registers(address=ADDR_EV_MAX_POWER_BASE + connector * 100, count=2)
        return toFloat(response.registers)

    def readEVPlannedEnergy(self, connector = 0) -> float:
        """ Connector EV planned (required) energy in kWh """
        response = self.client.read_input_registers(address=ADDR_EV_PLANNED_ENERGY_BASE + connector * 100, count=2)
        return toFloat(response.registers)


    # Commands
    def stopCharging(self, connector = 0):
        """ Stop charging for connector """
        self.client.write_registers(ADDR_STOP_CHARGING_BASE + connector * 100, [1])

    def pauseCharging(self, connector = 0):
        """ Pause charging for connector """
        self.client.write_registers(ADDR_PAUSE_CHARGING_BASE + connector * 100, [1])

    def setDepartureTime(self, departure: datetime.datetime, connector = 0):
        """ Set departure time for connector """
        seconds_since_1970 = time.mktime(departure.timetuple())
        self.client.write_registers(ADDR_SET_DEPARTURE_TIME_BASE + connector * 100, wrapInt64(seconds_since_1970), skip_encode=True)

    def setCurrent(self, currentA, connector = 0):
        """ Set current setpoint in A for connector """
        self.client.write_registers(ADDR_SET_CURRENT_SETPOINT_BASE + connector * 100, wrapFloat(currentA), skip_encode=True)

    def cancelCurrentSetpoint(self, connector = 0):
        """ Cancel current setpoint for connector """
        self.client.write_registers(ADDR_CANCEL_CURRENT_SETPOINT_BASE + connector * 100, [1])

    def setPower(self, watt, connector = 0):
        """ Set power setpoint in W for connector """
        self.client.write_registers(ADDR_SET_POWER_SETPOINT_BASE + connector * 100, wrapFloat(watt / 1000), skip_encode=True)

    def cancelPowerSetpoint(self, connector = 0):
        """ Cancel power setpoint for connector """
        self.client.write_registers(ADDR_CANCEL_POWER_SETPOINT_BASE + connector * 100, [1])

    def setTime(self, now: datetime.datetime):
        """ Set current time """
        seconds_since_1970 = time.mktime(now.timetuple())
        self.client.write_registers(ADDR_SET_TIME, wrapInt64(seconds_since_1970), skip_encode=True)

    def restart(self):
        """ Trigger restart """
        self.client.write_registers(ADDR_RESTART, [1])

    def close(self):
        self.client.close()
