"""
Vista de Reportes
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class ReportesView(ttk.Frame):
    def __init__(self, parent, app, usuario):
        super().__init__(parent)
        self.app = app
        self.usuario = usuario
        self.pack(fill='both', expand=True)
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de reportes"""
        # Título
        ttk.Label(self, text="📊 Reportes y Estadísticas",
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Notebook con pestañas
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña de ventas
        self.crear_pestaña_ventas(notebook)
        
        # Pestaña de productos
        self.crear_pestaña_productos(notebook)
        
        # Pestaña de inventario
        self.crear_pestaña_inventario(notebook)
    
    def crear_pestaña_ventas(self, notebook):
        """Crea la pestaña de reportes de ventas"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="💰 Ventas")
        
        # Controles de período
        frame_periodo = ttk.Frame(frame)
        frame_periodo.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_periodo, text="Período:",
                 font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        ttk.Button(frame_periodo, text="Hoy",
                  command=lambda: self.cargar_reporte_ventas('hoy')).pack(
                      side='left', padx=2)
        ttk.Button(frame_periodo, text="Semana",
                  command=lambda: self.cargar_reporte_ventas('semana')).pack(
                      side='left', padx=2)
        ttk.Button(frame_periodo, text="Mes",
                  command=lambda: self.cargar_reporte_ventas('mes')).pack(
                      side='left', padx=2)
        
        # Resumen
        frame_resumen = ttk.LabelFrame(frame, text="Resumen", padding=10)
        frame_resumen.pack(fill='x', padx=10, pady=10)
        
        info_frame = ttk.Frame(frame_resumen)
        info_frame.pack(fill='x')
        
        # Columna 1
        col1 = ttk.Frame(info_frame)
        col1.pack(side='left', expand=True, fill='both')
        
        ttk.Label(col1, text="Total Ventas:",
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.lbl_total_ventas = ttk.Label(col1, text="0",
                                         font=('Arial', 12, 'bold'))
        self.lbl_total_ventas.grid(row=0, column=1, sticky='e', padx=10, pady=5)
        
        ttk.Label(col1, text="Total Dinero:",
                 font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.lbl_total_dinero = ttk.Label(col1, text="$0.00",
                                         font=('Arial', 12, 'bold'),
                                         foreground=self.app.color_primario)
        self.lbl_total_dinero.grid(row=1, column=1, sticky='e', padx=10, pady=5)
        
        # Columna 2
        col2 = ttk.Frame(info_frame)
        col2.pack(side='left', expand=True, fill='both')
        
        ttk.Label(col2, text="Promedio Venta:",
                 font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.lbl_promedio_venta = ttk.Label(col2, text="$0.00",
                                           font=('Arial', 12, 'bold'))
        self.lbl_promedio_venta.grid(row=0, column=1, sticky='e', padx=10, pady=5)
        
        # Lista de ventas
        ttk.Label(frame, text="Detalle de Ventas:",
                 font=('Arial', 10, 'bold')).pack(padx=10, pady=5, anchor='w')
        
        frame_tabla = ttk.Frame(frame)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side='right', fill='y')
        
        self.tree_ventas = ttk.Treeview(frame_tabla,
                                       columns=('folio', 'fecha', 'cajero',
                                               'items', 'total', 'metodo'),
                                       show='headings',
                                       yscrollcommand=scrollbar.set)
        
        self.tree_ventas.heading('folio', text='Folio')
        self.tree_ventas.heading('fecha', text='Fecha/Hora')
        self.tree_ventas.heading('cajero', text='Cajero')
        self.tree_ventas.heading('items', text='Items')
        self.tree_ventas.heading('total', text='Total')
        self.tree_ventas.heading('metodo', text='Método Pago')
        
        self.tree_ventas.column('folio', width=120)
        self.tree_ventas.column('fecha', width=150)
        self.tree_ventas.column('cajero', width=100)
        self.tree_ventas.column('items', width=80)
        self.tree_ventas.column('total', width=100)
        self.tree_ventas.column('metodo', width=120)
        
        self.tree_ventas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree_ventas.yview)
        
        # Cargar datos del día
        self.cargar_reporte_ventas('hoy')
    
    def crear_pestaña_productos(self, notebook):
        """Crea la pestaña de productos más vendidos"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🏆 Productos")
        
        ttk.Label(frame, text="Productos Más Vendidos",
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        frame_tabla = ttk.Frame(frame)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side='right', fill='y')
        
        self.tree_productos = ttk.Treeview(frame_tabla,
                                          columns=('pos', 'nombre', 'cantidad', 'total'),
                                          show='headings',
                                          yscrollcommand=scrollbar.set)
        
        self.tree_productos.heading('pos', text='#')
        self.tree_productos.heading('nombre', text='Producto')
        self.tree_productos.heading('cantidad', text='Cantidad Vendida')
        self.tree_productos.heading('total', text='Total Generado')
        
        self.tree_productos.column('pos', width=50)
        self.tree_productos.column('nombre', width=300)
        self.tree_productos.column('cantidad', width=150)
        self.tree_productos.column('total', width=150)
        
        self.tree_productos.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree_productos.yview)
        
        ttk.Button(frame, text="🔄 Actualizar",
                  command=self.cargar_productos_mas_vendidos).pack(pady=10)
        
        self.cargar_productos_mas_vendidos()
    
    def crear_pestaña_inventario(self, notebook):
        """Crea la pestaña de estado del inventario"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📦 Inventario")
        
        ttk.Label(frame, text="Estado del Inventario",
                 font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Resumen
        frame_resumen = ttk.LabelFrame(frame, text="Resumen", padding=10)
        frame_resumen.pack(fill='x', padx=10, pady=10)
        
        productos = self.app.producto_controller.obtener_todos_productos()
        total_productos = len(productos)
        total_valor = sum(p.precio * p.stock for p in productos)
        productos_bajo_stock = len(self.app.producto_controller.obtener_productos_bajo_stock())
        
        info = [
            ("Total de Productos:", str(total_productos)),
            ("Valor Total Inventario:", f"${total_valor:,.2f}"),
            ("Productos con Stock Bajo:", str(productos_bajo_stock))
        ]
        
        for i, (etiqueta, valor) in enumerate(info):
            ttk.Label(frame_resumen, text=etiqueta,
                     font=('Arial', 10)).grid(row=i, column=0, sticky='w', pady=5)
            ttk.Label(frame_resumen, text=valor,
                     font=('Arial', 11, 'bold')).grid(row=i, column=1, sticky='e',
                                                     padx=20, pady=5)
        
        # Productos con stock bajo
        ttk.Label(frame, text="⚠️ Productos con Stock Bajo:",
                 font=('Arial', 10, 'bold'),
                 foreground='red').pack(padx=10, pady=10, anchor='w')
        
        frame_tabla = ttk.Frame(frame)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(frame_tabla)
        scrollbar.pack(side='right', fill='y')
        
        tree_stock = ttk.Treeview(frame_tabla,
                                 columns=('nombre', 'stock', 'categoria'),
                                 show='headings',
                                 yscrollcommand=scrollbar.set)
        
        tree_stock.heading('nombre', text='Producto')
        tree_stock.heading('stock', text='Stock')
        tree_stock.heading('categoria', text='Categoría')
        
        tree_stock.column('nombre', width=300)
        tree_stock.column('stock', width=100)
        tree_stock.column('categoria', width=150)
        
        tree_stock.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=tree_stock.yview)
        
        # Cargar productos con stock bajo
        productos_bajo = self.app.producto_controller.obtener_productos_bajo_stock()
        for producto in productos_bajo:
            tree_stock.insert('', 'end', values=(
                producto.nombre,
                f"{producto.stock} {producto.unidad}",
                producto.categoria
            ), tags=('alerta',))
        
        tree_stock.tag_configure('alerta', background='#FFCDD2')
    
    def cargar_reporte_ventas(self, periodo):
        """Carga el reporte de ventas según el período"""
        hoy = datetime.now()
        
        if periodo == 'hoy':
            fecha_inicio = hoy.strftime("%Y-%m-%d")
            fecha_fin = fecha_inicio
        elif periodo == 'semana':
            fecha_inicio = (hoy - timedelta(days=7)).strftime("%Y-%m-%d")
            fecha_fin = hoy.strftime("%Y-%m-%d")
        elif periodo == 'mes':
            fecha_inicio = (hoy - timedelta(days=30)).strftime("%Y-%m-%d")
            fecha_fin = hoy.strftime("%Y-%m-%d")
        
        ventas = self.app.venta_controller.obtener_ventas_por_fecha(
            fecha_inicio, fecha_fin)
        
        # Actualizar resumen
        total_ventas = len(ventas)
        total_dinero = sum(v.total for v in ventas)
        promedio = total_dinero / total_ventas if total_ventas > 0 else 0
        
        self.lbl_total_ventas.config(text=str(total_ventas))
        self.lbl_total_dinero.config(text=f"${total_dinero:,.2f}")
        self.lbl_promedio_venta.config(text=f"${promedio:,.2f}")
        
        # Actualizar tabla
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        
        for venta in reversed(ventas):  # Más recientes primero
            fecha_hora = datetime.fromisoformat(venta.fecha).strftime("%d/%m/%Y %H:%M")
            self.tree_ventas.insert('', 'end', values=(
                venta.folio,
                fecha_hora,
                venta.cajero,
                len(venta.items),
                f"${venta.total:.2f}",
                venta.metodo_pago
            ))
    
    def cargar_productos_mas_vendidos(self):
        """Carga los productos más vendidos"""
        productos_vendidos = self.app.venta_controller.obtener_productos_mas_vendidos(20)
        
        # Limpiar tabla
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        
        # Cargar datos
        for i, (codigo, datos) in enumerate(productos_vendidos, 1):
            self.tree_productos.insert('', 'end', values=(
                i,
                datos['nombre'],
                f"{datos['cantidad']} unidades",
                f"${datos['total']:,.2f}"
            ))
