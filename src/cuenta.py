from datetime import datetime
from .cliente import Cliente
from .transaccion import Transaccion

class Cuenta:
    def __init__(self, numero_cuenta: str, cliente: Cliente, saldo: float = 0.0):
        self._numero_cuenta = numero_cuenta
        self._cliente = cliente
        self._saldo = saldo
        self._transacciones = []
    
    @property
    def numero_cuenta(self) -> str:
        return self._numero_cuenta
    
    @property
    def cliente(self) -> Cliente:
        return self._cliente
    
    @property
    def saldo(self) -> float:
        return self._saldo
    
    @property
    def transacciones(self) -> list[Transaccion]:
        return self._transacciones
    
    def ingresar_dinero(self, monto: float) -> bool:
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        
        self._saldo += monto
        transaccion = Transaccion("deposito", monto, datetime.now())
        self._transacciones.append(transaccion)
        return True
    
    def retirar_dinero(self, monto: float) -> bool:
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > self._saldo:
            raise ValueError("Saldo insuficiente")
        
        self._saldo -= monto
        transaccion = Transaccion("retiro", monto, datetime.now())
        self._transacciones.append(transaccion)
        return True
    
    def mostrar_datos(self) -> str:
        return f"Cuenta N° {self._numero_cuenta} - Saldo: ${self._saldo:.2f}"


class CuentaAhorro(Cuenta):
    def __init__(self, numero_cuenta: str, cliente: Cliente, saldo: float = 0.0, tasa_interes: float = 0.01):
        super().__init__(numero_cuenta, cliente, saldo)
        self._tasa_interes = tasa_interes
    
    def aplicar_interes(self):
        interes = self._saldo * self._tasa_interes
        self.ingresar_dinero(interes)
        return interes


class CuentaCorriente(Cuenta):
    def __init__(self, numero_cuenta: str, cliente: Cliente, saldo: float = 0.0, descubierto: float = 1000.0):
        super().__init__(numero_cuenta, cliente, saldo)
        self._descubierto = descubierto
    
    def retirar_dinero(self, monto: float) -> bool:
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > (self._saldo + self._descubierto):
            raise ValueError("Saldo insuficiente, incluso con descubierto")
        
        self._saldo -= monto
        transaccion = Transaccion("retiro", monto, datetime.now())
        self._transacciones.append(transaccion)
        return True
