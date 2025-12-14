"""
Vista de Login
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os

class LoginView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill='both', expand=True)
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de login"""
        # Botón de tema en la esquina superior derecha
        frame_tema = ttk.Frame(self)
        frame_tema.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        
        tema_icono = "🌙" if self.app.theme_manager.get_theme_name() == 'light' else "☀️"
        btn_tema = ttk.Button(frame_tema,
                             text=tema_icono,
                             command=self.cambiar_tema,
                             width=3)
        btn_tema.pack()
        
        # Frame central
        frame_central = ttk.Frame(self)
        frame_central.place(relx=0.5, rely=0.5, anchor='center')

        # Logo (imagen)
        self.logo_img = None
        try:
            # La imagen está en la raíz del repo, no dentro de src/
            repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            logo_path = os.path.join(repo_root, "Captura de Pantalla 2025-12-13 a la(s) 18.24.02.png")
            if os.path.exists(logo_path):
                from PIL import Image, ImageTk

                img = Image.open(logo_path)
                # Ajuste suave de tamaño para el login
                img.thumbnail((320, 320))
                self.logo_img = ImageTk.PhotoImage(img)
                ttk.Label(frame_central, image=self.logo_img).pack(pady=(0, 10))
        except Exception:
            # Si Pillow no está o el archivo no abre, solo omitimos el logo
            self.logo_img = None
        
        # Logo/Título
        ttk.Label(
            frame_central,
            text="🏪 TIENDA PUMMAS",
            style='Title.TLabel'
        ).pack(pady=10)
        
        ttk.Label(frame_central,
                 text="Sistema de Inventario y Punto de Venta v2.0",
                 style='Subtitle.TLabel').pack(pady=10)
        
        # Frame de formulario
        form_frame = ttk.Frame(frame_central)
        form_frame.pack(pady=30, padx=50)
        
        # Usuario
        ttk.Label(form_frame, text="Usuario:", font=('Arial', 11)).grid(
            row=0, column=0, sticky='w', pady=10, padx=5)
        self.entry_usuario = ttk.Entry(form_frame, width=30, font=('Arial', 11))
        self.entry_usuario.grid(row=0, column=1, pady=10, padx=5)
        self.entry_usuario.focus()
        
        # Contraseña
        ttk.Label(form_frame, text="Contraseña:", font=('Arial', 11)).grid(
            row=1, column=0, sticky='w', pady=10, padx=5)
        self.entry_password = ttk.Entry(form_frame, width=30, show='●', font=('Arial', 11))
        self.entry_password.grid(row=1, column=1, pady=10, padx=5)
        
        # Botón de login
        btn_login = ttk.Button(form_frame, 
                              text="Iniciar Sesión",
                              style='Primary.TButton',
                              command=self.hacer_login,
                              width=30)
        btn_login.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Bind Enter key
        self.entry_usuario.bind('<Return>', lambda e: self.entry_password.focus())
        self.entry_password.bind('<Return>', lambda e: self.hacer_login())
        
        # Información de usuarios de prueba
        info_frame = ttk.Frame(frame_central)
        info_frame.pack(pady=20)
        
        ttk.Label(info_frame, 
                 text="Usuarios de prueba:",
                 font=('Arial', 9, 'bold')).pack()
        ttk.Label(info_frame, 
                 text="owner/(tu password) | admin/admin123 | cajero/1234",
                 font=('Arial', 8),
                 foreground='gray').pack()
    
    def cambiar_tema(self):
        """Cambia el tema de la aplicación"""
        self.app.toggle_theme()
    
    def hacer_login(self):
        """Procesa el login"""
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get()
        
        if not usuario or not password:
            messagebox.showwarning("Advertencia", 
                                  "Por favor ingrese usuario y contraseña")
            return
        
        if self.app.auth_controller.login(usuario, password):
            usuario_obj = self.app.auth_controller.obtener_usuario_actual()
            messagebox.showinfo("Éxito", 
                              f"¡Bienvenido {usuario_obj.nombre_completo}!")
            self.app.mostrar_sistema()
        else:
            messagebox.showerror("Error", 
                               "Usuario o contraseña incorrectos")
            self.entry_password.delete(0, tk.END)
            self.entry_usuario.focus()
