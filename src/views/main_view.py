"""
Vista Principal del Sistema
Contiene el menú y las diferentes secciones
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.views.ventas_view import VentasView
from src.views.inventario_view import InventarioView
from src.views.reportes_view import ReportesView

class MainView(ttk.Frame):
    def __init__(self, parent, app, usuario):
        super().__init__(parent)
        self.app = app
        self.usuario = usuario
        self.pack(fill='both', expand=True)
        
        self.vista_actual = None
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz principal"""
        # Frame superior con información
        frame_superior = ttk.Frame(self, height=80)
        frame_superior.pack(fill='x', side='top')
        frame_superior.pack_propagate(False)
        
        # Título
        ttk.Label(
            frame_superior,
            text="🏪 TIENDA PUMMAS",
            font=('Arial', 18, 'bold'),
            foreground=self.app.color_primario
        ).pack(side='left', padx=20, pady=10)
        
        # Información del usuario
        frame_usuario = ttk.Frame(frame_superior)
        frame_usuario.pack(side='right', padx=20)
        
        ttk.Label(frame_usuario,
                 text=f"Usuario: {self.usuario.nombre_completo}",
                 font=('Arial', 10, 'bold')).pack(anchor='e')
        ttk.Label(frame_usuario,
                 text=f"Rol: {self.usuario.rol.value}",
                 font=('Arial', 9)).pack(anchor='e')
        
        # Frame de botones
        frame_botones = ttk.Frame(frame_usuario)
        frame_botones.pack(anchor='e', pady=5)
        
        # Botón cambiar tema
        tema_icono = "🌙" if self.app.theme_manager.get_theme_name() == 'light' else "☀️"
        btn_tema = ttk.Button(frame_botones,
                             text=tema_icono,
                             command=self.cambiar_tema,
                             width=3)
        btn_tema.pack(side='left', padx=2)
        
        btn_cerrar_sesion = ttk.Button(frame_botones,
                                       text="Cerrar Sesión",
                                       command=self.cerrar_sesion,
                                       width=15)
        btn_cerrar_sesion.pack(side='left', padx=2)
        
        # Separador
        ttk.Separator(self, orient='horizontal').pack(fill='x')
        
        # Frame de contenido (con menú lateral y área principal)
        frame_contenido = ttk.Frame(self)
        frame_contenido.pack(fill='both', expand=True)
        
        # Menú lateral
        self.crear_menu_lateral(frame_contenido)
        
        # Separador vertical
        ttk.Separator(frame_contenido, orient='vertical').pack(side='left', fill='y')
        
        # Área principal
        self.area_principal = ttk.Frame(frame_contenido)
        self.area_principal.pack(side='left', fill='both', expand=True)
        
        # Mostrar vista por defecto según rol
        if self.usuario.tiene_permiso('ventas'):
            self.mostrar_ventas()
        else:
            self.mostrar_inicio()
    
    def crear_menu_lateral(self, parent):
        """Crea el menú lateral"""
        frame_menu = ttk.Frame(parent, width=200)
        frame_menu.pack(side='left', fill='y')
        frame_menu.pack_propagate(False)
        
        ttk.Label(frame_menu,
                 text="MENÚ",
                 font=('Arial', 12, 'bold')).pack(pady=20)
        
        # Opciones de menú según permisos
        if self.usuario.tiene_permiso('ventas'):
            self.crear_boton_menu(frame_menu, "💰 Punto de Venta", self.mostrar_ventas)
        
        if self.usuario.tiene_permiso('productos'):
            self.crear_boton_menu(frame_menu, "📦 Inventario", self.mostrar_inventario)
        
        if self.usuario.tiene_permiso('reportes'):
            self.crear_boton_menu(frame_menu, "📊 Reportes", self.mostrar_reportes)
        
        # Separador
        ttk.Separator(frame_menu, orient='horizontal').pack(fill='x', pady=10)
        
        # Opciones adicionales para OWNER/ADMIN
        if self.usuario.rol.value in ['OWNER', 'ADMIN']:
            self.crear_boton_menu(frame_menu, "⚙️ Configuración", self.mostrar_configuracion)
    
    def crear_boton_menu(self, parent, texto, comando):
        """Crea un botón de menú"""
        btn = ttk.Button(parent,
                        text=texto,
                        command=comando,
                        width=25)
        btn.pack(pady=5, padx=10, fill='x')
    
    def limpiar_area_principal(self):
        """Limpia el área principal"""
        if self.vista_actual:
            self.vista_actual.destroy()
            self.vista_actual = None
    
    def mostrar_inicio(self):
        """Muestra la vista de inicio"""
        self.limpiar_area_principal()
        
        frame = ttk.Frame(self.area_principal)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame,
                 text="¡Bienvenido al Sistema!",
                 font=('Arial', 20, 'bold')).pack(pady=50)
        
        ttk.Label(frame,
                 text=f"Fecha: {datetime.now().strftime('%d/%m/%Y')}",
                 font=('Arial', 14)).pack(pady=10)
        
        self.vista_actual = frame
    
    def mostrar_ventas(self):
        """Muestra la vista de ventas"""
        self.limpiar_area_principal()
        self.vista_actual = VentasView(self.area_principal, self.app, self.usuario)
    
    def mostrar_inventario(self):
        """Muestra la vista de inventario"""
        self.limpiar_area_principal()
        self.vista_actual = InventarioView(self.area_principal, self.app, self.usuario)
    
    def mostrar_reportes(self):
        """Muestra la vista de reportes"""
        self.limpiar_area_principal()
        self.vista_actual = ReportesView(self.area_principal, self.app, self.usuario)
    
    def mostrar_configuracion(self):
        """Muestra la vista de configuración"""
        self.limpiar_area_principal()
        
        frame = ttk.Frame(self.area_principal)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame,
                 text="⚙️ Configuración",
                 font=('Arial', 18, 'bold')).pack(pady=20)
        
        ttk.Label(frame,
                 text="Próximamente: Configuración de sistema",
                 font=('Arial', 12)).pack(pady=10)
        
        self.vista_actual = frame
    
    def cerrar_sesion(self):
        """Cierra la sesión"""
        respuesta = messagebox.askyesno("Confirmar",
                                        "¿Está seguro que desea cerrar sesión?")
        if respuesta:
            self.app.cerrar_sesion()
    
    def cambiar_tema(self):
        """Cambia el tema de la aplicación"""
        self.app.toggle_theme()
