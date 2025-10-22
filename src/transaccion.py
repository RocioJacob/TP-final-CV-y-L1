from datetime import datetime

class Transaccion:
    def __init__(self, monto: float, tipo: str, fecha: datetime = None,):
        self.__monto = monto
        self.__tipo = tipo  # 'ingreso' o 'egreso'
        self.__fecha = fecha 

    @property
    def monto(self) -> float:
        return self.__monto

    @property
    def tipo(self) -> str:
        return self.__tipo

    @property
    def fecha(self) -> datetime:
        return self.__fecha
    
    def __str__(self)
        return f"{self.__fecha.strftime('%Y-%m-%d %H:%M:%S')} - {self.__tipo.upper()}: ${self.__monto:.2f}"
    
    class Transferencia(Transaccion):
        def __init__(self, monto: float, fecha: datetime, origen: str, destino: str):
            super().__init__("transferencia", monto, fecha)
            self._origen = origen
            self._destino = destino
        def __str__(self):
            return (f"{self.fecha.strftime('%Y-%m-%d %H:%M:%S')} - TRANSFERENCIA: ${self.monto:.2f} "
                    f"de {self._origen} a {self._destino}")