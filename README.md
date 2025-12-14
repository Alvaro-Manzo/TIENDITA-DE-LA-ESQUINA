# 🏪 Sistema de Inventario - Tiendita de la Esquina

**Sistema de punto de venta e inventario completo para tiendas de abarrotes en México**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

---

## 📋 Características Principales

### 💰 Punto de Venta (POS)
- ✅ Búsqueda rápida por código de barras o nombre
- ✅ Carrito de compras interactivo
- ✅ Cálculo automático de IVA (16%)
- ✅ Múltiples métodos de pago (Efectivo, Tarjeta, Transferencia)
- ✅ Generación de folios únicos
- ✅ Actualización automática de inventario

### 📦 Gestión de Inventario
- ✅ Catálogo con 75+ productos mexicanos precargados
- ✅ Agregar, editar y eliminar productos
- ✅ Ajuste de stock (entradas y salidas)
- ✅ Alertas de stock bajo automáticas
- ✅ Filtrado por categoría
- ✅ Búsqueda avanzada

### 📊 Reportes y Estadísticas
- ✅ Reportes de ventas (Hoy, Semana, Mes)
- ✅ Productos más vendidos
- ✅ Análisis de inventario
- ✅ Estadísticas por cajero
- ✅ Valor total del inventario

### 👥 Sistema de Usuarios y Roles
- ✅ 3 niveles de acceso (Owner, Admin, Cajero)
- ✅ Contraseñas encriptadas (SHA-256)
- ✅ Control de permisos por rol
- ✅ Registro de último acceso

### 🇲🇽 Productos Mexicanos Incluidos
- 🥤 Refrescos: Coca-Cola, Pepsi, Jarritos, Sprite, Fanta
- 💧 Agua: Ciel, Bonafont
- 🍟 Botanas: Sabritas, Doritos, Takis, Cheetos
- 🍬 Dulces: Gansito, Pingüinos, Mazapán, Pulparindo
- 🍺 Cervezas: Corona, Victoria, Modelo, Tecate
- 🥛 Lácteos: Lala, FUD
- 🌾 Abarrotes: Arroz, frijol, azúcar, café
- 🧻 Y más...

---

## 🚀 Instalación Rápida

### Opción 1: Script Automático (Recomendado)
```bash
# Clonar o descargar el proyecto
cd TIENDITADELAESQUINA

# Ejecutar instalador
./install.sh

# Iniciar aplicación
./run.sh
```

### Opción 2: Manual
```bash
# Instalar dependencias
python3 -m pip install --user tkinter-tooltip pillow reportlab python-barcode qrcode

# Ejecutar aplicación
python3 src/main.py
```

---

## 👥 Usuarios Predeterminados

| Usuario | Contraseña | Rol | Permisos |
|---------|-----------|-----|----------|
| **owner** | `owner123` | OWNER | 🔓 Acceso total |
| **admin** | `admin123` | ADMIN | 🔐 Ventas, inventario, reportes |
| **cajero** | `cajero123` | CAJERO | 🔒 Solo punto de venta |

---

## 📸 Capturas de Pantalla

### 🔐 Pantalla de Login
Inicio de sesión seguro con roles diferenciados

### 💰 Punto de Venta
Interfaz intuitiva para ventas rápidas con búsqueda por código de barras

### 📦 Gestión de Inventario
Control completo de productos con alertas de stock bajo

### � Reportes
Estadísticas detalladas y análisis de ventas

---

## �📁 Estructura del Proyecto

```
TIENDITADELAESQUINA/
│
├── src/
│   ├── main.py                    # 🚀 Punto de entrada de la aplicación
│   │
│   ├── models/                    # 📊 Modelos de datos
│   │   ├── __init__.py
│   │   ├── producto.py           # Modelo de productos
│   │   ├── usuario.py            # Modelo de usuarios
│   │   └── venta.py              # Modelo de ventas
│   │
│   ├── controllers/               # 🎮 Controladores (lógica de negocio)
│   │   ├── __init__.py
│   │   ├── auth_controller.py    # Autenticación
│   │   ├── producto_controller.py # Gestión de productos
│   │   └── venta_controller.py   # Gestión de ventas
│   │
│   ├── views/                     # 🖼️ Interfaces gráficas
│   │   ├── __init__.py
│   │   ├── login_view.py         # Vista de login
│   │   ├── main_view.py          # Vista principal
│   │   ├── ventas_view.py        # Vista de ventas/POS
│   │   ├── inventario_view.py    # Vista de inventario
│   │   └── reportes_view.py      # Vista de reportes
│   │
│   └── data/                      # 💾 Base de datos JSON
│       ├── productos.json         # 75+ productos mexicanos
│       ├── usuarios.json          # Usuarios del sistema
│       └── ventas.json            # Historial de ventas
│
├── config.json                    # ⚙️ Configuración del sistema
├── requirements.txt               # 📦 Dependencias Python
├── install.sh                     # 🔧 Script de instalación
├── run.sh                         # ▶️ Script de ejecución
├── README.md                      # 📖 Este archivo
└── MANUAL.md                      # 📚 Manual de usuario completo
```

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|-----------|-----|
| **Python 3.8+** | Lenguaje principal |
| **Tkinter** | Interfaz gráfica nativa |
| **JSON** | Base de datos ligera |
| **ReportLab** | Generación de PDFs |
| **Python-Barcode** | Códigos de barras |
| **QRCode** | Códigos QR |
| **Hashlib** | Encriptación de contraseñas |

