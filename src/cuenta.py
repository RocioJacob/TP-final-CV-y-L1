from __future__ import annotations
from typing import List
import uuid
# Importamos los modelos necesarios
from cliente import Cliente
from transaccion import Transaccion

class Cuenta:
    def __init__(self, cliente: Cliente):
        # atributos privados
        self.__numero_cuenta = self._generar_numero()
        self.__saldo = 0.0
        self.__cliente = cliente
        self.__transacciones: List[Transaccion] = []

    # Encapsulamiento
    @property
    def numero_cuenta(self) -> str:
        return self.__numero_cuenta

    @property
    def saldo(self) -> float:
        return self.__saldo

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    def _generar_numero(self) -> str:
        return str(uuid.uuid4())[:8]

    # Métodos - polimorfismo posible reimplementando en subclases
    def ingresar(self, monto: float) -> Transaccion:
        if monto <= 0:
            raise ValueError("El monto a ingresar debe ser mayor que cero")
        # Acceder al atributo privado mediante name mangling para modificarlo
        self._Cuenta__saldo += monto
        tx = Transaccion("DEP", monto)
        self._Cuenta__transacciones.append(tx)
        return tx

    def retirar(self, monto: float) -> Transaccion:
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser mayor que cero")
        if monto > self.__saldo:
            raise ValueError("Saldo insuficiente")
        # Acceder al atributo privado mediante name mangling para modificarlo
        self._Cuenta__saldo -= monto
        tx = Transaccion("RET", monto)
        self._Cuenta__transacciones.append(tx)
        return tx

    def registrar_transaccion(self, tx: Transaccion):
        # permite registrar transacciones externas (p.ej. transferencia interna)
        self._Cuenta__transacciones.append(tx)

    def obtener_transacciones(self) -> List[Transaccion]:
        return list(self._Cuenta__transacciones)

    def mostrar_datos(self) -> dict:
        return {"numero_cuenta": self.numero_cuenta, "saldo": self.saldo, "cliente": self.cliente.mostrar_datos()}

    def __repr__(self):
        return f"Cuenta({self.numero_cuenta}, Saldo={self.saldo})"


# Subclases para herencia y polimorfismo
class CuentaAhorro(Cuenta):
    def __init__(self, cliente: Cliente, tasa_interes: float = 0.01):
        super().__init__(cliente)
        self.__tasa_interes = tasa_interes

    def aplicar_interes(self):
        # ejemplo simple: aplicar interes sobre saldo
        interes = self.saldo * self.__tasa_interes
        if interes > 0:
            self.ingresar(interes)

    def __repr__(self):
        return f"CuentaAhorro({self.numero_cuenta}, Saldo={self.saldo}, Tasa={self.__tasa_interes})"


class CuentaCorriente(Cuenta):
    def __init__(self, cliente: Cliente, limite_descubierto: float = 0.0):
        super().__init__(cliente)
        self.__limite_descubierto = float(limite_descubierto)

    def retirar(self, monto: float) -> Transaccion:
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser mayor que cero")
        disponible = self.saldo + self.__limite_descubierto
        if monto > disponible:
            raise ValueError("Saldo + límite insuficiente")
        
        # Uso del name mangling para acceder y modificar el saldo y transacciones
        try:
            self._Cuenta__saldo -= monto
            
            # Creamos y registramos la transacción
            tx = Transaccion("RET", monto)
            self._Cuenta__transacciones.append(tx)
            return tx
            
        except Exception as e:
            # En un sistema real, el name mangling podría ser más robusto, 
            # pero aquí manejamos el error en caso de fallo interno.
            raise RuntimeError("Error interno al procesar retiro con descubierto") from e

    def __repr__(self):
        return f"CuentaCorriente({self.numero_cuenta}, Saldo={self.saldo}, Descubierto={self.__limite_descubierto})"