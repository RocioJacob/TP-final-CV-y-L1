import pytest
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from transaccion import Transaccion


class TestTransaccion:
    """Tests para la clase Transacción"""
    
    def test_crear_transaccion(self):
        """Prueba crear una transacción"""
        trans = Transaccion(tipo="ingreso", monto=500, cuenta_numero="001")
        assert trans.tipo == "ingreso"
        assert trans.monto == 500
        assert trans.cuenta_numero == "001"
    
    def test_transaccion_tiene_fecha(self):
        """Prueba que la transacción tiene fecha"""
        trans = Transaccion(tipo="retiro", monto=200, cuenta_numero="002")
        assert isinstance(trans.fecha, datetime)
    
    def test_monto_negativo(self):
        """Prueba transacción con monto negativo"""
        with pytest.raises(ValueError):
            Transaccion(tipo="ingreso", monto=-100, cuenta_numero="003")