# ---------- app/modbus_reader.py ----------
from pymodbus.client.sync import ModbusTcpClient
from datetime import datetime
from .models import crear_registro
import math

class ConnectionModbusClient:
    def __init__(self, _host, _port, _timeout=3):
        self.client = ModbusTcpClient(host=_host, port=_port, timeout=_timeout)
        self.client.connect()

    def convertirAnguloPotencia(self, data):
        result = []
        for i in data:
            try:
                result.append(i * 57.2958)
            except:
                result.append(0)
        return result

    def take_data_device(self, address):
        read = lambda i: self.client.read_holding_registers(address=i, count=1, unit=1).registers[0]

        V = [read(i)/10 for i in [0x25, 0x26, 0x27]]
        F = [read(0x3E)/100]
        I = [read(i)/100 for i in [0x2B, 0x2C, 0x2D]]
        P = [read(i)/100 for i in [0x2E, 0x2F, 0x30]]
        Q = [read(i)/100 for i in [0x32, 0x33, 0x34]]
        S = [read(i)/100 for i in [0x3A, 0x3B, 0x3C]]
        PF = [read(i)/1000 for i in [0x36, 0x37, 0x38]]
        Ang = self.convertirAnguloPotencia(PF)

        voltaje = V[0]  # ejemplo simple, podrías hacer promedio
        frecuencia = F[0]

        datos = (
            voltaje, frecuencia, V[0], V[1], V[2],
            I[0], I[1], I[2], P[0], P[1], P[2],
            Q[0], Q[1], Q[2], S[0], S[1], S[2],
            PF[0], PF[1], PF[2], frecuencia,
            Ang[0], Ang[1], Ang[2]
        )
        crear_registro(datos)
        return datos
