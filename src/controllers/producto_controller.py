"""
Controlador de Productos
Maneja toda la lógica relacionada con productos
"""
import json
import os
from typing import List, Optional
from src.models.producto import Producto

class ProductoController:
    def __init__(self, data_path: str = "src/data/productos.json"):
        self.data_path = data_path
        self.productos: List[Producto] = []
        self.cargar_productos()
    
    def cargar_productos(self):
        """Carga los productos desde el archivo JSON"""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.productos = [Producto.from_dict(p) for p in data]
            except Exception as e:
                print(f"Error al cargar productos: {e}")
                self.productos = []
        else:
            self.productos = []
    
    def guardar_productos(self):
        """Guarda los productos en el archivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            with open(self.data_path, 'w', encoding='utf-8') as f:
                data = [p.to_dict() for p in self.productos]
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar productos: {e}")
    
    def buscar_por_codigo(self, codigo_barras: str) -> Optional[Producto]:
        """Busca un producto por código de barras"""
        for producto in self.productos:
            if producto.codigo_barras == codigo_barras:
                return producto
        return None
    
    def buscar_por_nombre(self, termino: str) -> List[Producto]:
        """Busca productos por nombre (búsqueda parcial)"""
        termino = termino.lower()
        resultados = []
        for producto in self.productos:
            if termino in producto.nombre.lower():
                resultados.append(producto)
        return resultados
    
    def buscar_por_categoria(self, categoria: str) -> List[Producto]:
        """Busca productos por categoría"""
        return [p for p in self.productos if p.categoria == categoria]
    
    def agregar_producto(self, producto: Producto) -> bool:
        """Agrega un nuevo producto"""
        if self.buscar_por_codigo(producto.codigo_barras):
            return False  # Ya existe
        self.productos.append(producto)
        self.guardar_productos()
        return True
    
    def actualizar_producto(self, producto: Producto) -> bool:
        """Actualiza un producto existente"""
        for i, p in enumerate(self.productos):
            if p.codigo_barras == producto.codigo_barras:
                self.productos[i] = producto
                self.guardar_productos()
                return True
        return False
    
    def eliminar_producto(self, codigo_barras: str) -> bool:
        """Elimina un producto"""
        for i, p in enumerate(self.productos):
            if p.codigo_barras == codigo_barras:
                del self.productos[i]
                self.guardar_productos()
                return True
        return False
    
    def actualizar_stock(self, codigo_barras: str, cantidad: int) -> bool:
        """Actualiza el stock de un producto"""
        producto = self.buscar_por_codigo(codigo_barras)
        if producto:
            producto.actualizar_stock(cantidad)
            self.guardar_productos()
            return True
        return False
    
    def obtener_productos_bajo_stock(self, umbral: int = 10) -> List[Producto]:
        """Obtiene productos con stock bajo"""
        return [p for p in self.productos if p.stock <= umbral]
    
    def obtener_todas_categorias(self) -> List[str]:
        """Obtiene todas las categorías únicas"""
        categorias = set(p.categoria for p in self.productos)
        return sorted(list(categorias))
    
    def obtener_todos_productos(self) -> List[Producto]:
        """Obtiene todos los productos"""
        return self.productos
