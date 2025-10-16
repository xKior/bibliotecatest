from datetime import datetime, timedelta
from typing import Optional

class Prestamo:
    
    DIAS_PRESTAMO = 14 
    
    def __init__(self, id: str, libro_isbn: str, usuario_id: str, 
                 fecha_prestamo: Optional[datetime] = None,
                 fecha_devolucion: Optional[datetime] = None):
        if not id or not isinstance(id, str):
            raise ValueError("ID debe ser una cadena no vacía")
        if not libro_isbn or not isinstance(libro_isbn, str):
            raise ValueError("ISBN del libro debe ser una cadena no vacía")
        if not usuario_id or not isinstance(usuario_id, str):
            raise ValueError("ID del usuario debe ser una cadena no vacía")
        
        self._id = id
        self._libro_isbn = libro_isbn
        self._usuario_id = usuario_id
        self._fecha_prestamo = fecha_prestamo or datetime.now()
        self._fecha_devolucion = fecha_devolucion
        self._fecha_limite = self._fecha_prestamo + timedelta(days=self.DIAS_PRESTAMO)
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def libro_isbn(self) -> str:
        return self._libro_isbn
    
    @property
    def usuario_id(self) -> str:
        return self._usuario_id
    
    @property
    def fecha_prestamo(self) -> datetime:
        return self._fecha_prestamo
    
    @property
    def fecha_devolucion(self) -> Optional[datetime]:
        return self._fecha_devolucion
    
    @property
    def fecha_limite(self) -> datetime:
        return self._fecha_limite
    
    def devolver(self, fecha: Optional[datetime] = None) -> bool:
        if self._fecha_devolucion is not None:
            return False
        self._fecha_devolucion = fecha or datetime.now()
        return True
    
    def esta_activo(self) -> bool:
        return self._fecha_devolucion is None
    
    def esta_vencido(self, fecha_actual: Optional[datetime] = None) -> bool:
        if not self.esta_activo():
            return False
        fecha = fecha_actual or datetime.now()
        return fecha > self._fecha_limite
    
    def dias_restantes(self, fecha_actual: Optional[datetime] = None) -> int:
        if not self.esta_activo():
            return 0
        fecha = fecha_actual or datetime.now()
        diferencia = self._fecha_limite - fecha
        return max(0, diferencia.days)
    
    def __str__(self) -> str:
        estado = "Activo" if self.esta_activo() else "Devuelto"
        return f"Préstamo {self._id}: Libro {self._libro_isbn} a Usuario {self._usuario_id} - {estado}"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Prestamo):
            return False
        return self._id == other._id