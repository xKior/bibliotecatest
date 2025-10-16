import pytest
from src.libro import Libro

class TestLibro:
    
    def test_crear_libro_exitoso(self):
        libro = Libro("978-0132350884", "Clean Code", "Robert C. Martin")
        
        assert libro.isbn == "978-0132350884"
        assert libro.titulo == "Clean Code"
        assert libro.autor == "Robert C. Martin"
        assert libro.disponible == True
    
    def test_crear_libro_no_disponible(self):
        libro = Libro("978-0132350884", "Clean Code", "Robert C. Martin", disponible=False)
        
        assert libro.disponible == False
    
    def test_crear_libro_isbn_invalido(self):
        with pytest.raises(ValueError, match="ISBN debe ser una cadena no vacía"):
            Libro("", "Clean Code", "Robert C. Martin")
        
        with pytest.raises(ValueError, match="ISBN debe ser una cadena no vacía"):
            Libro(None, "Clean Code", "Robert C. Martin")
    
    def test_crear_libro_titulo_invalido(self):
        with pytest.raises(ValueError, match="Título debe ser una cadena no vacía"):
            Libro("978-0132350884", "", "Robert C. Martin")
    
    def test_crear_libro_autor_invalido(self):
        with pytest.raises(ValueError, match="Autor debe ser una cadena no vacía"):
            Libro("978-0132350884", "Clean Code", "")
    
    def test_prestar_libro_disponible(self):
        libro = Libro("978-0132350884", "Clean Code", "Robert C. Martin")
        
        resultado = libro.prestar()
        
        assert resultado == True
        assert libro.disponible == False
    
    def test_prestar_libro_no_disponible(self):
        libro = Libro("978-0132350884", "Clean Code", "Robert C. Martin")
        libro.prestar()
        
        resultado = libro.prestar()
        
        assert resultado == False
        assert libro.disponible == False
    
    def test_devolver_libro_prestado(self):
        libro = Libro("978-0132350884", "Clean Code", "Robert C. Martin")
        libro.prestar()
        
        resultado = libro.devolver()
        
        assert resultado == True
        assert libro.disponible == True
    
    def test_devolver_libro_disponible(self):
        libro = Libro("978-0132350884", "Clean Code", "Robert C. Martin")
        
        resultado = libro.devolver()
        
        assert resultado == False
        assert libro.disponible == True
    
    def test_str_representation(self):
        libro = Libro("978-0132350884", "Clean Code", "Robert C. Martin")
        
        str_libro = str(libro)
        
        assert "Clean Code" in str_libro
        assert "Robert C. Martin" in str_libro
        assert "978-0132350884" in str_libro
        assert "Disponible" in str_libro
    
    def test_equality_mismo_isbn(self):
        libro1 = Libro("978-0132350884", "Clean Code", "Robert C. Martin")
        libro2 = Libro("978-0132350884", "Otro Título", "Otro Autor")
        
        assert libro1 == libro2
    
    def test_equality_diferente_isbn(self):
        libro1 = Libro("978-0132350884", "Clean Code", "Robert C. Martin")
        libro2 = Libro("978-0201616224", "The Pragmatic Programmer", "Andrew Hunt")
        
        assert libro1 != libro2