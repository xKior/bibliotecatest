import pytest
from datetime import datetime, timedelta
from src.prestamo import Prestamo

class TestPrestamo:
    
    def test_crear_prestamo_exitoso(self):
        prestamo = Prestamo("P001", "978-0132350884", "U001")
        
        assert prestamo.id == "P001"
        assert prestamo.libro_isbn == "978-0132350884"
        assert prestamo.usuario_id == "U001"
        assert prestamo.fecha_prestamo is not None
        assert prestamo.fecha_devolucion is None
        assert prestamo.esta_activo() == True
    
    def test_crear_prestamo_id_invalido(self):
        with pytest.raises(ValueError, match="ID debe ser una cadena no vacía"):
            Prestamo("", "978-0132350884", "U001")
    
    def test_crear_prestamo_isbn_invalido(self):
        with pytest.raises(ValueError, match="ISBN del libro debe ser una cadena no vacía"):
            Prestamo("P001", "", "U001")
    
    def test_crear_prestamo_usuario_invalido(self):
        with pytest.raises(ValueError, match="ID del usuario debe ser una cadena no vacía"):
            Prestamo("P001", "978-0132350884", "")
    
    def test_devolver_prestamo_activo(self):
        prestamo = Prestamo("P001", "978-0132350884", "U001")
        
        resultado = prestamo.devolver()
        
        assert resultado == True
        assert prestamo.fecha_devolucion is not None
        assert prestamo.esta_activo() == False
    
    def test_devolver_prestamo_ya_devuelto(self):
        prestamo = Prestamo("P001", "978-0132350884", "U001")
        prestamo.devolver()
        
        resultado = prestamo.devolver()
        
        assert resultado == False
    
    def test_esta_vencido_no_vencido(self):
        prestamo = Prestamo("P001", "978-0132350884", "U001")
        
        assert prestamo.esta_vencido() == False
    
    def test_esta_vencido_vencido(self):
        fecha_pasada = datetime.now() - timedelta(days=20)
        prestamo = Prestamo("P001", "978-0132350884", "U001", fecha_prestamo=fecha_pasada)
        
        assert prestamo.esta_vencido() == True
    
    def test_esta_vencido_devuelto(self):
        fecha_pasada = datetime.now() - timedelta(days=20)
        prestamo = Prestamo("P001", "978-0132350884", "U001", fecha_prestamo=fecha_pasada)
        prestamo.devolver()
        
        assert prestamo.esta_vencido() == False
    
    def test_dias_restantes_nuevo(self):
        prestamo = Prestamo("P001", "978-0132350884", "U001")
        
        dias = prestamo.dias_restantes()
        
        assert dias >= 13 and dias <= 14
    
    def test_dias_restantes_vencido(self):
        fecha_pasada = datetime.now() - timedelta(days=20)
        prestamo = Prestamo("P001", "978-0132350884", "U001", fecha_prestamo=fecha_pasada)
        
        dias = prestamo.dias_restantes()
        
        assert dias == 0
    
    def test_dias_restantes_devuelto(self):
        prestamo = Prestamo("P001", "978-0132350884", "U001")
        prestamo.devolver()
        
        dias = prestamo.dias_restantes()
        
        assert dias == 0
    
    def test_fecha_limite_correcta(self):
        fecha_prestamo = datetime(2025, 10, 1, 10, 0, 0)
        prestamo = Prestamo("P001", "978-0132350884", "U001", fecha_prestamo=fecha_prestamo)
        
        fecha_esperada = fecha_prestamo + timedelta(days=14)
        
        assert prestamo.fecha_limite == fecha_esperada
    
    def test_equality_mismo_id(self):
        prestamo1 = Prestamo("P001", "978-0132350884", "U001")
        prestamo2 = Prestamo("P001", "978-0201616224", "U002")
        
        assert prestamo1 == prestamo2