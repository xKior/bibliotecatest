import pytest
from src.biblioteca import Biblioteca, LibroNoDisponibleError, UsuarioNoExisteError, LibroNoExisteError
from src.libro import Libro
from src.usuario import Usuario

class TestBiblioteca:
    
    @pytest.fixture
    def biblioteca(self):
        return Biblioteca()
    
    @pytest.fixture
    def libro_ejemplo(self):
        return Libro("978-0132350884", "Clean Code", "Robert C. Martin")
    
    @pytest.fixture
    def usuario_ejemplo(self):
        return Usuario("U001", "Juan Pérez")
    
    def test_agregar_libro_exitoso(self, biblioteca, libro_ejemplo):
        resultado = biblioteca.agregar_libro(libro_ejemplo)
        
        assert resultado == True
        assert biblioteca.obtener_libro("978-0132350884") == libro_ejemplo
        assert biblioteca.total_libros() == 1
    
    def test_agregar_libro_duplicado(self, biblioteca, libro_ejemplo):
        biblioteca.agregar_libro(libro_ejemplo)
        
        libro_duplicado = Libro("978-0132350884", "Otro Título", "Otro Autor")
        resultado = biblioteca.agregar_libro(libro_duplicado)
        
        assert resultado == False
        assert biblioteca.total_libros() == 1
    
    def test_obtener_libro_existente(self, biblioteca, libro_ejemplo):
        biblioteca.agregar_libro(libro_ejemplo)
        
        libro = biblioteca.obtener_libro("978-0132350884")
        
        assert libro is not None
        assert libro.titulo == "Clean Code"
    
    def test_obtener_libro_no_existente(self, biblioteca):
        libro = biblioteca.obtener_libro("ISBN-INEXISTENTE")
        
        assert libro is None
    
    def test_eliminar_libro_disponible(self, biblioteca, libro_ejemplo):
        biblioteca.agregar_libro(libro_ejemplo)
        
        resultado = biblioteca.eliminar_libro("978-0132350884")
        
        assert resultado == True
        assert biblioteca.obtener_libro("978-0132350884") is None
        assert biblioteca.total_libros() == 0
    
    def test_eliminar_libro_prestado(self, biblioteca, libro_ejemplo, usuario_ejemplo):
        biblioteca.agregar_libro(libro_ejemplo)
        biblioteca.registrar_usuario(usuario_ejemplo)
        biblioteca.crear_prestamo("978-0132350884", "U001")
        
        resultado = biblioteca.eliminar_libro("978-0132350884")
        
        assert resultado == False
        assert biblioteca.obtener_libro("978-0132350884") is not None
    
    def test_registrar_usuario_exitoso(self, biblioteca, usuario_ejemplo):
        resultado = biblioteca.registrar_usuario(usuario_ejemplo)
        
        assert resultado == True
        assert biblioteca.obtener_usuario("U001") == usuario_ejemplo
        assert biblioteca.total_usuarios() == 1
    
    def test_registrar_usuario_duplicado(self, biblioteca, usuario_ejemplo):
        biblioteca.registrar_usuario(usuario_ejemplo)
        
        usuario_duplicado = Usuario("U001", "María García")
        resultado = biblioteca.registrar_usuario(usuario_duplicado)
        
        assert resultado == False
        assert biblioteca.total_usuarios() == 1
    
    def test_eliminar_usuario_sin_prestamos(self, biblioteca, usuario_ejemplo):
        biblioteca.registrar_usuario(usuario_ejemplo)
        
        resultado = biblioteca.eliminar_usuario("U001")
        
        assert resultado == True
        assert biblioteca.obtener_usuario("U001") is None
    
    def test_eliminar_usuario_con_prestamos(self, biblioteca, libro_ejemplo, usuario_ejemplo):
        biblioteca.agregar_libro(libro_ejemplo)
        biblioteca.registrar_usuario(usuario_ejemplo)
        biblioteca.crear_prestamo("978-0132350884", "U001")
        
        resultado = biblioteca.eliminar_usuario("U001")
        
        assert resultado == False
        assert biblioteca.obtener_usuario("U001") is not None
    
    @pytest.mark.parametrize("titulo_busqueda,esperados", [
        ("Clean", 1),
        ("Code", 1),
        ("Python", 0),
        ("", 3),  
    ])
    def test_buscar_libros_por_titulo(self, biblioteca, titulo_busqueda, esperados):
        biblioteca.agregar_libro(Libro("ISBN1", "Clean Code", "Robert Martin"))
        biblioteca.agregar_libro(Libro("ISBN2", "Design Patterns", "Gang of Four"))
        biblioteca.agregar_libro(Libro("ISBN3", "Refactoring", "Martin Fowler"))
        
        resultados = biblioteca.buscar_libros(titulo=titulo_busqueda)
        
        assert len(resultados) == esperados
    
    @pytest.mark.parametrize("autor_busqueda,esperados", [
        ("Martin", 2),
        ("Fowler", 1),
        ("Unknown", 0),
    ])
    def test_buscar_libros_por_autor(self, biblioteca, autor_busqueda, esperados):
        biblioteca.agregar_libro(Libro("ISBN1", "Clean Code", "Robert Martin"))
        biblioteca.agregar_libro(Libro("ISBN2", "Design Patterns", "Gang of Four"))
        biblioteca.agregar_libro(Libro("ISBN3", "Refactoring", "Martin Fowler"))
        
        resultados = biblioteca.buscar_libros(autor=autor_busqueda)
        
        assert len(resultados) == esperados
    
    def test_buscar_libros_disponibles(self, biblioteca, usuario_ejemplo):
        biblioteca.agregar_libro(Libro("ISBN1", "Libro 1", "Autor 1"))
        biblioteca.agregar_libro(Libro("ISBN2", "Libro 2", "Autor 2"))
        biblioteca.registrar_usuario(usuario_ejemplo)
        biblioteca.crear_prestamo("ISBN1", "U001")
        
        resultados = biblioteca.buscar_libros(disponible=True)
        
        assert len(resultados) == 1
        assert resultados[0].isbn == "ISBN2"