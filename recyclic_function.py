from pyModbusTCP.client import ModbusClient
import time
from time import sleep
from datetime import datetime
import struct

c = ModbusClient(host="192.168.1.15", port=502, auto_open=True)

# if c.open():
#     print(f"connected!, value of c: {c}")
# else:
#     print(f"Not connected!, value of c: {c}")

class Modbus_TCP_Sentinel:

    # def version(self):
    #     version = c.read_input_registers(0, 26)
    #     if version:
    #         print(f"Version:\n{version}")
    #     else:
    #         print("read error")

    def reject_count(self):
        reject_count = c.read_input_registers(306, 2)
        if reject_count:
            print(f"reject count: {reject_count[1]}")
        else:
            print("read error")

    def recyclic(self, period): # period is the time in minutes, i.e user will enter how many minutes one wants to run this function
        t_end = time.time() + 60 * (int(period)) #here I'm multiplying periods/minutes with 60. by doing so we're converting it into seconds
        cycle_ran=0
        while time.time() < t_end:
            running.reject_count()
            cycle_ran=cycle_ran+1
            # print(f"cycle ran for {cycle_ran}th time")
            sleep_time=0.01
            sleep(sleep_time)
        print(f"--------------------------------------------"
              f"\nProgram fetched data for : {period} minutes "
              f"\nwith delay of : {sleep_time} seconds"
              f"\ntotal cycle ran : {cycle_ran}"
              f"\n--------------------------------------------")

running=Modbus_TCP_Sentinel()
# running.version()
# running.reject_count()
running.recyclic(1)




