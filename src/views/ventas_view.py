"""
Vista de Ventas / Punto de Venta
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.models.venta import Venta, ItemVenta

class VentasView(ttk.Frame):
    def __init__(self, parent, app, usuario):
        super().__init__(parent)
        self.app = app
        self.usuario = usuario
        self.pack(fill='both', expand=True)
        
        self.carrito = []
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz del punto de venta"""
        # Título
        ttk.Label(self, text="💰 Punto de Venta",
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Frame principal dividido en dos columnas
        frame_principal = ttk.Frame(self)
        frame_principal.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Columna izquierda: Búsqueda y productos
        self.crear_panel_busqueda(frame_principal)
        
        # Columna derecha: Carrito y total
        self.crear_panel_carrito(frame_principal)
    
    def crear_panel_busqueda(self, parent):
        """Crea el panel de búsqueda de productos"""
        frame_izq = ttk.Frame(parent)
        frame_izq.pack(side='left', fill='both', expand=True, padx=5)
        
        # Búsqueda
        ttk.Label(frame_izq, text="Buscar Producto:",
                 font=('Arial', 11, 'bold')).pack(pady=5)
        
        frame_busqueda = ttk.Frame(frame_izq)
        frame_busqueda.pack(fill='x', pady=5)
        
        self.entry_busqueda = ttk.Entry(frame_busqueda, font=('Arial', 11))
        self.entry_busqueda.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.entry_busqueda.bind('<Return>', lambda e: self.buscar_producto())
        self.entry_busqueda.focus()
        
        ttk.Button(frame_busqueda, text="🔍 Buscar",
                  command=self.buscar_producto).pack(side='left')
        
        # Lista de resultados
        ttk.Label(frame_izq, text="Resultados:",
                 font=('Arial', 10, 'bold')).pack(pady=5)
        
        # Frame para treeview y scrollbar
        frame_tree = ttk.Frame(frame_izq)
        frame_tree.pack(fill='both', expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side='right', fill='y')
        
        self.tree_productos = ttk.Treeview(frame_tree,
                                          columns=('codigo', 'nombre', 'precio', 'stock'),
                                          show='headings',
                                          yscrollcommand=scrollbar.set,
                                          height=15)
        
        self.tree_productos.heading('codigo', text='Código')
        self.tree_productos.heading('nombre', text='Nombre')
        self.tree_productos.heading('precio', text='Precio')
        self.tree_productos.heading('stock', text='Stock')
        
        self.tree_productos.column('codigo', width=100)
        self.tree_productos.column('nombre', width=250)
        self.tree_productos.column('precio', width=80)
        self.tree_productos.column('stock', width=60)
        
        self.tree_productos.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree_productos.yview)
        
        # Doble clic para agregar al carrito
        self.tree_productos.bind('<Double-1>', lambda e: self.agregar_al_carrito())
        
        # Botón agregar
        ttk.Button(frame_izq, text="➕ Agregar al Carrito",
                  style='Primary.TButton',
                  command=self.agregar_al_carrito).pack(pady=10)
    
    def crear_panel_carrito(self, parent):
        """Crea el panel del carrito de compras"""
        frame_der = ttk.Frame(parent, width=400)
        frame_der.pack(side='right', fill='both', padx=5)
        frame_der.pack_propagate(False)
        
        # Título carrito
        ttk.Label(frame_der, text="🛒 Carrito de Compra",
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Lista del carrito
        frame_tree_carrito = ttk.Frame(frame_der)
        frame_tree_carrito.pack(fill='both', expand=True, pady=5)
        
        scrollbar_carrito = ttk.Scrollbar(frame_tree_carrito)
        scrollbar_carrito.pack(side='right', fill='y')
        
        self.tree_carrito = ttk.Treeview(frame_tree_carrito,
                                        columns=('cant', 'nombre', 'precio', 'subtotal'),
                                        show='headings',
                                        yscrollcommand=scrollbar_carrito.set,
                                        height=12)
        
        self.tree_carrito.heading('cant', text='Cant')
        self.tree_carrito.heading('nombre', text='Producto')
        self.tree_carrito.heading('precio', text='Precio')
        self.tree_carrito.heading('subtotal', text='Subtotal')
        
        self.tree_carrito.column('cant', width=50)
        self.tree_carrito.column('nombre', width=180)
        self.tree_carrito.column('precio', width=70)
        self.tree_carrito.column('subtotal', width=80)
        
        self.tree_carrito.pack(side='left', fill='both', expand=True)
        scrollbar_carrito.config(command=self.tree_carrito.yview)
        
        # Botón eliminar
        ttk.Button(frame_der, text="🗑️ Eliminar Seleccionado",
                  command=self.eliminar_del_carrito).pack(pady=5)
        
        ttk.Button(frame_der, text="🗑️ Limpiar Carrito",
                  command=self.limpiar_carrito).pack(pady=5)
        
        # Totales
        frame_totales = ttk.Frame(frame_der)
        frame_totales.pack(fill='x', pady=10, padx=10)
        
        ttk.Label(frame_totales, text="Subtotal:",
                 font=('Arial', 11)).grid(row=0, column=0, sticky='w', pady=2)
        self.lbl_subtotal = ttk.Label(frame_totales, text="$0.00",
                                     font=('Arial', 11, 'bold'))
        self.lbl_subtotal.grid(row=0, column=1, sticky='e', pady=2)
        
        ttk.Label(frame_totales, text="IVA (16%):",
                 font=('Arial', 11)).grid(row=1, column=0, sticky='w', pady=2)
        self.lbl_iva = ttk.Label(frame_totales, text="$0.00",
                                font=('Arial', 11, 'bold'))
        self.lbl_iva.grid(row=1, column=1, sticky='e', pady=2)
        
        ttk.Separator(frame_totales, orient='horizontal').grid(
            row=2, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(frame_totales, text="TOTAL:",
                 font=('Arial', 14, 'bold')).grid(row=3, column=0, sticky='w', pady=2)
        self.lbl_total = ttk.Label(frame_totales, text="$0.00",
                                  font=('Arial', 14, 'bold'),
                                  foreground=self.app.color_primario)
        self.lbl_total.grid(row=3, column=1, sticky='e', pady=2)
        
        frame_totales.columnconfigure(1, weight=1)
        
        # Método de pago
        ttk.Label(frame_der, text="Método de Pago:",
                 font=('Arial', 10)).pack(pady=(10, 5))
        self.combo_metodo_pago = ttk.Combobox(frame_der,
                                             values=['Efectivo', 'Tarjeta', 'Transferencia'],
                                             state='readonly',
                                             width=30)
        self.combo_metodo_pago.set('Efectivo')
        self.combo_metodo_pago.pack(pady=5)
        
        # Botón cobrar
        ttk.Button(frame_der, text="💵 COBRAR",
                  style='Primary.TButton',
                  command=self.procesar_venta).pack(pady=15, fill='x', padx=20)
    
    def buscar_producto(self):
        """Busca productos"""
        termino = self.entry_busqueda.get().strip()
        
        # Limpiar resultados
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        if not termino:
            return
        
        # Buscar por código o nombre
        producto = self.app.producto_controller.buscar_por_codigo(termino)
        if producto:
            resultados = [producto]
        else:
            resultados = self.app.producto_controller.buscar_por_nombre(termino)
        
        # Mostrar resultados
        for producto in resultados:
            self.tree_productos.insert('', 'end', values=(
                producto.codigo_barras,
                producto.nombre,
                f"${producto.precio:.2f}",
                producto.stock
            ))
    
    def agregar_al_carrito(self):
        """Agrega un producto al carrito"""
        seleccion = self.tree_productos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        item = self.tree_productos.item(seleccion[0])
        values = item.get('values') or []
        if not values:
            messagebox.showerror("Error", "No se pudo leer el producto seleccionado")
            return
        codigo = str(values[0]).strip()
        if not codigo:
            messagebox.showerror("Error", "Código de producto inválido")
            return
        
        producto = self.app.producto_controller.buscar_por_codigo(codigo)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        if producto.stock <= 0:
            messagebox.showerror("Error", "Producto sin stock")
            return
        
        # Verificar si ya está en el carrito
        for i, item_carrito in enumerate(self.carrito):
            if item_carrito['codigo'] == codigo:
                if item_carrito['cantidad'] < producto.stock:
                    self.carrito[i]['cantidad'] += 1
                    self.actualizar_carrito()
                else:
                    messagebox.showwarning("Advertencia", "No hay más stock disponible")
                return
        
        # Agregar nuevo item
        self.carrito.append({
            'codigo': producto.codigo_barras,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad': 1
        })
        
        self.actualizar_carrito()
        self.entry_busqueda.delete(0, tk.END)
        self.entry_busqueda.focus()
    
    def eliminar_del_carrito(self):
        """Elimina un producto del carrito"""
        seleccion = self.tree_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto del carrito")
            return
        
        idx = self.tree_carrito.index(seleccion[0])
        del self.carrito[idx]
        self.actualizar_carrito()
    
    def limpiar_carrito(self):
        """Limpia todo el carrito"""
        if self.carrito:
            respuesta = messagebox.askyesno("Confirmar",
                                           "¿Desea limpiar todo el carrito?")
            if respuesta:
                self.carrito = []
                self.actualizar_carrito()
    
    def actualizar_carrito(self):
        """Actualiza la vista del carrito"""
        # Limpiar tree
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        
        # Calcular totales
        subtotal = 0
        
        for item in self.carrito:
            item_subtotal = item['precio'] * item['cantidad']
            subtotal += item_subtotal
            
            self.tree_carrito.insert('', 'end', values=(
                item['cantidad'],
                item['nombre'],
                f"${item['precio']:.2f}",
                f"${item_subtotal:.2f}"
            ))
        
        iva = subtotal * 0.16
        total = subtotal + iva
        
        self.lbl_subtotal.config(text=f"${subtotal:.2f}")
        self.lbl_iva.config(text=f"${iva:.2f}")
        self.lbl_total.config(text=f"${total:.2f}")
    
    def procesar_venta(self):
        """Procesa la venta"""
        if not self.carrito:
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        # Verificar stock disponible
        for item in self.carrito:
            producto = self.app.producto_controller.buscar_por_codigo(item['codigo'])
            if producto.stock < item['cantidad']:
                messagebox.showerror("Error",
                                   f"Stock insuficiente para {producto.nombre}")
                return
        
        # Calcular totales
        subtotal = sum(item['precio'] * item['cantidad'] for item in self.carrito)
        iva = subtotal * 0.16
        total = subtotal + iva
        
        # Crear items de venta
        items_venta = []
        for item in self.carrito:
            item_subtotal = item['precio'] * item['cantidad']
            items_venta.append(ItemVenta(
                codigo_barras=item['codigo'],
                nombre=item['nombre'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio'],
                subtotal=item_subtotal
            ))
        
        # Crear venta
        folio = self.app.venta_controller.generar_folio()
        venta = Venta(
            folio=folio,
            cajero=self.usuario.username,
            items=items_venta,
            subtotal=subtotal,
            iva=iva,
            total=total,
            metodo_pago=self.combo_metodo_pago.get()
        )
        
        # Registrar venta
        if self.app.venta_controller.registrar_venta(venta):
            # Actualizar stock
            for item in self.carrito:
                self.app.producto_controller.actualizar_stock(
                    item['codigo'],
                    -item['cantidad']
                )
            
            messagebox.showinfo("Éxito",
                              f"Venta registrada\nFolio: {folio}\nTotal: ${total:.2f}")
            
            # Limpiar carrito
            self.carrito = []
            self.actualizar_carrito()
            self.entry_busqueda.focus()
        else:
            messagebox.showerror("Error", "No se pudo registrar la venta")
