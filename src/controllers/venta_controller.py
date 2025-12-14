"""
Controlador de Ventas
Maneja toda la lógica relacionada con ventas
"""
import json
import os
from datetime import datetime
from typing import List, Optional
from src.models.venta import Venta, ItemVenta
from src.models.producto import Producto

class VentaController:
    def __init__(self, data_path: str = "src/data/ventas.json"):
        self.data_path = data_path
        self.ventas: List[Venta] = []
        self.cargar_ventas()
    
    def cargar_ventas(self):
        """Carga las ventas desde el archivo JSON"""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.ventas = [Venta.from_dict(v) for v in data]
            except Exception as e:
                print(f"Error al cargar ventas: {e}")
                self.ventas = []
        else:
            self.ventas = []
    
    def guardar_ventas(self):
        """Guarda las ventas en el archivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            with open(self.data_path, 'w', encoding='utf-8') as f:
                data = [v.to_dict() for v in self.ventas]
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar ventas: {e}")
    
    def generar_folio(self) -> str:
        """Genera un nuevo folio para la venta"""
        fecha = datetime.now().strftime("%Y%m%d")
        numero = len([v for v in self.ventas if v.folio.startswith(fecha)]) + 1
        return f"{fecha}-{numero:04d}"
    
    def registrar_venta(self, venta: Venta) -> bool:
        """Registra una nueva venta"""
        try:
            self.ventas.append(venta)
            self.guardar_ventas()
            return True
        except Exception as e:
            print(f"Error al registrar venta: {e}")
            return False
    
    def buscar_venta(self, folio: str) -> Optional[Venta]:
        """Busca una venta por folio"""
        for venta in self.ventas:
            if venta.folio == folio:
                return venta
        return None

    def obtener_todas_ventas(self) -> List[Venta]:
        """Obtiene todas las ventas cargadas."""
        return self.ventas
    
    def obtener_ventas_por_fecha(self, fecha_inicio: str, fecha_fin: str) -> List[Venta]:
        """Obtiene ventas en un rango de fechas"""
        resultado = []
        for venta in self.ventas:
            fecha_venta = venta.fecha[:10]  # Solo la fecha, sin hora
            if fecha_inicio <= fecha_venta <= fecha_fin:
                resultado.append(venta)
        return resultado
    
    def obtener_ventas_cajero(self, cajero: str) -> List[Venta]:
        """Obtiene todas las ventas de un cajero"""
        return [v for v in self.ventas if v.cajero == cajero]
    
    def calcular_total_ventas(self, ventas: List[Venta]) -> float:
        """Calcula el total de una lista de ventas"""
        return sum(v.total for v in ventas)
    
    def obtener_ventas_del_dia(self) -> List[Venta]:
        """Obtiene las ventas del día actual"""
        hoy = datetime.now().strftime("%Y-%m-%d")
        return self.obtener_ventas_por_fecha(hoy, hoy)
    
    def obtener_productos_mas_vendidos(self, limite: int = 10) -> List[tuple]:
        """Obtiene los productos más vendidos"""
        productos_vendidos = {}
        
        for venta in self.ventas:
            for item in venta.items:
                codigo = item.codigo_barras
                if codigo in productos_vendidos:
                    productos_vendidos[codigo]['cantidad'] += item.cantidad
                    productos_vendidos[codigo]['total'] += item.subtotal
                else:
                    productos_vendidos[codigo] = {
                        'nombre': item.nombre,
                        'cantidad': item.cantidad,
                        'total': item.subtotal
                    }
        
        # Ordenar por cantidad vendida
        productos_ordenados = sorted(
            productos_vendidos.items(),
            key=lambda x: x[1]['cantidad'],
            reverse=True
        )
        
        return productos_ordenados[:limite]
    
    def obtener_reporte_ventas(self, fecha_inicio: str, fecha_fin: str) -> dict:
        """Genera un reporte de ventas para un período"""
        ventas = self.obtener_ventas_por_fecha(fecha_inicio, fecha_fin)
        
        total_ventas = len(ventas)
        total_dinero = self.calcular_total_ventas(ventas)
        
        # Ventas por cajero
        ventas_por_cajero = {}
        for venta in ventas:
            if venta.cajero in ventas_por_cajero:
                ventas_por_cajero[venta.cajero] += venta.total
            else:
                ventas_por_cajero[venta.cajero] = venta.total
        
        # Ventas por método de pago
        ventas_por_metodo = {}
        for venta in ventas:
            metodo = venta.metodo_pago
            if metodo in ventas_por_metodo:
                ventas_por_metodo[metodo] += venta.total
            else:
                ventas_por_metodo[metodo] = venta.total
        
        return {
            'periodo': f"{fecha_inicio} a {fecha_fin}",
            'total_ventas': total_ventas,
            'total_dinero': total_dinero,
            'promedio_venta': total_dinero / total_ventas if total_ventas > 0 else 0,
            'ventas_por_cajero': ventas_por_cajero,
            'ventas_por_metodo': ventas_por_metodo
        }
