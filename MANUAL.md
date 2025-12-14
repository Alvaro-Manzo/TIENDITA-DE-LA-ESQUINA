# 📖 Manual de Usuario - Tiendita de la Esquina

## 🚀 Inicio Rápido

### Requisitos
- Python 3.8 o superior
- macOS, Windows o Linux

### Instalación

1. **Instalar dependencias**:
```bash
./install.sh
```

O manualmente:
```bash
python3 -m pip install --user tkinter-tooltip pillow reportlab python-barcode qrcode
```

2. **Ejecutar la aplicación**:
```bash
./run.sh
```

O manualmente:
```bash
python src/main.py
```

## 👥 Usuarios del Sistema

El sistema incluye 3 usuarios predefinidos:

| Usuario | Contraseña | Rol | Permisos |
|---------|-----------|-----|----------|
| `owner` | `owner123` | OWNER | Acceso total al sistema |
| `admin` | `admin123` | ADMIN | Ventas, inventario y reportes |
| `cajero` | `cajero123` | CAJERO | Solo punto de venta |

## 📋 Funcionalidades

### 💰 Punto de Venta (Todos los roles con permiso de ventas)

1. **Buscar productos**:
   - Por código de barras (Enter para buscar)
   - Por nombre (búsqueda parcial)

2. **Agregar al carrito**:
   - Doble clic en el producto
   - O seleccionar y clic en "Agregar al Carrito"

3. **Gestionar carrito**:
   - Ver subtotal, IVA y total automáticamente
   - Eliminar productos individuales
   - Limpiar todo el carrito

4. **Procesar venta**:
   - Seleccionar método de pago (Efectivo, Tarjeta, Transferencia)
   - Clic en "COBRAR"
   - El sistema genera un folio único
   - Se actualiza automáticamente el inventario

### 📦 Gestión de Inventario (OWNER y ADMIN)

1. **Ver productos**:
   - Lista completa con todos los detalles
   - Productos con stock bajo resaltados en rojo
   - Filtrar por categoría
   - Buscar por nombre o código

2. **Agregar producto**:
   - Clic en "➕ Nuevo Producto"
   - Llenar formulario (campos con * son obligatorios)
   - Guardar

3. **Editar producto**:
   - Seleccionar producto
   - Clic en "✏️ Editar"
   - Modificar datos
   - Guardar

4. **Ajustar stock**:
   - Seleccionar producto
   - Clic en "📦 Ajustar Stock"
   - Elegir tipo: Entrada (agregar) o Salida (restar)
   - Ingresar cantidad

5. **Eliminar producto**:
   - Seleccionar producto
   - Clic en "🗑️ Eliminar"
   - Confirmar

### 📊 Reportes (OWNER y ADMIN)

#### Pestaña Ventas
- Ver ventas por período (Hoy, Semana, Mes)
- Resumen: Total de ventas, dinero generado, promedio
- Detalle de cada venta con folio, fecha, cajero, total

#### Pestaña Productos
- Top 20 productos más vendidos
- Cantidad vendida y total generado por producto

#### Pestaña Inventario
- Resumen del inventario
- Valor total del inventario
- Lista de productos con stock bajo

## 🏪 Catálogo de Productos Incluido

El sistema viene con **75+ productos mexicanos** precargados:

### Categorías:
- 🥤 **Refrescos**: Coca-Cola, Pepsi, Jarritos, Sprite, Fanta, etc.
- 💧 **Agua**: Ciel, Bonafont
- 🍟 **Botanas**: Sabritas, Doritos, Takis, Cheetos, Chips
- 🍬 **Dulces**: Gansito, Pingüinos, Mazapán, Pulparindo, Duvalín
- 🍺 **Cervezas**: Corona, Victoria, Modelo, Tecate, Indio, Sol
- 🥛 **Lácteos**: Leche Lala, yogurt, crema, queso
- 🥓 **Embutidos**: Jamón, salchicha FUD
- 🍞 **Panadería**: Pan Bimbo, tortillas
- 🌾 **Abarrotes**: Arroz, frijol, azúcar, sal, aceite, café
- 🧻 **Higiene y Limpieza**: Papel higiénico, jabón, detergente, cloro

## 💡 Consejos de Uso

### Para Cajeros:
1. Mantén el foco en la búsqueda para escanear códigos rápidamente
2. Usa Enter para buscar sin hacer clic
3. Doble clic en productos para agregar más rápido
4. Verifica el total antes de cobrar

### Para Administradores:
1. Revisa diariamente los productos con stock bajo
2. Actualiza precios según sea necesario
3. Mantén organizado el inventario por categorías
4. Genera reportes semanales para análisis

### Para Propietarios:
1. Revisa reportes de ventas regularmente
2. Identifica productos más vendidos para reabastecimiento
3. Analiza tendencias de venta
4. Gestiona usuarios según necesidad

## 🔒 Seguridad

- Las contraseñas se almacenan con hash SHA-256
- Cada usuario tiene permisos específicos
- Sistema de roles para control de acceso
- Sesiones individuales por usuario

## 📊 CFDI (Facturas Electrónicas)

El sistema está preparado para integración con CFDI:
- Configuración en `config.json`
- RFC de la tienda
- Régimen fiscal
- Estructura de datos compatible con CFDI 4.0

*Nota: La generación de XML CFDI requiere módulo adicional*

## 🔧 Configuración Avanzada

Edita `config.json` para:
- Cambiar tasa de IVA
- Ajustar umbral de stock bajo
- Configurar datos fiscales
- Activar/desactivar backups

## 🐛 Solución de Problemas

### La aplicación no inicia
```bash
# Verificar Python
python3 --version

# Reinstalar dependencias
pip install --user -r requirements.txt
```

### Error en importación de tkinter
```bash
# En macOS, tkinter viene con Python
# En Linux:
sudo apt-get install python3-tk
```

### Datos no se guardan
- Verifica permisos de escritura en carpeta `src/data/`
- Asegúrate de cerrar correctamente la aplicación

## 📝 Archivos de Datos

Los datos se almacenan en formato JSON:
- `src/data/productos.json` - Catálogo de productos
- `src/data/usuarios.json` - Usuarios del sistema
- `src/data/ventas.json` - Historial de ventas

**Importante**: Haz backups regulares de estos archivos

## 🤝 Soporte

Para dudas o problemas:
1. Revisa este manual
2. Verifica los logs de error
3. Consulta la documentación del código

## 📄 Licencia

Proyecto educativo - Uso libre para aprendizaje

---

**¡Gracias por usar Tiendita de la Esquina! 🏪**
