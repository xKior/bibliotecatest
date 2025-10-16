import pytest
from src.usuario import Usuario

class TestUsuario:
    
    def test_crear_usuario_exitoso(self):
        usuario = Usuario("U001", "Juan Pérez")
        
        assert usuario.id == "U001"
        assert usuario.nombre == "Juan Pérez"
        assert usuario.libros_prestados == []
        assert usuario.cantidad_prestamos() == 0
    
    def test_crear_usuario_id_invalido(self):
        with pytest.raises(ValueError, match="ID debe ser una cadena no vacía"):
            Usuario("", "Juan Pérez")
        
        with pytest.raises(ValueError, match="ID debe ser una cadena no vacía"):
            Usuario(None, "Juan Pérez")
    
    def test_crear_usuario_nombre_invalido(self):
        with pytest.raises(ValueError, match="Nombre debe ser una cadena no vacía"):
            Usuario("U001", "")
    
    def test_agregar_prestamo_exitoso(self):
        usuario = Usuario("U001", "Juan Pérez")
        
        resultado = usuario.agregar_prestamo("978-0132350884")
        
        assert resultado == True
        assert "978-0132350884" in usuario.libros_prestados
        assert usuario.cantidad_prestamos() == 1
    
    def test_agregar_prestamo_duplicado(self):
        usuario = Usuario("U001", "Juan Pérez")
        usuario.agregar_prestamo("978-0132350884")
        
        resultado = usuario.agregar_prestamo("978-0132350884")
        
        assert resultado == False
        assert usuario.cantidad_prestamos() == 1
    
    def test_agregar_prestamo_limite_excedido(self):
        usuario = Usuario("U001", "Juan Pérez")
        
        for i in range(5):
            usuario.agregar_prestamo(f"ISBN-{i}")
        
        with pytest.raises(ValueError, match="ha alcanzado el límite de 5 libros"):
            usuario.agregar_prestamo("ISBN-6")
    
    def test_remover_prestamo_exitoso(self):
        usuario = Usuario("U001", "Juan Pérez")
        usuario.agregar_prestamo("978-0132350884")
        
        resultado = usuario.remover_prestamo("978-0132350884")
        
        assert resultado == True
        assert "978-0132350884" not in usuario.libros_prestados
        assert usuario.cantidad_prestamos() == 0
    
    def test_remover_prestamo_no_existente(self):
        usuario = Usuario("U001", "Juan Pérez")
        
        resultado = usuario.remover_prestamo("978-0132350884")
        
        assert resultado == False
    
    def test_tiene_libro_true(self):
        usuario = Usuario("U001", "Juan Pérez")
        usuario.agregar_prestamo("978-0132350884")
        
        assert usuario.tiene_libro("978-0132350884") == True
    
    def test_tiene_libro_false(self):
        usuario = Usuario("U001", "Juan Pérez")
        
        assert usuario.tiene_libro("978-0132350884") == False
    
    def test_puede_prestar_sin_libros(self):
        usuario = Usuario("U001", "Juan Pérez")
        
        assert usuario.puede_prestar() == True
    
    def test_puede_prestar_con_limite(self):
        usuario = Usuario("U001", "Juan Pérez")
        
        for i in range(5):
            usuario.agregar_prestamo(f"ISBN-{i}")
        
        assert usuario.puede_prestar() == False
    
    def test_libros_prestados_es_copia(self):
        usuario = Usuario("U001", "Juan Pérez")
        usuario.agregar_prestamo("978-0132350884")
        
        libros = usuario.libros_prestados
        libros.append("ISBN-FAKE")
        
        assert "ISBN-FAKE" not in usuario.libros_prestados
    
    def test_equality_mismo_id(self):
        usuario1 = Usuario("U001", "Juan Pérez")
        usuario2 = Usuario("U001", "María García")
        
        assert usuario1 == usuario2