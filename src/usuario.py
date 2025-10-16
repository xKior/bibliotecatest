from typing import List

class Usuario:
    
    MAX_LIBROS = 5
    
    def __init__(self, id: str, nombre: str):
        if not id or not isinstance(id, str):
            raise ValueError("ID debe ser una cadena no vacía")
        if not nombre or not isinstance(nombre, str):
            raise ValueError("Nombre debe ser una cadena no vacía")
        
        self._id = id
        self._nombre = nombre
        self._libros_prestados: List[str] = [] 
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def libros_prestados(self) -> List[str]:
        return self._libros_prestados.copy()
    
    def agregar_prestamo(self, isbn: str) -> bool:
        if len(self._libros_prestados) >= self.MAX_LIBROS:
            raise ValueError(f"El usuario ha alcanzado el límite de {self.MAX_LIBROS} libros")
        if isbn in self._libros_prestados:
            return False
        self._libros_prestados.append(isbn)
        return True
    
    def remover_prestamo(self, isbn: str) -> bool:
        if isbn not in self._libros_prestados:
            return False
        self._libros_prestados.remove(isbn)
        return True
    
    def tiene_libro(self, isbn: str) -> bool:
        return isbn in self._libros_prestados
    
    def cantidad_prestamos(self) -> int:
        return len(self._libros_prestados)
    
    def puede_prestar(self) -> bool:
        return len(self._libros_prestados) < self.MAX_LIBROS
    
    def __str__(self) -> str:
        return f"Usuario: {self._nombre} (ID: {self._id}) - {len(self._libros_prestados)} libros prestados"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Usuario):
            return False
        return self._id == other._id