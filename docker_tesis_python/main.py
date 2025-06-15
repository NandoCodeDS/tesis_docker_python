from fastapi import FastAPI
from .modbus_reader import ConnectionModbusClient
from .usuarios import log

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API Modbus funcionando"}

@app.post("/capturar")
def capturar():
    client = ConnectionModbusClient("52.14.42.244", 8000)
    datos = client.take_data_device("nodo1")
    return {"status": "Datos capturados", "datos": datos}

@app.post("/login")  # <-- usa POST para enviar credenciales
def login_user(usuario: Usuario):
    return login(usuario)