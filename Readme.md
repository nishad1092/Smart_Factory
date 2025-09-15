# 🏭 Smart Factory IoT Pipeline (FastAPI + PyModbus + OpenPLC)

This project simulates a real-world **Smart Factory OT-layer pipeline** using open-source industrial components.

We integrate a **sensor simulator**, **Modbus TCP protocol**, and an **OpenPLC Ladder Logic controller** to model a temperature monitoring and threshold alert system in an industrial context.

---

## ✅ Features Implemented (Phase 1)

- Simulated temperature and humidity sensors using FastAPI  
- Modbus TCP-based data transmission using PyModbus  
- Real-time Ladder Logic decision making using OpenPLC Runtime  
- Accurate PLC memory addressing using Modbus mapping  

---

## 🛠️ Technologies Used

| Layer        | Tool/Library        | Purpose                                 |
|--------------|---------------------|-----------------------------------------|
| Sensor Sim   | `FastAPI`           | Simulate temperature + humidity sensor  |
| Protocol     | `pymodbus`          | Modbus TCP master/client in Python      |
| PLC Runtime  | `OpenPLC Runtime`   | Executes PLC program inside Debian VM   |
| PLC IDE      | `OpenPLC Editor`    | For writing and compiling Ladder Logic  |

---

## 🏗️ Architecture

```mermaid
flowchart LR
     [FastAPI Sensor Simulator] --> [PyModbus TCP Client]--> C(OpenPLC Runtime)