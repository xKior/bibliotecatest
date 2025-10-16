class Libro:
    
    def __init__(self, isbn: str, titulo: str, autor: str, disponible: bool = True):
        if not isbn or not isinstance(isbn, str):
            raise ValueError("ISBN debe ser una cadena no vacía")
        if not titulo or not isinstance(titulo, str):
            raise ValueError("Título debe ser una cadena no vacía")
        if not autor or not isinstance(autor, str):
            raise ValueError("Autor debe ser una cadena no vacía")
        
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor
        self._disponible = disponible
    
    @property
    def isbn(self) -> str:
        return self._isbn
    
    @property
    def titulo(self) -> str:
        return self._titulo
    
    @property
    def autor(self) -> str:
        return self._autor
    
    @property
    def disponible(self) -> bool:
        return self._disponible
    
    def prestar(self) -> bool:
        if not self._disponible:
            return False
        self._disponible = False
        return True
    
    def devolver(self) -> bool:
        if self._disponible:
            return False
        self._disponible = True
        return True
    
    def __str__(self) -> str:
        estado = "Disponible" if self._disponible else "Prestado"
        return f"{self._titulo} por {self._autor} (ISBN: {self._isbn}) - {estado}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Libro):
            return False
        return self._isbn == other._isbn