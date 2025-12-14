"""
Aplicación Principal - Sistema de Inventario
Tiendita de la Esquina v2.0
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import json

from src.controllers.auth_controller import AuthController
from src.controllers.producto_controller import ProductoController
from src.controllers.venta_controller import VentaController
from src.views.login_view import LoginView
from src.views.main_view import MainView
from src.utils.theme_manager import ThemeManager

class App:
    def __init__(self):
        self.root = tk.Tk()
        # Cargar configuración
        self.cargar_configuracion()

        # Título de la app (nombre configurable)
        self.root.title(
            f"{self.config.get('app_name','TIENDA PUMMAS')} - Sistema de Inventario v{self.config.get('version','2.0')}"
        )
        
        # Configurar ventana
        self.root.geometry(f"{self.config['ui']['window_width']}x{self.config['ui']['window_height']}")
        
        # Inicializar gestor de temas
        self.theme_manager = ThemeManager(self.config.get('theme', 'light'))
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Inicializar controladores
        self.auth_controller = AuthController()
        self.producto_controller = ProductoController()
        self.venta_controller = VentaController()
        
        # Vista actual
        self.vista_actual = None
        
        # Mostrar login
        self.mostrar_login()
    
    def cargar_configuracion(self):
        """Carga la configuración desde config.json"""
        try:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'config.json'
            )
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
            self.config = {
                'theme': 'light',
                'ui': {'window_width': 1400, 'window_height': 800}
            }
    
    def guardar_configuracion(self):
        """Guarda la configuración en config.json"""
        try:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'config.json'
            )
            self.config['theme'] = self.theme_manager.get_theme_name()
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
    
    def configurar_estilo(self):
        """Configura el estilo de la aplicación según el tema"""
        style = ttk.Style()
        
        # Obtener colores del tema
        colors = self.theme_manager.get_all_colors()
        
        # Configurar tema base
        if self.theme_manager.get_theme_name() == 'dark':
            try:
                style.theme_use('alt')  # Tema alternativo para mejor compatibilidad con oscuro
            except:
                style.theme_use('clam')
        else:
            style.theme_use('clam')
        
        # Configurar colores base
        self.root.configure(bg=colors['bg_secondary'])
        
        # Configurar estilos personalizados
        style.configure('TFrame', background=colors['bg_secondary'])
        style.configure('TLabel', 
                       background=colors['bg_secondary'], 
                       foreground=colors['fg_primary'])
        
        style.configure('TButton',
                       background=colors['button_bg'],
                       foreground=colors['button_fg'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=6)
        style.map('TButton',
                 background=[('active', colors['button_hover']),
                           ('pressed', colors['accent_hover'])])
        
        style.configure('Primary.TButton',
                       background=colors['accent_primary'],
                       foreground=colors['button_fg'],
                       font=('Arial', 10, 'bold'),
                       padding=8)
        style.map('Primary.TButton',
                 background=[('active', colors['accent_secondary']),
                           ('pressed', colors['accent_hover'])])
        
        style.configure('Title.TLabel',
                       font=('Arial', 24, 'bold'),
                       foreground=colors['accent_primary'],
                       background=colors['bg_secondary'])
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 14),
                       foreground=colors['fg_primary'],
                       background=colors['bg_secondary'])
        
        style.configure('TEntry',
                       fieldbackground=colors['input_bg'],
                       foreground=colors['fg_primary'],
                       bordercolor=colors['input_border'],
                       lightcolor=colors['input_border'],
                       darkcolor=colors['input_border'])
        
        style.configure('Treeview',
                       background=colors['tree_even'],
                       foreground=colors['fg_primary'],
                       fieldbackground=colors['tree_even'],
                       borderwidth=1)
        style.map('Treeview',
                 background=[('selected', colors['tree_selected'])],
                 foreground=[('selected', colors['fg_primary'])])
        
        style.configure('Treeview.Heading',
                       background=colors['bg_tertiary'],
                       foreground=colors['fg_primary'],
                       relief='flat')
        style.map('Treeview.Heading',
                 background=[('active', colors['accent_secondary'])])
        
        style.configure('TCombobox',
                       fieldbackground=colors['input_bg'],
                       background=colors['input_bg'],
                       foreground=colors['fg_primary'],
                       arrowcolor=colors['fg_primary'])
        
        style.configure('TNotebook',
                       background=colors['bg_secondary'])
        style.configure('TNotebook.Tab',
                       background=colors['bg_tertiary'],
                       foreground=colors['fg_primary'],
                       padding=[10, 5])
        style.map('TNotebook.Tab',
                 background=[('selected', colors['accent_primary'])],
                 foreground=[('selected', colors['button_fg'])])
        
        # Guardar colores para acceso rápido
        self.color_primario = colors['accent_primary']
        self.color_secundario = colors['accent_secondary']
        self.color_fondo = colors['bg_secondary']
        self.color_texto = colors['fg_primary']
        self.colors = colors
    
    def toggle_theme(self):
        """Cambia entre modo claro y oscuro"""
        self.theme_manager.toggle_theme()
        self.configurar_estilo()
        self.guardar_configuracion()
        
        # Recargar la vista actual
        if self.vista_actual:
            if hasattr(self, 'auth_controller') and self.auth_controller.obtener_usuario_actual():
                self.mostrar_sistema()
            else:
                self.mostrar_login()
    
    def mostrar_login(self):
        """Muestra la ventana de login"""
        if self.vista_actual:
            self.vista_actual.destroy()
        
        self.vista_actual = LoginView(self.root, self)
    
    def mostrar_sistema(self):
        """Muestra el sistema principal después del login"""
        if self.vista_actual:
            self.vista_actual.destroy()
        
        usuario = self.auth_controller.obtener_usuario_actual()
        if usuario:
            self.vista_actual = MainView(self.root, self, usuario)
        else:
            messagebox.showerror("Error", "No hay usuario autenticado")
            self.mostrar_login()
    
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        self.auth_controller.logout()
        self.mostrar_login()
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        # Centrar ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

def main():
    """Función principal"""
    app = App()
    app.ejecutar()

if __name__ == "__main__":
    main()
