# Sonnen Charger Modbus API
Allows to access Sonnen Charger (or any other ETREL INCH) using TCP Modbus

## Usage
```Python
from sonnen_charger_modbus import Charger, ChargerConnectorStatus
import traceback

charger = Charger('192.168.0.1', 502)

try:
    if charger.readConStatus(0).value >= ChargerConnectorStatus.WaitingForVehicleToRespond.value:
        carConnected = True
        chargingPower = charger.readActivePowerTotal(0) * 1000
        print('chargingPower', chargingPower)
except Exception as e:
    print('Error in Modbus communication:')
    traceback.print_exc()
    print(e)

charger.close()
```
