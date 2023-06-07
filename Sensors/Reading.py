from serial import Serial
import time
import serial.tools.list_ports
import pandas as pd


# List available ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)



port = 'COM5'  # Update with the correct port for your Arduino
baud_rate = 9600  # Update with the correct baud rate for your Arduino
ser = Serial(port, baud_rate)

#ser.open()


val = {
    "time": [],
    "number_of_sensor":[],
    "pressure":[]
}

start=time.time()

while (time.time()-start)<10:
    response = ser.readline().decode().strip()
    values = response.split(',')
    if values[2]!=1:
        val["time"].append(values[0])
        val["number_of_sensor"].append(values[1])
        val["pressure"].append(values[2])


df = pd.DataFrame(val)
df.to_csv('output.csv',index=False)

print(df)

ser.close()



