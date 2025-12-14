"""
Modelo de Producto
"""
from datetime import datetime
from typing import Optional

class Producto:
    def __init__(self, codigo_barras: str, nombre: str, precio: float, 
                 stock: int, categoria: str, proveedor: str = "",
                 precio_compra: float = 0.0, unidad: str = "pz"):
        self.codigo_barras = codigo_barras
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
        self.proveedor = proveedor
        self.precio_compra = precio_compra
        self.unidad = unidad
        self.fecha_creacion = datetime.now().isoformat()
        self.fecha_actualizacion = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convierte el producto a diccionario"""
        return {
            "codigo_barras": self.codigo_barras,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
            "categoria": self.categoria,
            "proveedor": self.proveedor,
            "precio_compra": self.precio_compra,
            "unidad": self.unidad,
            "fecha_creacion": self.fecha_creacion,
            "fecha_actualizacion": self.fecha_actualizacion
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Producto':
        """Crea un producto desde un diccionario"""
        producto = Producto(
            codigo_barras=data["codigo_barras"],
            nombre=data["nombre"],
            precio=data["precio"],
            stock=data["stock"],
            categoria=data["categoria"],
            proveedor=data.get("proveedor", ""),
            precio_compra=data.get("precio_compra", 0.0),
            unidad=data.get("unidad", "pz")
        )
        producto.fecha_creacion = data.get("fecha_creacion", datetime.now().isoformat())
        producto.fecha_actualizacion = data.get("fecha_actualizacion", datetime.now().isoformat())
        return producto
    
    def actualizar_stock(self, cantidad: int):
        """Actualiza el stock del producto"""
        self.stock += cantidad
        self.fecha_actualizacion = datetime.now().isoformat()
    
    def __str__(self) -> str:
        return f"{self.nombre} - ${self.precio:.2f} ({self.stock} {self.unidad})"
