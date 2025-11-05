import pytest
from src.cliente import Cliente
from src.cuenta import CuentaAhorro, CuentaCorriente
from src.almacenamiento import Banco

# Tests para Cliente
def test_crear_cliente_valido():
    cliente = Cliente('Juan', 'Perez', '12345678')
    assert cliente.nombre == 'Juan'
    assert cliente.apellido == 'Perez'
    assert cliente.dni == '12345678'

def test_cliente_datos_invalidos():
    # Test nombre inválido
    with pytest.raises(ValueError, match="Nombre inválido"):
        Cliente('', 'Perez', '12345678')
    
    # Test apellido inválido
    with pytest.raises(ValueError, match="Apellido inválido"):
        Cliente('Juan', '', '12345678')
    
    # Test DNI inválido
    with pytest.raises(ValueError, match="DNI debe ser numérico y no vacío"):
        Cliente('Juan', 'Perez', 'ABC')

def test_cliente_mostrar_datos():
    cliente = Cliente('Juan', 'Perez', '12345678')
    datos = cliente.mostrar_datos()
    assert datos == {"nombre": "Juan", "apellido": "Perez", "dni": "12345678"}

# Tests para CuentaAhorro
def test_crear_cuenta_ahorro_valida():
    cliente = Cliente('Juan', 'Perez', '12345678')
    cuenta = CuentaAhorro(cliente, 0.05)
    assert isinstance(cuenta.numero_cuenta, str)
    assert len(cuenta.numero_cuenta) == 8
    assert cuenta.saldo == 0
    assert cuenta.cliente == cliente

def test_cuenta_ahorro_operaciones():
    cliente = Cliente('Juan', 'Perez', '12345678')
    cuenta = CuentaAhorro(cliente, 0.05)
    
    # Test depósito
    tx = cuenta.ingresar(1000)
    assert cuenta.saldo == 1000
    assert tx.tipo == 'DEP'
    assert tx.monto == 1000
    
    # Test retiro
    tx = cuenta.retirar(500)
    assert cuenta.saldo == 500
    assert tx.tipo == 'RET'
    assert tx.monto == 500
    
    # Test retiro con saldo insuficiente
    with pytest.raises(ValueError, match="Saldo insuficiente"):
        cuenta.retirar(1000)

# Tests para CuentaCorriente
def test_crear_cuenta_corriente_valida():
    cliente = Cliente('Juan', 'Perez', '12345678')
    cuenta = CuentaCorriente(cliente, 1000)
    assert isinstance(cuenta.numero_cuenta, str)
    assert len(cuenta.numero_cuenta) == 8
    assert cuenta.saldo == 0
    assert cuenta.cliente == cliente

def test_cuenta_corriente_operaciones():
    cliente = Cliente('Juan', 'Perez', '12345678')
    cuenta = CuentaCorriente(cliente, 1000)  # límite de sobregiro
    
    # Test depósito
    tx = cuenta.ingresar(500)
    assert cuenta.saldo == 500
    
    # Test retiro dentro del límite de sobregiro
    tx = cuenta.retirar(1000)
    assert cuenta.saldo == -500
    
    # Test retiro excediendo límite de sobregiro
    with pytest.raises(ValueError):
        cuenta.retirar(600)

# Tests para Banco
def test_crear_banco_valido():
    banco = Banco('Mi Banco')
    assert banco.nombre == 'Mi Banco'
    assert banco.clientes == []
    assert banco.cuentas == []

def test_banco_operaciones():
    banco = Banco('Mi Banco')
    cliente = Cliente('Juan', 'Perez', '12345678')
    
    # Test agregar cliente
    banco.agregar_cliente(cliente)
    assert cliente in banco.clientes
    
    # Test agregar cuenta
    cuenta = CuentaAhorro(cliente, 0.05)
    banco.agregar_cuenta(cuenta)
    assert cuenta in banco.cuentas
