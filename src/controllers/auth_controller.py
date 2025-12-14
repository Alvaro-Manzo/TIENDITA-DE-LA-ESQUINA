"""
Controlador de Autenticación
Maneja login, logout y gestión de usuarios
"""
import json
import os
from typing import Optional, List
from src.models.usuario import Usuario, RolUsuario

class AuthController:
    def __init__(self, data_path: str = "src/data/usuarios.json"):
        self.data_path = data_path
        self.usuarios: List[Usuario] = []
        self.usuario_actual: Optional[Usuario] = None
        self.cargar_usuarios()
    
    def cargar_usuarios(self):
        """Carga los usuarios desde el archivo JSON"""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.usuarios = [Usuario.from_dict(u) for u in data]
            except Exception as e:
                print(f"Error al cargar usuarios: {e}")
                self.usuarios = []
        else:
            self.usuarios = []
    
    def guardar_usuarios(self):
        """Guarda los usuarios en el archivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            with open(self.data_path, 'w', encoding='utf-8') as f:
                data = [u.to_dict() for u in self.usuarios]
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar usuarios: {e}")
    
    def login(self, username: str, password: str) -> bool:
        """Intenta hacer login con las credenciales proporcionadas"""
        username = (username or "").strip().lower()
        password = password or ""

        for usuario in self.usuarios:
            if (usuario.username or "").strip().lower() == username:
                if not usuario.activo:
                    return False
                if usuario.verificar_password(password):
                    self.usuario_actual = usuario
                    usuario.actualizar_acceso()
                    self.guardar_usuarios()
                    return True
                return False

        return False
    
    def logout(self):
        """Cierra la sesión del usuario actual"""
        self.usuario_actual = None
    
    def obtener_usuario_actual(self) -> Optional[Usuario]:
        """Obtiene el usuario actualmente logueado"""
        return self.usuario_actual
    
    def crear_usuario(self, username: str, password: str, rol: RolUsuario,
                     nombre_completo: str = "") -> bool:
        """Crea un nuevo usuario"""
        # Verificar que no exista
        for usuario in self.usuarios:
            if usuario.username == username:
                return False
        
        nuevo_usuario = Usuario(username, password, rol, nombre_completo)
        self.usuarios.append(nuevo_usuario)
        self.guardar_usuarios()
        return True
    
    def actualizar_usuario(self, username: str, **kwargs) -> bool:
        """Actualiza un usuario existente"""
        for usuario in self.usuarios:
            if usuario.username == username:
                if 'nombre_completo' in kwargs:
                    usuario.nombre_completo = kwargs['nombre_completo']
                if 'activo' in kwargs:
                    usuario.activo = kwargs['activo']
                if 'password' in kwargs:
                    usuario.password_hash = usuario._hash_password(kwargs['password'])
                self.guardar_usuarios()
                return True
        return False
    
    def eliminar_usuario(self, username: str) -> bool:
        """Elimina un usuario (lo desactiva)"""
        for usuario in self.usuarios:
            if usuario.username == username:
                usuario.activo = False
                self.guardar_usuarios()
                return True
        return False
    
    def obtener_todos_usuarios(self) -> List[Usuario]:
        """Obtiene todos los usuarios"""
        return self.usuarios
    
    def verificar_permiso(self, accion: str) -> bool:
        """Verifica si el usuario actual tiene permiso para una acción"""
        if self.usuario_actual:
            return self.usuario_actual.tiene_permiso(accion)
        return False