---

## 📖 Guía de Uso Rápida

### Para Cajeros 💰
1. Login con usuario `cajero`
2. Buscar producto por código de barras o nombre
3. Agregar al carrito
4. Seleccionar método de pago
5. Cobrar y generar ticket

### Para Administradores 👨‍💼
1. Login con usuario `admin` o `owner`
2. Acceder a Inventario para gestionar productos
3. Ajustar stock cuando sea necesario
4. Revisar reportes de ventas
5. Identificar productos de alto movimiento

### Para Propietarios 👑
1. Login con usuario `owner`
2. Acceso completo a todas las funcionalidades
3. Gestión de usuarios (próximamente)
4. Configuración del sistema
5. Análisis completo del negocio

---

## 🔐 Seguridad

- 🔒 Contraseñas encriptadas con SHA-256
- 👤 Sistema de roles y permisos
- 📝 Registro de accesos por usuario
- 🚫 Validación de permisos en cada acción

---

## 💡 Características Técnicas

### Arquitectura
- **Patrón MVC**: Modelo-Vista-Controlador
- **Modular**: Fácil de mantener y extender
- **Escalable**: Preparado para crecer

### Base de Datos
- **JSON**: Ligera y portable
- **Sin instalación**: No requiere servidor de BD
- **Fácil respaldo**: Solo copiar archivos

### Interfaz
- **Responsive**: Se adapta a diferentes tamaños
- **Intuitiva**: Diseño amigable
- **Atajos de teclado**: Para mayor velocidad

---

## 📊 Estadísticas del Proyecto

- 📦 **75+ productos** mexicanos precargados
- 🏷️ **10 categorías** de productos
- � **3 roles** de usuario
- 🎨 **5 vistas** principales
- �📝 **2000+ líneas** de código
- ✅ **100%** Python puro

---

## 🔮 Próximas Características

- [ ] 🧾 Generación de tickets PDF
- [ ] 📧 Envío de tickets por email
- [ ] 📱 Versión móvil (Android/iOS)
- [ ] ☁️ Sincronización en la nube
- [ ] 📈 Gráficas de ventas
- [ ] 🏪 Soporte multi-sucursal
- [ ] 🧮 Generación XML CFDI 4.0
- [ ] 📲 Lectura de código de barras con cámara
- [ ] 💳 Integración con terminales bancarias
- [ ] 🔔 Notificaciones push

---

## 🤝 Contribuciones

Este es un proyecto educativo. Si deseas mejorarlo:

1. Fork el proyecto
2. Crea tu rama de características
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

## ⚠️ Requisitos del Sistema

### Mínimos
- **OS**: macOS 10.12+, Windows 7+, Linux (cualquier distro)
- **RAM**: 512 MB
- **Disco**: 50 MB
- **Python**: 3.8 o superior

### Recomendados
- **OS**: macOS 11+, Windows 10+, Ubuntu 20.04+
- **RAM**: 2 GB
- **Disco**: 100 MB
- **Python**: 3.10 o superior

---

## 📞 Soporte

Para preguntas, problemas o sugerencias:

1. 📖 Revisa el **MANUAL.md** completo
2. 🔍 Busca en los issues existentes
3. 💬 Crea un nuevo issue si es necesario

---

## 📄 Licencia

Este proyecto es de **uso educativo**. Libre para aprender, modificar y distribuir.

---

## 🙏 Agradecimientos

Desarrollado con ❤️ para la comunidad educativa mexicana.

Productos y marcas mencionadas son propiedad de sus respectivos dueños.

---

## 📚 Documentación Adicional

- 📖 [Manual de Usuario Completo](MANUAL.md)
- 🔧 [Configuración Avanzada](config.json)
- 💾 [Estructura de Datos](src/data/)

---

<div align="center">

### ⭐ Si te gusta este proyecto, dale una estrella ⭐

**Hecho en México 🇲🇽 con Python 🐍**

[Reportar Bug](https://github.com) • [Solicitar Feature](https://github.com) • [Ver Documentación](MANUAL.md)

</div>

---

## 🎓 Ideal para:

- 📚 **Estudiantes** aprendiendo Python y desarrollo de software
- 🏪 **Pequeños negocios** que necesitan un sistema simple
- 👨‍💻 **Desarrolladores** que quieren un ejemplo de arquitectura MVC
- 🎯 **Proyectos escolares** de programación
- 🔧 **Base** para sistemas más complejos

---

**¿Listo para comenzar? ¡Ejecuta `./run.sh` y empieza a vender! 🚀**
