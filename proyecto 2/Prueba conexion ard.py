import serial
import json

direccion = serial.Serial('COM7',9600)
while True:
    info = direccion.readline()
    try: 
        jsoninfo = json.loads(info)

    except Exception:
        pass
