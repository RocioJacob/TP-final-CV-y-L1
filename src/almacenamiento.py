from typing import List, Optional
# Importación de modelos desde los nuevos archivos
from cliente import Cliente
from cuenta import Cuenta, CuentaAhorro, CuentaCorriente 

# -------------------- ALMACENAMIENTO EN MEMORIA --------------------

class Banco:
    # ... (el resto de la implementación de la clase Banco es el mismo) ...
    def __init__(self):
        self._clientes: List[Cliente] = []
        self._cuentas: List[Cuenta] = []

    # Cliente CRUD
    def crear_cliente(self, nombre: str, apellido: str, dni: str) -> Cliente:
        if self.buscar_cliente_por_dni(dni) is not None:
            raise ValueError("Ya existe un cliente con ese DNI")
        cliente = Cliente(nombre, apellido, dni)
        self._clientes.append(cliente)
        return cliente

    def buscar_cliente_por_dni(self, dni: str) -> Optional[Cliente]:
        for c in self._clientes:
            if c.dni == dni:
                return c
        return None

    def listar_clientes(self) -> List[Cliente]:
        return list(self._clientes)

    # Cuentas
    def crear_cuenta_ahorro(self, dni_cliente: str, tasa_interes: float = 0.01) -> CuentaAhorro:
        cliente = self.buscar_cliente_por_dni(dni_cliente)
        if cliente is None:
            raise ValueError("Cliente no encontrado")
        cuenta = CuentaAhorro(cliente, tasa_interes)
        self._cuentas.append(cuenta)
        return cuenta

    def crear_cuenta_corriente(self, dni_cliente: str, limite_descubierto: float = 0.0) -> CuentaCorriente:
        cliente = self.buscar_cliente_por_dni(dni_cliente)
        if cliente is None:
            raise ValueError("Cliente no encontrado")
        cuenta = CuentaCorriente(cliente, limite_descubierto)
        self._cuentas.append(cuenta)
        return cuenta

    def buscar_cuenta_por_num(self, numero: str) -> Optional[Cuenta]:
        for c in self._cuentas:
            if c.numero_cuenta == numero:
                return c
        return None

    def listar_cuentas(self) -> List[Cuenta]:
        return list(self._cuentas)

    def listar_cuentas_por_cliente(self, dni_cliente: str) -> List[Cuenta]:
        return [c for c in self._cuentas if c.cliente.dni == dni_cliente]