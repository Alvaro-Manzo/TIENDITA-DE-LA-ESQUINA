"""
Vista de Inventario
Gestión de productos
"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.models.producto import Producto

class InventarioView(ttk.Frame):
    def __init__(self, parent, app, usuario):
        super().__init__(parent)
        self.app = app
        self.usuario = usuario
        self.pack(fill='both', expand=True)
        
        self.crear_interfaz()
        self.cargar_productos()
    
    def crear_interfaz(self):
        """Crea la interfaz de inventario"""
        # Título
        ttk.Label(self, text="📦 Gestión de Inventario",
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Frame de controles
        frame_controles = ttk.Frame(self)
        frame_controles.pack(fill='x', padx=10, pady=5)
        
        # Búsqueda
        ttk.Label(frame_controles, text="Buscar:").pack(side='left', padx=5)
        self.entry_buscar = ttk.Entry(frame_controles, width=30)
        self.entry_buscar.pack(side='left', padx=5)
        self.entry_buscar.bind('<KeyRelease>', lambda e: self.filtrar_productos())
        
        ttk.Button(frame_controles, text="🔍 Buscar",
                  command=self.filtrar_productos).pack(side='left', padx=5)
        
        # Filtro por categoría
        ttk.Label(frame_controles, text="Categoría:").pack(side='left', padx=5)
        categorias = ['Todas'] + self.app.producto_controller.obtener_todas_categorias()
        self.combo_categoria = ttk.Combobox(frame_controles,
                                           values=categorias,
                                           state='readonly',
                                           width=15)
        self.combo_categoria.set('Todas')
        self.combo_categoria.pack(side='left', padx=5)
        self.combo_categoria.bind('<<ComboboxSelected>>', lambda e: self.filtrar_productos())
        
        ttk.Button(frame_controles, text="🔄 Actualizar",
                  command=self.cargar_productos).pack(side='left', padx=5)
        
        # Botones de acción
        frame_acciones = ttk.Frame(self)
        frame_acciones.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_acciones, text="➕ Nuevo Producto",
                  style='Primary.TButton',
                  command=self.nuevo_producto).pack(side='left', padx=5)
        
        ttk.Button(frame_acciones, text="✏️ Editar",
                  command=self.editar_producto).pack(side='left', padx=5)
        
        ttk.Button(frame_acciones, text="📦 Ajustar Stock",
                  command=self.ajustar_stock).pack(side='left', padx=5)
        
        ttk.Button(frame_acciones, text="🗑️ Eliminar",
                  command=self.eliminar_producto).pack(side='left', padx=5)
        
        # Tabla de productos
        frame_tabla = ttk.Frame(self)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar_y = ttk.Scrollbar(frame_tabla)
        scrollbar_y.pack(side='right', fill='y')
        
        scrollbar_x = ttk.Scrollbar(frame_tabla, orient='horizontal')
        scrollbar_x.pack(side='bottom', fill='x')
        
        self.tree = ttk.Treeview(frame_tabla,
                                columns=('codigo', 'nombre', 'categoria', 'precio',
                                        'precio_compra', 'stock', 'proveedor'),
                                show='headings',
                                yscrollcommand=scrollbar_y.set,
                                xscrollcommand=scrollbar_x.set)
        
        self.tree.heading('codigo', text='Código de Barras')
        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('categoria', text='Categoría')
        self.tree.heading('precio', text='Precio Venta')
        self.tree.heading('precio_compra', text='Precio Compra')
        self.tree.heading('stock', text='Stock')
        self.tree.heading('proveedor', text='Proveedor')
        
        self.tree.column('codigo', width=120)
        self.tree.column('nombre', width=250)
        self.tree.column('categoria', width=100)
        self.tree.column('precio', width=100)
        self.tree.column('precio_compra', width=100)
        self.tree.column('stock', width=80)
        self.tree.column('proveedor', width=150)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Información de stock bajo
        frame_info = ttk.Frame(self)
        frame_info.pack(fill='x', padx=10, pady=5)
        
        self.lbl_stock_bajo = ttk.Label(frame_info,
                                       text="",
                                       foreground='red',
                                       font=('Arial', 9, 'bold'))
        self.lbl_stock_bajo.pack(side='left')
    
    def cargar_productos(self):
        """Carga todos los productos"""
        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        productos = self.app.producto_controller.obtener_todos_productos()
        
        for producto in productos:
            # Resaltar productos con stock bajo
            tags = ()
            if producto.stock <= 10:
                tags = ('stock_bajo',)
            
            self.tree.insert('', 'end', values=(
                producto.codigo_barras,
                producto.nombre,
                producto.categoria,
                f"${producto.precio:.2f}",
                f"${producto.precio_compra:.2f}",
                producto.stock,
                producto.proveedor
            ), tags=tags)
        
        # Configurar tag para stock bajo
        self.tree.tag_configure('stock_bajo', background='#FFCDD2')
        
        # Actualizar información de stock bajo
        productos_bajo_stock = self.app.producto_controller.obtener_productos_bajo_stock()
        if productos_bajo_stock:
            self.lbl_stock_bajo.config(
                text=f"⚠️ {len(productos_bajo_stock)} productos con stock bajo"
            )
        else:
            self.lbl_stock_bajo.config(text="✅ Stock adecuado en todos los productos")
    
    def filtrar_productos(self):
        """Filtra productos según búsqueda y categoría"""
        termino = self.entry_buscar.get().strip().lower()
        categoria = self.combo_categoria.get()
        
        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        productos = self.app.producto_controller.obtener_todos_productos()
        
        for producto in productos:
            # Filtrar por categoría
            if categoria != 'Todas' and producto.categoria != categoria:
                continue
            
            # Filtrar por término de búsqueda
            if termino:
                if (termino not in producto.nombre.lower() and
                    termino not in producto.codigo_barras.lower()):
                    continue
            
            tags = ()
            if producto.stock <= 10:
                tags = ('stock_bajo',)
            
            self.tree.insert('', 'end', values=(
                producto.codigo_barras,
                producto.nombre,
                producto.categoria,
                f"${producto.precio:.2f}",
                f"${producto.precio_compra:.2f}",
                producto.stock,
                producto.proveedor
            ), tags=tags)
        
        self.tree.tag_configure('stock_bajo', background='#FFCDD2')
    
    def nuevo_producto(self):
        """Abre ventana para crear nuevo producto"""
        ProductoDialog(self, self.app, None, self.cargar_productos)
    
    def editar_producto(self):
        """Edita el producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        item = self.tree.item(seleccion[0])
        codigo = item['values'][0]
        producto = self.app.producto_controller.buscar_por_codigo(codigo)
        
        ProductoDialog(self, self.app, producto, self.cargar_productos)
    
    def ajustar_stock(self):
        """Ajusta el stock del producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        item = self.tree.item(seleccion[0])
        codigo = item['values'][0]
        producto = self.app.producto_controller.buscar_por_codigo(codigo)
        
        StockDialog(self, self.app, producto, self.cargar_productos)
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        item = self.tree.item(seleccion[0])
        codigo = item['values'][0]
        nombre = item['values'][1]
        
        respuesta = messagebox.askyesno("Confirmar",
                                        f"¿Desea eliminar el producto?\n{nombre}")
        if respuesta:
            if self.app.producto_controller.eliminar_producto(codigo):
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.cargar_productos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")


class ProductoDialog:
    """Diálogo para crear/editar productos"""
    def __init__(self, parent, app, producto, callback):
        self.app = app
        self.producto = producto
        self.callback = callback
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Nuevo Producto" if not producto else "Editar Producto")
        self.ventana.geometry("500x600")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.crear_interfaz()
        
        if producto:
            self.cargar_datos()
    
    def crear_interfaz(self):
        """Crea la interfaz del diálogo"""
        frame = ttk.Frame(self.ventana, padding=20)
        frame.pack(fill='both', expand=True)
        
        # Código de barras
        ttk.Label(frame, text="Código de Barras:*").grid(
            row=0, column=0, sticky='w', pady=5)
        self.entry_codigo = ttk.Entry(frame, width=40)
        self.entry_codigo.grid(row=0, column=1, pady=5)
        
        # Nombre
        ttk.Label(frame, text="Nombre:*").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_nombre = ttk.Entry(frame, width=40)
        self.entry_nombre.grid(row=1, column=1, pady=5)
        
        # Categoría
        ttk.Label(frame, text="Categoría:*").grid(row=2, column=0, sticky='w', pady=5)
        categorias = self.app.producto_controller.obtener_todas_categorias()
        self.combo_categoria = ttk.Combobox(frame, values=categorias, width=37)
        self.combo_categoria.grid(row=2, column=1, pady=5)
        
        # Precio de venta
        ttk.Label(frame, text="Precio Venta:*").grid(row=3, column=0, sticky='w', pady=5)
        self.entry_precio = ttk.Entry(frame, width=40)
        self.entry_precio.grid(row=3, column=1, pady=5)
        
        # Precio de compra
        ttk.Label(frame, text="Precio Compra:").grid(row=4, column=0, sticky='w', pady=5)
        self.entry_precio_compra = ttk.Entry(frame, width=40)
        self.entry_precio_compra.grid(row=4, column=1, pady=5)
        
        # Stock
        ttk.Label(frame, text="Stock:*").grid(row=5, column=0, sticky='w', pady=5)
        self.entry_stock = ttk.Entry(frame, width=40)
        self.entry_stock.grid(row=5, column=1, pady=5)
        
        # Unidad
        ttk.Label(frame, text="Unidad:").grid(row=6, column=0, sticky='w', pady=5)
        self.combo_unidad = ttk.Combobox(frame,
                                        values=['pz', 'kg', 'lt', 'caja', 'paq'],
                                        state='readonly',
                                        width=37)
        self.combo_unidad.set('pz')
        self.combo_unidad.grid(row=6, column=1, pady=5)
        
        # Proveedor
        ttk.Label(frame, text="Proveedor:").grid(row=7, column=0, sticky='w', pady=5)
        self.entry_proveedor = ttk.Entry(frame, width=40)
        self.entry_proveedor.grid(row=7, column=1, pady=5)
        
        # Botones
        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=8, column=0, columnspan=2, pady=20)
        
        ttk.Button(frame_botones, text="💾 Guardar",
                  style='Primary.TButton',
                  command=self.guardar).pack(side='left', padx=5)
        
        ttk.Button(frame_botones, text="❌ Cancelar",
                  command=self.ventana.destroy).pack(side='left', padx=5)
    
    def cargar_datos(self):
        """Carga los datos del producto a editar"""
        self.entry_codigo.insert(0, self.producto.codigo_barras)
        self.entry_codigo.config(state='disabled')  # No se puede cambiar el código
        self.entry_nombre.insert(0, self.producto.nombre)
        self.combo_categoria.set(self.producto.categoria)
        self.entry_precio.insert(0, str(self.producto.precio))
        self.entry_precio_compra.insert(0, str(self.producto.precio_compra))
        self.entry_stock.insert(0, str(self.producto.stock))
        self.combo_unidad.set(self.producto.unidad)
        self.entry_proveedor.insert(0, self.producto.proveedor)
    
    def guardar(self):
        """Guarda el producto"""
        try:
            codigo = self.entry_codigo.get().strip()
            nombre = self.entry_nombre.get().strip()
            categoria = self.combo_categoria.get().strip()
            precio = float(self.entry_precio.get().strip())
            precio_compra = float(self.entry_precio_compra.get().strip() or 0)
            stock = int(self.entry_stock.get().strip())
            unidad = self.combo_unidad.get()
            proveedor = self.entry_proveedor.get().strip()
            
            if not codigo or not nombre or not categoria:
                messagebox.showwarning("Advertencia",
                                     "Complete los campos obligatorios (*)") 
                return
            
            if precio <= 0 or stock < 0:
                messagebox.showwarning("Advertencia",
                                     "Precio y stock deben ser valores válidos")
                return
            
            if self.producto:
                # Actualizar
                self.producto.nombre = nombre
                self.producto.categoria = categoria
                self.producto.precio = precio
                self.producto.precio_compra = precio_compra
                self.producto.stock = stock
                self.producto.unidad = unidad
                self.producto.proveedor = proveedor
                
                if self.app.producto_controller.actualizar_producto(self.producto):
                    messagebox.showinfo("Éxito", "Producto actualizado")
                    self.callback()
                    self.ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar")
            else:
                # Nuevo
                nuevo_producto = Producto(
                    codigo_barras=codigo,
                    nombre=nombre,
                    precio=precio,
                    stock=stock,
                    categoria=categoria,
                    proveedor=proveedor,
                    precio_compra=precio_compra,
                    unidad=unidad
                )
                
                if self.app.producto_controller.agregar_producto(nuevo_producto):
                    messagebox.showinfo("Éxito", "Producto agregado")
                    self.callback()
                    self.ventana.destroy()
                else:
                    messagebox.showerror("Error",
                                       "El código de barras ya existe")
        
        except ValueError:
            messagebox.showerror("Error", "Valores numéricos inválidos")


class StockDialog:
    """Diálogo para ajustar stock"""
    def __init__(self, parent, app, producto, callback):
        self.app = app
        self.producto = producto
        self.callback = callback
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Ajustar Stock")
        self.ventana.geometry("400x300")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz del diálogo"""
        frame = ttk.Frame(self.ventana, padding=20)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text=f"Producto: {self.producto.nombre}",
                 font=('Arial', 11, 'bold')).pack(pady=10)
        
        ttk.Label(frame, text=f"Stock actual: {self.producto.stock} {self.producto.unidad}",
                 font=('Arial', 10)).pack(pady=5)
        
        ttk.Label(frame, text="Tipo de ajuste:").pack(pady=10)
        
        self.var_tipo = tk.StringVar(value="entrada")
        ttk.Radiobutton(frame, text="➕ Entrada (agregar)",
                       variable=self.var_tipo,
                       value="entrada").pack(pady=5)
        ttk.Radiobutton(frame, text="➖ Salida (restar)",
                       variable=self.var_tipo,
                       value="salida").pack(pady=5)
        
        ttk.Label(frame, text="Cantidad:").pack(pady=10)
        self.entry_cantidad = ttk.Entry(frame, width=20)
        self.entry_cantidad.pack(pady=5)
        self.entry_cantidad.focus()
        
        frame_botones = ttk.Frame(frame)
        frame_botones.pack(pady=20)
        
        ttk.Button(frame_botones, text="💾 Guardar",
                  style='Primary.TButton',
                  command=self.guardar).pack(side='left', padx=5)
        
        ttk.Button(frame_botones, text="❌ Cancelar",
                  command=self.ventana.destroy).pack(side='left', padx=5)
    
    def guardar(self):
        """Guarda el ajuste de stock"""
        try:
            cantidad = int(self.entry_cantidad.get().strip())
            
            if cantidad <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a 0")
                return
            
            if self.var_tipo.get() == "salida":
                cantidad = -cantidad
                if self.producto.stock + cantidad < 0:
                    messagebox.showerror("Error", "Stock insuficiente")
                    return
            
            if self.app.producto_controller.actualizar_stock(
                self.producto.codigo_barras, cantidad):
                messagebox.showinfo("Éxito", "Stock actualizado")
                self.callback()
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el stock")
        
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida")
