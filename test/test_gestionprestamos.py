import pytest
from src.biblioteca import Biblioteca, LibroNoDisponibleError, UsuarioNoExisteError, LibroNoExisteError
from src.libro import Libro
from src.usuario import Usuario

class TestGestionPrestamos:
    
    @pytest.fixture
    def biblioteca_configurada(self):
        biblioteca = Biblioteca()
        
        biblioteca.agregar_libro(Libro("ISBN1", "Clean Code", "Robert Martin"))
        biblioteca.agregar_libro(Libro("ISBN2", "Design Patterns", "Gang of Four"))
        
        biblioteca.registrar_usuario(Usuario("U001", "Juan Pérez"))
        biblioteca.registrar_usuario(Usuario("U002", "María García"))
        
        return biblioteca
    
    def test_crear_prestamo_exitoso(self, biblioteca_configurada):
        prestamo = biblioteca_configurada.crear_prestamo("ISBN1", "U001")
        
        assert prestamo is not None
        assert prestamo.libro_isbn == "ISBN1"
        assert prestamo.usuario_id == "U001"
        assert prestamo.esta_activo() == True
        
        libro = biblioteca_configurada.obtener_libro("ISBN1")
        assert libro.disponible == False
        
        usuario = biblioteca_configurada.obtener_usuario("U001")
        assert usuario.tiene_libro("ISBN1") == True
    
    def test_crear_prestamo_libro_no_existe(self, biblioteca_configurada):
        with pytest.raises(LibroNoExisteError, match="no existe"):
            biblioteca_configurada.crear_prestamo("ISBN-FALSO", "U001")
    
    def test_crear_prestamo_libro_no_disponible(self, biblioteca_configurada):
        biblioteca_configurada.crear_prestamo("ISBN1", "U001")
        
        with pytest.raises(LibroNoDisponibleError, match="no está disponible"):
            biblioteca_configurada.crear_prestamo("ISBN1", "U002")
    
    def test_crear_prestamo_usuario_no_existe(self, biblioteca_configurada):
        with pytest.raises(UsuarioNoExisteError, match="no existe"):
            biblioteca_configurada.crear_prestamo("ISBN1", "U999")
    
    def test_crear_prestamo_usuario_limite_excedido(self, biblioteca_configurada):
        for i in range(3, 8):
            biblioteca_configurada.agregar_libro(Libro(f"ISBN{i}", f"Libro {i}", "Autor"))
        
        for i in range(1, 6):
            biblioteca_configurada.crear_prestamo(f"ISBN{i}", "U001")
        
        with pytest.raises(ValueError, match="límite de préstamos"):
            biblioteca_configurada.crear_prestamo("ISBN6", "U001")
    
    def test_devolver_prestamo_exitoso(self, biblioteca_configurada):
        prestamo = biblioteca_configurada.crear_prestamo("ISBN1", "U001")
        
        resultado = biblioteca_configurada.devolver_prestamo(prestamo.id)
        
        assert resultado == True
        assert prestamo.esta_activo() == False
        
        libro = biblioteca_configurada.obtener_libro("ISBN1")
        assert libro.disponible == True
        
        usuario = biblioteca_configurada.obtener_usuario("U001")
        assert usuario.tiene_libro("ISBN1") == False
    
    def test_devolver_prestamo_no_existe(self, biblioteca_configurada):
        resultado = biblioteca_configurada.devolver_prestamo("PRESTAMO-FALSO")
        
        assert resultado == False
    
    def test_devolver_prestamo_ya_devuelto(self, biblioteca_configurada):
        prestamo = biblioteca_configurada.crear_prestamo("ISBN1", "U001")
        biblioteca_configurada.devolver_prestamo(prestamo.id)
        
        resultado = biblioteca_configurada.devolver_prestamo(prestamo.id)
        
        assert resultado == False
    
    def test_listar_prestamos_activos(self, biblioteca_configurada):
        prestamo1 = biblioteca_configurada.crear_prestamo("ISBN1", "U001")
        prestamo2 = biblioteca_configurada.crear_prestamo("ISBN2", "U002")
        
        biblioteca_configurada.devolver_prestamo(prestamo1.id)
        
        activos = biblioteca_configurada.listar_prestamos_activos()
        
        assert len(activos) == 1
        assert activos[0].id == prestamo2.id
    
    def test_listar_prestamos_usuario(self, biblioteca_configurada):
        biblioteca_configurada.agregar_libro(Libro("ISBN3", "Libro 3", "Autor"))
        
        biblioteca_configurada.crear_prestamo("ISBN1", "U001")
        biblioteca_configurada.crear_prestamo("ISBN2", "U001")
        biblioteca_configurada.crear_prestamo("ISBN3", "U002")
        
        prestamos_u001 = biblioteca_configurada.listar_prestamos_usuario("U001")
        
        assert len(prestamos_u001) == 2
        assert all(p.usuario_id == "U001" for p in prestamos_u001)
    
    def test_listar_prestamos_vencidos(self, biblioteca_configurada):
        from datetime import datetime, timedelta
        
        fecha_antigua = datetime.now() - timedelta(days=20)
        
        prestamo = biblioteca_configurada.crear_prestamo("ISBN1", "U001")
        
        prestamo._fecha_prestamo = fecha_antigua
        prestamo._fecha_limite = fecha_antigua + timedelta(days=14)
        
        vencidos = biblioteca_configurada.listar_prestamos_vencidos()
        
        assert len(vencidos) == 1
        assert vencidos[0].esta_vencido() == True