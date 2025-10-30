from __future__ import annotations

class Cliente:
    def __init__(self, nombre: str, apellido: str, dni: str):
        self.__nombre = None
        self.__apellido = None
        self.__dni = None
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni

    # Getters / setters con validación mínima
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, val: str):
        if not isinstance(val, str) or not val.strip():
            raise ValueError("Nombre inválido")
        self.__nombre = val.strip()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, val: str):
        if not isinstance(val, str) or not val.strip():
            raise ValueError("Apellido inválido")
        self.__apellido = val.strip()

    @property
    def dni(self) -> str:
        return self.__dni

    @dni.setter
    def dni(self, val: str):
        if not isinstance(val, str) or not val.strip() or not val.strip().isdigit():
            raise ValueError("DNI debe ser numérico y no vacío")
        self.__dni = val.strip()

    def mostrar_datos(self) -> dict:
        return {"nombre": self.nombre, "apellido": self.apellido, "dni": self.dni}

    def __repr__(self):
        return f"Cliente({self.nombre} {self.apellido}, DNI={self.dni})"