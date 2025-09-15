## OpenPLC Memory Mapping for REAL (Float) Variables

This section explains how sensor data is written from a Python `pymodbus` client to OpenPLC using Modbus **Holding Registers** mapped to `%MD` variables.

---

###  What is `%MD` in OpenPLC?

In OpenPLC, `%MDx` refers to:

- `%M`   → Internal Memory (bit-level)
- `%MD`  → **Memory Double-word (32-bit)** — used for `REAL` (float) values

Each `%MD` variable occupies:

- **4 bytes** = **32 bits**
- Which equals **two consecutive 16-bit Modbus Holding Registers**

---

### 🛠️ Memory Layout

| Variable     | OpenPLC Type | Modbus Register Address | Size (Registers) | Notes              |
|--------------|--------------|--------------------------|------------------|--------------------|
| `tempsensor` | `%MD0`       | HR[2048], HR[2049]       | 2                | Temperature value  |
| `threshold`  | `%MD4`       | HR[2056], HR[2057]       | 2                | Threshold value    |

**Why skip between `%MD0` and `%MD4`?**  
Each `%MDx` represents a **32-bit** (`REAL`) value, which is **4 bytes** or **2 consecutive 16-bit Modbus Holding Registers**.

- `%MD0` occupies **HR[2048, 2049]**
- The next available **non-overlapping** 32-bit (4-byte) block is **HR[2050, 2051]** → this would be `%MD2`
- We **skip `%MD2` and `%MD3`** to ensure clean 4-byte boundaries
- `%MD4` then uses **HR[2056, 2057]**

This spacing ensures **data alignment and no memory overlap**, which is especially important for Modbus integrations and debugging with external tools like Node-RED or SCADA systems.

---

###  Python Code (Using PyModbus)

```python
from pymodbus.client import ModbusTcpClient
import struct

PLC_IP = "192.168.64.5"
PLC_PORT = 1502

def write_real_to_register(client, address, value):
    # Convert float to 2x 16-bit registers (big-endian)
    payload = struct.unpack('>HH', struct.pack('>f', value))
    client.write_registers(address, payload)

client = ModbusTcpClient(PLC_IP, port=PLC_PORT)
client.connect()

# Write to %MD0 → HR[2048, 2049]
write_real_to_register(client, 2048, 26.82)

# Write to %MD4 → HR[2056, 2057]
write_real_to_register(client, 2056, 30.00)

client.close()