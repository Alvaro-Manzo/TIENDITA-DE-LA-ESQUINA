"""
Modelo de Venta
"""
from datetime import datetime
from typing import List, Dict

class ItemVenta:
    def __init__(self, codigo_barras: str, nombre: str, cantidad: int, 
                 precio_unitario: float, subtotal: float):
        self.codigo_barras = codigo_barras
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal
    
    def to_dict(self) -> dict:
        return {
            "codigo_barras": self.codigo_barras,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.subtotal
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'ItemVenta':
        return ItemVenta(
            codigo_barras=data["codigo_barras"],
            nombre=data["nombre"],
            cantidad=data["cantidad"],
            precio_unitario=data["precio_unitario"],
            subtotal=data["subtotal"]
        )

class Venta:
    def __init__(self, folio: str, cajero: str, items: List[ItemVenta], 
                 subtotal: float, iva: float, total: float, 
                 metodo_pago: str = "Efectivo"):
        self.folio = folio
        self.cajero = cajero
        self.items = items
        self.subtotal = subtotal
        self.iva = iva
        self.total = total
        self.metodo_pago = metodo_pago
        self.fecha = datetime.now().isoformat()
        self.cliente_rfc = None
        self.facturada = False
    
    def to_dict(self) -> dict:
        """Convierte la venta a diccionario"""
        return {
            "folio": self.folio,
            "cajero": self.cajero,
            "items": [item.to_dict() for item in self.items],
            "subtotal": self.subtotal,
            "iva": self.iva,
            "total": self.total,
            "metodo_pago": self.metodo_pago,
            "fecha": self.fecha,
            "cliente_rfc": self.cliente_rfc,
            "facturada": self.facturada
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Venta':
        """Crea una venta desde un diccionario"""
        items = [ItemVenta.from_dict(item) for item in data["items"]]
        venta = Venta(
            folio=data["folio"],
            cajero=data["cajero"],
            items=items,
            subtotal=data["subtotal"],
            iva=data["iva"],
            total=data["total"],
            metodo_pago=data.get("metodo_pago", "Efectivo")
        )
        venta.fecha = data["fecha"]
        venta.cliente_rfc = data.get("cliente_rfc")
        venta.facturada = data.get("facturada", False)
        return venta
    
    def marcar_facturada(self, rfc_cliente: str):
        """Marca la venta como facturada"""
        self.facturada = True
        self.cliente_rfc = rfc_cliente
    
    def __str__(self) -> str:
        return f"Venta {self.folio} - ${self.total:.2f} ({len(self.items)} items)"
