class Cliente:
    def __init__(self, nombre: str, apellido: str, dni: str):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni

    @property
    def nombre(self) -> str:
        return self.__nombre
    @nombre.setter
    def nombre(self, nombre: str):
        self.__nombre = nombre

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, apellido: str):
        self.__apellido = apellido

    @property
    def dni(self) -> str:
        return self.__dni

    @dni.setter
    def dni(self, dni: str):
        self.__dni = dni

    def mostrar_datos(self) -> str:
        return f"Nombre: {self.__nombre}, Apellido: {self.__apellido}, DNI: {self.__dni}"