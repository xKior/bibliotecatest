import pytest
from src.biblioteca import Biblioteca
from src.libro import Libro
from src.usuario import Usuario

class TestIntegracionBiblioteca:
    
    def test_flujo_completo_prestamo_devolucion(self):
        biblioteca = Biblioteca()
        
        libro1 = Libro("978-0132350884", "Clean Code", "Robert C. Martin")
        libro2 = Libro("978-0201616224", "The Pragmatic Programmer", "Andrew Hunt")
        
        assert biblioteca.agregar_libro(libro1) == True
        assert biblioteca.agregar_libro(libro2) == True
        assert biblioteca.total_libros() == 2
        
        usuario1 = Usuario("U001", "Juan Pérez")
        usuario2 = Usuario("U002", "María García")
        
        assert biblioteca.registrar_usuario(usuario1) == True
        assert biblioteca.registrar_usuario(usuario2) == True
        assert biblioteca.total_usuarios() == 2
        
        prestamo1 = biblioteca.crear_prestamo("978-0132350884", "U001")
        prestamo2 = biblioteca.crear_prestamo("978-0201616224", "U002")
        
        assert prestamo1.esta_activo() == True
        assert prestamo2.esta_activo() == True
        assert biblioteca.total_prestamos_activos() == 2
        
        assert libro1.disponible == False
        assert libro2.disponible == False
        assert usuario1.cantidad_prestamos() == 1
        assert usuario2.cantidad_prestamos() == 1
        
        assert biblioteca.devolver_prestamo(prestamo1.id) == True
        assert prestamo1.esta_activo() == False
        assert libro1.disponible == True
        assert usuario1.cantidad_prestamos() == 0
        assert biblioteca.total_prestamos_activos() == 1
        
        disponibles = biblioteca.buscar_libros(disponible=True)
        assert len(disponibles) == 1
        assert disponibles[0].isbn == "978-0132350884"
        
        prestamo3 = biblioteca.crear_prestamo("978-0132350884", "U002")
        assert prestamo3.esta_activo() == True
        assert usuario2.cantidad_prestamos() == 2
    
    def test_flujo_multiples_prestamos_usuario(self):
        biblioteca = Biblioteca()
        
        for i in range(1, 6):
            libro = Libro(f"ISBN-{i}", f"Libro {i}", f"Autor {i}")
            biblioteca.agregar_libro(libro)
        
        usuario = Usuario("U001", "Juan Pérez")
        biblioteca.registrar_usuario(usuario)
        
        prestamo1 = biblioteca.crear_prestamo("ISBN-1", "U001")
        prestamo2 = biblioteca.crear_prestamo("ISBN-2", "U001")
        prestamo3 = biblioteca.crear_prestamo("ISBN-3", "U001")
        
        assert usuario.cantidad_prestamos() == 3
        assert biblioteca.total_prestamos_activos() == 3
        
        biblioteca.devolver_prestamo(prestamo2.id)
        assert usuario.cantidad_prestamos() == 2
        
        prestamo4 = biblioteca.crear_prestamo("ISBN-2", "U001")
        prestamo5 = biblioteca.crear_prestamo("ISBN-4", "U001")
        
        assert usuario.cantidad_prestamos() == 4
        
        prestamos_usuario = biblioteca.listar_prestamos_usuario("U001")
        assert len(prestamos_usuario) == 4
    
    def test_flujo_busqueda_avanzada(self):
        """Test: Búsquedas complejas en el catálogo"""
        biblioteca = Biblioteca()
        
        libros = [
            Libro("ISBN-1", "Clean Code", "Robert Martin"),
            Libro("ISBN-2", "Clean Architecture", "Robert Martin"),
            Libro("ISBN-3", "Design Patterns", "Gang of Four"),
            Libro("ISBN-4", "Refactoring", "Martin Fowler"),
            Libro("ISBN-5", "Domain Driven Design", "Eric Evans"),
        ]
        
        for libro in libros:
            biblioteca.agregar_libro(libro)
        
        resultados_martin = biblioteca.buscar_libros(autor="Martin")
        assert len(resultados_martin) == 3
        
        resultados_design = biblioteca.buscar_libros(titulo="Design")
        assert len(resultados_design) == 2
        
        usuario = Usuario("U001", "Juan Pérez")
        biblioteca.registrar_usuario(usuario)
        
        biblioteca.crear_prestamo("ISBN-1", "U001")
        biblioteca.crear_prestamo("ISBN-3", "U001")
        
        disponibles = biblioteca.buscar_libros(disponible=True)
        assert len(disponibles) == 3
        
        disponibles_martin = biblioteca.buscar_libros(autor="Martin", disponible=True)
        assert len(disponibles_martin) == 2
    
    def test_flujo_restricciones_y_excepciones(self):
        biblioteca = Biblioteca()
        
        libro = Libro("ISBN-1", "Test Book", "Test Author")
        biblioteca.agregar_libro(libro)
        
        usuario = Usuario("U001", "Juan Pérez")
        biblioteca.registrar_usuario(usuario)
        
        prestamo = biblioteca.crear_prestamo("ISBN-1", "U001")
        assert prestamo is not None
        
        usuario2 = Usuario("U002", "María García")
        biblioteca.registrar_usuario(usuario2)
        
        with pytest.raises(Exception):  
            biblioteca.crear_prestamo("ISBN-1", "U002")
        
        with pytest.raises(Exception):  
            biblioteca.crear_prestamo("ISBN-FALSO", "U001")
        
        with pytest.raises(Exception):  
            biblioteca.crear_prestamo("ISBN-1", "U999")
        
        assert biblioteca.eliminar_libro("ISBN-1") == False
        
        assert biblioteca.eliminar_usuario("U001") == False
        
        biblioteca.devolver_prestamo(prestamo.id)
        
        assert biblioteca.eliminar_libro("ISBN-1") == True
        assert biblioteca.eliminar_usuario("U001") == True
    
    def test_flujo_estadisticas_sistema(self):
        biblioteca = Biblioteca()
        
        for i in range(1, 11):
            biblioteca.agregar_libro(Libro(f"ISBN-{i}", f"Libro {i}", f"Autor {i}"))
        
        for i in range(1, 6):
            biblioteca.registrar_usuario(Usuario(f"U00{i}", f"Usuario {i}"))
        
        assert biblioteca.total_libros() == 10
        assert biblioteca.total_usuarios() == 5
        assert biblioteca.total_prestamos_activos() == 0
        
        biblioteca.crear_prestamo("ISBN-1", "U001")
        biblioteca.crear_prestamo("ISBN-2", "U001")
        biblioteca.crear_prestamo("ISBN-3", "U002")
        biblioteca.crear_prestamo("ISBN-4", "U003")
        
        assert biblioteca.total_prestamos_activos() == 4
        
        disponibles = biblioteca.buscar_libros(disponible=True)
        assert len(disponibles) == 6
        
        prestamos = biblioteca.listar_prestamos_activos()
        biblioteca.devolver_prestamo(prestamos[0].id)
        biblioteca.devolver_prestamo(prestamos[1].id)
        
        assert biblioteca.total_prestamos_activos() == 2
        
        disponibles = biblioteca.buscar_libros(disponible=True)
        assert len(disponibles) == 8