"""
Paquete de vistas
"""
from .login_view import LoginView
from .main_view import MainView
from .ventas_view import VentasView
from .inventario_view import InventarioView
from .reportes_view import ReportesView

__all__ = ['LoginView', 'MainView', 'VentasView', 'InventarioView', 'ReportesView']
