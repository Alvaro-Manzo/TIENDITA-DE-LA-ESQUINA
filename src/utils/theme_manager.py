"""
Módulo de Temas para la Aplicación
Maneja temas claro y oscuro
"""

class ThemeManager:
    """Gestor de temas de la aplicación"""
    
    # Tema Claro
    LIGHT_THEME = {
        'name': 'light',
        'bg_primary': '#FFFFFF',
        'bg_secondary': '#F5F5F5',
        'bg_tertiary': '#E0E0E0',
        'fg_primary': '#212121',
        'fg_secondary': '#424242',
        'fg_tertiary': '#757575',
        'accent_primary': '#2E7D32',
        'accent_secondary': '#66BB6A',
        'accent_hover': '#1B5E20',
        'success': '#4CAF50',
        'warning': '#FF9800',
        'error': '#F44336',
        'info': '#2196F3',
        'border': '#BDBDBD',
        'shadow': '#00000033',
        'input_bg': '#FFFFFF',
        'input_border': '#BDBDBD',
        'button_bg': '#2E7D32',
        'button_fg': '#FFFFFF',
        'button_hover': '#66BB6A',
        'tree_odd': '#FAFAFA',
        'tree_even': '#FFFFFF',
        'tree_selected': '#C8E6C9',
        'stock_low': '#FFCDD2',
        'stock_ok': '#C8E6C9'
    }
    
    # Tema Oscuro
    DARK_THEME = {
        'name': 'dark',
        'bg_primary': '#1E1E1E',
        'bg_secondary': '#252525',
        'bg_tertiary': '#2D2D2D',
        'fg_primary': '#E0E0E0',
        'fg_secondary': '#B0B0B0',
        'fg_tertiary': '#808080',
        'accent_primary': '#4CAF50',
        'accent_secondary': '#66BB6A',
        'accent_hover': '#81C784',
        'success': '#4CAF50',
        'warning': '#FFA726',
        'error': '#EF5350',
        'info': '#42A5F5',
        'border': '#404040',
        'shadow': '#00000066',
        'input_bg': '#2D2D2D',
        'input_border': '#404040',
        'button_bg': '#4CAF50',
        'button_fg': '#FFFFFF',
        'button_hover': '#66BB6A',
        'tree_odd': '#252525',
        'tree_even': '#2D2D2D',
        'tree_selected': '#1B5E20',
        'stock_low': '#B71C1C',
        'stock_ok': '#1B5E20'
    }
    
    def __init__(self, theme_name='light'):
        """Inicializa el gestor de temas"""
        self.current_theme = self.LIGHT_THEME if theme_name == 'light' else self.DARK_THEME
        self.theme_name = theme_name
    
    def get_color(self, color_key):
        """Obtiene un color del tema actual"""
        return self.current_theme.get(color_key, '#000000')
    
    def toggle_theme(self):
        """Cambia entre tema claro y oscuro"""
        if self.theme_name == 'light':
            self.current_theme = self.DARK_THEME
            self.theme_name = 'dark'
        else:
            self.current_theme = self.LIGHT_THEME
            self.theme_name = 'light'
        return self.theme_name
    
    def set_theme(self, theme_name):
        """Establece un tema específico"""
        if theme_name in ['light', 'dark']:
            self.theme_name = theme_name
            self.current_theme = self.LIGHT_THEME if theme_name == 'light' else self.DARK_THEME
            return True
        return False
    
    def get_theme_name(self):
        """Obtiene el nombre del tema actual"""
        return self.theme_name
    
    def get_all_colors(self):
        """Obtiene todos los colores del tema actual"""
        return self.current_theme.copy()
