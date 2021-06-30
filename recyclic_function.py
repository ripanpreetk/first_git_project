from pyModbusTCP.client import ModbusClient
import time
from time import sleep
from datetime import datetime
import struct

c = ModbusClient(host="localhost", port=502, auto_open=True)

class Modbus_TCP_Sentinel:

    def version(self):
        version = c.read_input_registers(0, 26)
        if version:
            print(f"Version:\n{version}")
        else:
            print("read error")

    def recyclic(self, period):
        t_end = time.time() + 60 * (int(period))
        while time.time() < t_end:
            running.version()
            sleep(5)

running=Modbus_TCP_Sentinel()
running.recyclic(1)


