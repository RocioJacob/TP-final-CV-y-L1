from __future__ import annotations
from typing import Optional
from datetime import datetime
import uuid

class Transaccion:
    def __init__(self, tipo: str, monto: float, fecha: Optional[datetime] = None):
        if tipo not in ("DEP", "RET"):
            raise ValueError("Tipo de transacción debe ser 'DEP' o 'RET'")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que 0")
        self.__tipo = tipo
        self.__monto = float(monto)
        self.__fecha = fecha or datetime.now()
        self.__id = str(uuid.uuid4())

    @property
    def tipo(self) -> str:
        return self.__tipo

    @property
    def monto(self) -> float:
        return self.__monto

    @property
    def fecha(self) -> datetime:
        return self.__fecha

    def to_dict(self) -> dict:
        return {"id": self.__id, "tipo": self.tipo, "monto": self.monto, "fecha": self.fecha.isoformat()}

    def __repr__(self):
        return f"Transaccion({self.tipo}, {self.monto}, {self.fecha.isoformat()})"