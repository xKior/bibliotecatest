from typing import List, Optional, Dict
from datetime import datetime
import uuid
from src.libro import Libro
from src.usuario import Usuario
from src.prestamo import Prestamo

class LibroNoDisponibleError(Exception):
    pass

class UsuarioNoExisteError(Exception):
    pass

class LibroNoExisteError(Exception):
    pass

class Biblioteca:
    
    def __init__(self):
        self._catalogo: Dict[str, 'Libro'] = {} 
        self._usuarios: Dict[str, 'Usuario'] = {} 
        self._prestamos: Dict[str, 'Prestamo'] = {}  
    
    def agregar_libro(self, libro: 'Libro') -> bool:
        if libro.isbn in self._catalogo:
            return False
        self._catalogo[libro.isbn] = libro
        return True
    
    def obtener_libro(self, isbn: str) -> Optional['Libro']:
        return self._catalogo.get(isbn)
    
    def actualizar_libro(self, isbn: str, **kwargs) -> bool:
        if isbn not in self._catalogo:
            return False
        return True
    
    def eliminar_libro(self, isbn: str) -> bool:
        if isbn not in self._catalogo:
            return False
        if not self._catalogo[isbn].disponible:
            return False
        del self._catalogo[isbn]
        return True
    
    def buscar_libros(self, **criterios) -> List['Libro']:
        resultados = list(self._catalogo.values())
        
        if 'titulo' in criterios:
            titulo = criterios['titulo'].lower()
            resultados = [l for l in resultados if titulo in l.titulo.lower()]
        
        if 'autor' in criterios:
            autor = criterios['autor'].lower()
            resultados = [l for l in resultados if autor in l.autor.lower()]
        
        if 'disponible' in criterios:
            disponible = criterios['disponible']
            resultados = [l for l in resultados if l.disponible == disponible]
        
        return resultados
    
    def registrar_usuario(self, usuario: 'Usuario') -> bool:
        if usuario.id in self._usuarios:
            return False
        self._usuarios[usuario.id] = usuario
        return True
    
    def obtener_usuario(self, id: str) -> Optional['Usuario']:
        return self._usuarios.get(id)
    
    def eliminar_usuario(self, id: str) -> bool:
        if id not in self._usuarios:
            return False
        if self._usuarios[id].cantidad_prestamos() > 0:
            return False
        del self._usuarios[id]
        return True
    
    def crear_prestamo(self, libro_isbn: str, usuario_id: str) -> 'Prestamo':
        libro = self.obtener_libro(libro_isbn)
        if libro is None:
            raise LibroNoExisteError(f"Libro con ISBN {libro_isbn} no existe")
        if not libro.disponible:
            raise LibroNoDisponibleError(f"Libro {libro.titulo} no está disponible")
        
        usuario = self.obtener_usuario(usuario_id)
        if usuario is None:
            raise UsuarioNoExisteError(f"Usuario con ID {usuario_id} no existe")
        if not usuario.puede_prestar():
            raise ValueError(f"Usuario ha alcanzado el límite de préstamos")
        
        prestamo_id = str(uuid.uuid4())
        prestamo = Prestamo(prestamo_id, libro_isbn, usuario_id)
        
        libro.prestar()
        usuario.agregar_prestamo(libro_isbn)
        self._prestamos[prestamo_id] = prestamo
        
        return prestamo
    
    def devolver_prestamo(self, prestamo_id: str) -> bool:
        if prestamo_id not in self._prestamos:
            return False
        
        prestamo = self._prestamos[prestamo_id]
        if not prestamo.esta_activo():
            return False
        
        libro = self.obtener_libro(prestamo.libro_isbn)
        usuario = self.obtener_usuario(prestamo.usuario_id)
        
        if libro:
            libro.devolver()
        if usuario:
            usuario.remover_prestamo(prestamo.libro_isbn)
        
        prestamo.devolver()
        return True
    
    def obtener_prestamo(self, prestamo_id: str) -> Optional['Prestamo']:
        return self._prestamos.get(prestamo_id)
    
    def listar_prestamos_activos(self) -> List['Prestamo']:
        return [p for p in self._prestamos.values() if p.esta_activo()]
    
    def listar_prestamos_usuario(self, usuario_id: str) -> List['Prestamo']:
        return [p for p in self._prestamos.values() 
                if p.usuario_id == usuario_id and p.esta_activo()]
    
    def listar_prestamos_vencidos(self) -> List['Prestamo']:
        return [p for p in self._prestamos.values() if p.esta_vencido()]
    
    def total_libros(self) -> int:
        return len(self._catalogo)
    
    def total_usuarios(self) -> int:
        return len(self._usuarios)
    
    def total_prestamos_activos(self) -> int:
        return len(self.listar_prestamos_activos())