"""
Modelo de Usuario
"""
from datetime import datetime
from enum import Enum
import hashlib

class RolUsuario(Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    CAJERO = "CAJERO"

class Usuario:
    def __init__(self, username: str, password: str, rol: RolUsuario, 
                 nombre_completo: str = ""):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.rol = rol if isinstance(rol, RolUsuario) else RolUsuario[rol]
        self.nombre_completo = nombre_completo or username
        self.activo = True
        self.fecha_creacion = datetime.now().isoformat()
        self.ultimo_acceso = None
    
    def _hash_password(self, password: str) -> str:
        """Hash de la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verificar_password(self, password: str) -> bool:
        """Verifica si la contraseña es correcta"""
        return self.password_hash == self._hash_password(password)
    
    def actualizar_acceso(self):
        """Actualiza la fecha de último acceso"""
        self.ultimo_acceso = datetime.now().isoformat()
    
    def tiene_permiso(self, accion: str) -> bool:
        """Verifica si el usuario tiene permiso para realizar una acción"""
        permisos = {
            RolUsuario.OWNER: ["*"],  # Todos los permisos
            RolUsuario.ADMIN: ["ventas", "productos", "reportes", "inventario"],
            RolUsuario.CAJERO: ["ventas"]
        }
        
        permisos_rol = permisos.get(self.rol, [])
        return "*" in permisos_rol or accion in permisos_rol
    
    def to_dict(self) -> dict:
        """Convierte el usuario a diccionario"""
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "rol": self.rol.value,
            "nombre_completo": self.nombre_completo,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion,
            "ultimo_acceso": self.ultimo_acceso
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Usuario':
        """Crea un usuario desde un diccionario"""
        usuario = Usuario.__new__(Usuario)
        usuario.username = data["username"]
        usuario.password_hash = data["password_hash"]
        usuario.rol = RolUsuario[data["rol"]]
        usuario.nombre_completo = data.get("nombre_completo", data["username"])
        usuario.activo = data.get("activo", True)
        usuario.fecha_creacion = data.get("fecha_creacion", datetime.now().isoformat())
        usuario.ultimo_acceso = data.get("ultimo_acceso")
        return usuario
    
    def __str__(self) -> str:
        return f"{self.nombre_completo} ({self.rol.value})"
