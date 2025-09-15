from fastapi import FastAPI
from random import uniform
from pymodbus.client import ModbusTcpClient
import struct

from datetime import datetime

app = FastAPI()

sensor_generator = {
    "sensor_device": "DHT22",
    "temperature": "",
    "humidity": "",
    "timestamp": ""
}

# Route: Root
@app.get("/")
def root():
    return {"message": "Sensor Generator API is running 🚀"}

@app.get('/data')
def get_sensor_generator():
    print("Smart Factory")
    sensor_generator["temperature"] = round(uniform(20,30), 2)
    sensor_generator["humidity"] =  round(uniform(40,50) , 2)
    sensor_generator["timestamp"] = datetime.now()
    return sensor_generator
    
PLC_IP = "192.168.64.5"   # IP of your Debian 13 VM
PLC_PORT = 1502           # Modbus port you configured

def write_real_to_register(client, address, value):
    # Convert float to two 16-bit Modbus words (big-endian)
    payload = struct.unpack('>HH', struct.pack('>f', value))
    print(payload)
    client.write_registers(address, payload)

@app.post("/push_to_openplc/")
def push_sensor_to_openplc(threshold: float = 30.0):
    temp = round(uniform(20, 40), 2)

    client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
    if not client.connect():
        return {"status": "error", "message": "Could not connect to OpenPLC"}

    try:
        # Write temperature to HR[0,1] and uses MD0, each MD uses 2 byte or 2 16 bit registers so it skips twice from 2048
        # MD is Double Word, i.e 32 bits = 4 bytes, so every 4 bytes REAL type chooses.
        write_real_to_register(client, 2048, temp)

        # Write threshold to HR[2,3] and uses MD4
        write_real_to_register(client, 2056, threshold)

        client.close()
        return {
            "status": "success",
            "temperature": temp,
            "threshold": threshold
        }

    except Exception as e:
        client.close()
        return {"status": "error", "message": str(e)}