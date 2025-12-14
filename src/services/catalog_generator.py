"""src/services/catalog_generator.py

Genera un catálogo grande y consistente de productos para una tienda de abarrotes.

Objetivo:
- Generar MUCHOS productos sin errores de JSON.
- Evitar duplicados por codigo_barras.
- Mantener campos obligatorios: codigo_barras, nombre, precio, stock, categoria, proveedor, precio_compra, unidad.

Nota:
- No intenta replicar todos los UPC/EAN reales de México (no es viable ni deseable).
- Genera códigos internos EAN-13 válidos con prefijos reservados para uso interno.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class ProductTemplate:
    categoria: str
    unidad: str
    base_precio: float
    base_compra: float
    nombres: List[str]


def _ean13_check_digit(d12: str) -> str:
    """Calcula dígito verificador EAN-13 para 12 dígitos."""
    if len(d12) != 12 or not d12.isdigit():
        raise ValueError("Se requieren 12 dígitos para calcular EAN-13")

    s = 0
    for i, ch in enumerate(d12):
        n = int(ch)
        s += n if (i % 2 == 0) else n * 3
    cd = (10 - (s % 10)) % 10
    return str(cd)


def make_internal_ean13(prefix: str, seq: int) -> str:
    """Genera EAN-13 interno.

    prefix: 3 dígitos (ej: '990' reservado interno)
    seq: entero >= 0 (se convierte a 9 dígitos)
    """
    if len(prefix) != 3 or not prefix.isdigit():
        raise ValueError("prefix debe tener 3 dígitos")
    body = f"{seq:09d}"  # 9 dígitos
    d12 = prefix + body
    return d12 + _ean13_check_digit(d12)


def generate_catalog(
    size_multiplier: int = 8,
    base_stock: int = 30,
    prefix: str = "990",
) -> List[Dict]:
    """Genera un catálogo grande.

    size_multiplier:
      - Controla cuántas variaciones se crean por producto base.
      - 8 genera cientos; 20 genera miles.

    base_stock:
      - Stock inicial aproximado.

    prefix:
      - Prefijo EAN-13 interno.
    """

    # Plantillas por categoría (nombres comunes, sin necesidad de recetas/códigos reales)
    templates: List[ProductTemplate] = [
        ProductTemplate(
            categoria="Refrescos",
            unidad="pz",
            base_precio=15.0,
            base_compra=10.5,
            nombres=[
                "Cola 600ml",
                "Cola 2L",
                "Cola 355ml Lata",
                "Naranja 600ml",
                "Limón 600ml",
                "Manzana 600ml",
                "Toronja 600ml",
                "Sabor Uva 600ml",
                "Sabor Piña 600ml",
            ],
        ),
        ProductTemplate(
            categoria="Agua",
            unidad="pz",
            base_precio=10.0,
            base_compra=6.5,
            nombres=[
                "Agua Natural 600ml",
                "Agua Natural 1.5L",
                "Agua Mineral 600ml",
                "Agua Saborizada 600ml",
                "Agua Natural 1L",
                "Agua Mineral 1.5L",
            ],
        ),
        ProductTemplate(
            categoria="Jugos",
            unidad="pz",
            base_precio=22.0,
            base_compra=16.0,
            nombres=[
                "Jugo Naranja 1L",
                "Jugo Manzana 1L",
                "Jugo Durazno 1L",
                "Néctar Mango 1L",
                "Néctar Guayaba 1L",
                "Bebida Frutal 500ml",
            ],
        ),
        ProductTemplate(
            categoria="Energéticas",
            unidad="pz",
            base_precio=35.0,
            base_compra=24.0,
            nombres=[
                "Energética 473ml",
                "Energética 355ml",
                "Energética Sin Azúcar 473ml",
            ],
        ),
        ProductTemplate(
            categoria="Cerveza",
            unidad="pz",
            base_precio=28.0,
            base_compra=20.0,
            nombres=[
                "Cerveza Lata 355ml",
                "Cerveza Botella 355ml",
                "Cerveza Clara 355ml",
                "Cerveza Oscura 355ml",
            ],
        ),
        ProductTemplate(
            categoria="Botanas",
            unidad="pz",
            base_precio=18.0,
            base_compra=12.0,
            nombres=[
                "Papas Original 45g",
                "Papas Adobadas 45g",
                "Papas Jalapeño 45g",
                "Totopos Nacho 62g",
                "Totopos Picante 62g",
                "Churritos 50g",
                "Palomitas 50g",
                "Cacahuates 50g",
                "Semillas 50g",
            ],
        ),
        ProductTemplate(
            categoria="Galletas",
            unidad="pz",
            base_precio=18.0,
            base_compra=12.5,
            nombres=[
                "Galletas Chocolate 170g",
                "Galletas Vainilla 170g",
                "Galletas Avena 180g",
                "Galletas Saladas 200g",
            ],
        ),
        ProductTemplate(
            categoria="Dulces",
            unidad="pz",
            base_precio=10.0,
            base_compra=6.5,
            nombres=[
                "Pastelito Chocolate",
                "Pastelito Vainilla",
                "Galletas Chocolate",
                "Galletas Vainilla",
                "Paleta Picante",
                "Caramelo Macizo",
                "Chicle Menta",
                "Chocolate Barra 50g",
                "Gomitas 100g",
            ],
        ),
        ProductTemplate(
            categoria="Pan",
            unidad="pz",
            base_precio=45.0,
            base_compra=32.0,
            nombres=[
                "Pan Blanco 680g",
                "Pan Integral 680g",
                "Tortillas Harina 10pzs",
                "Tortillas Maíz 1kg",
            ],
        ),
        ProductTemplate(
            categoria="Lácteos",
            unidad="pz",
            base_precio=28.0,
            base_compra=20.0,
            nombres=[
                "Leche Entera 1L",
                "Leche Deslactosada 1L",
                "Yogurt Natural 1L",
                "Crema 500ml",
                "Queso Panela 400g",
                "Mantequilla 90g",
                "Leche Evaporada 360g",
            ],
        ),
        ProductTemplate(
            categoria="Embutidos",
            unidad="pz",
            base_precio=38.0,
            base_compra=27.0,
            nombres=[
                "Jamón 250g",
                "Salchichas 500g",
                "Chorizo 250g",
            ],
        ),
        ProductTemplate(
            categoria="Abarrotes",
            unidad="pz",
            base_precio=25.0,
            base_compra=18.0,
            nombres=[
                "Arroz 1kg",
                "Frijol Negro 1kg",
                "Azúcar 1kg",
                "Sal 1kg",
                "Aceite 1L",
                "Atún 140g",
                "Sopa Instantánea",
                "Mayonesa 390g",
                "Catsup 397g",
                "Café 200g",
                "Harina 1kg",
                "Pasta 200g",
                "Salsa 370g",
            ],
        ),
        ProductTemplate(
            categoria="Salsas y Condimentos",
            unidad="pz",
            base_precio=22.0,
            base_compra=15.0,
            nombres=[
                "Salsa Picante 150ml",
                "Salsa Tipo Inglesa 145ml",
                "Mostaza 220g",
                "Consomé 8cubos",
                "Chile en Polvo 120g",
            ],
        ),
        ProductTemplate(
            categoria="Enlatados",
            unidad="pz",
            base_precio=24.0,
            base_compra=17.0,
            nombres=[
                "Elote en Grano 220g",
                "Chícharos 220g",
                "Frijoles Refritos 430g",
                "Champiñones 186g",
            ],
        ),
        ProductTemplate(
            categoria="Higiene",
            unidad="pz",
            base_precio=35.0,
            base_compra=26.0,
            nombres=[
                "Papel Higiénico 4 rollos",
                "Pasta Dental 100ml",
                "Jabón de Tocador 150g",
                "Shampoo 400ml",
                "Desodorante 150ml",
                "Toallas Sanitarias 10pzs",
                "Rastrillos 2pzs",
            ],
        ),
        ProductTemplate(
            categoria="Limpieza",
            unidad="pz",
            base_precio=28.0,
            base_compra=20.0,
            nombres=[
                "Cloro 1L",
                "Detergente 1kg",
                "Suavizante 850ml",
                "Desengrasante 500ml",
                "Fibras de Limpieza 3pzs",
                "Jabón en Barra 400g",
                "Limpiador Multiusos 1L",
            ],
        ),
        ProductTemplate(
            categoria="Mascotas",
            unidad="pz",
            base_precio=22.0,
            base_compra=15.0,
            nombres=[
                "Croquetas Perro 1kg",
                "Croquetas Gato 1kg",
                "Sobres Gato 85g",
                "Sobres Perro 100g",
                "Snacks Perro 100g",
                "Snacks Gato 60g",
                "Arena para Gato 5kg",
                "Shampoo Perro 250ml",
            ],
        ),

        ProductTemplate(
            categoria="Básicos Frescos",
            unidad="pz",
            base_precio=28.0,
            base_compra=20.0,
            nombres=[
                "Huevo 12pzs",
                "Huevo 30pzs",
                "Tortillas Maíz 1kg",
                "Tortillas Harina 10pzs",
                "Pan Blanco 680g",
                "Pollo Congelado 1kg",
                "Carne Molida 500g",
                "Manzana 1kg",
                "Plátano 1kg",
                "Jitomate 1kg",
                "Cebolla 1kg",
                "Limón 1kg",
            ],
        ),
    ]

    marcas_por_categoria: Dict[str, List[str]] = {
        "Refrescos": ["Coca-Cola", "Pepsi", "Jarritos", "Fanta", "Sprite", "Manzanita"],
        "Agua": ["Ciel", "Bonafont", "E-Pura", "Peñafiel", "Santa María"],
        "Jugos": ["Del Valle", "Jumex", "Tropicana"],
        "Energéticas": ["Monster", "Red Bull"],
        "Cerveza": ["Tecate", "Corona", "Victoria", "Modelo"],
        "Botanas": ["Sabritas", "Barcel", "Doritos", "Cheetos", "Ruffles"],
        "Galletas": ["Gamesa", "Nabisco", "Cuétara"],
        "Dulces": ["Marinela", "Ricolino", "Vero", "De La Rosa", "Hershey's"],
        "Pan": ["Bimbo", "Tía Rosa"],
        "Lácteos": ["Lala", "Alpura", "Nestlé", "FUD"],
        "Embutidos": ["FUD", "San Rafael", "Zwan"],
        "Abarrotes": ["Herdez", "La Costeña", "Verde Valle", "Kellogg's"],
        "Salsas y Condimentos": ["Valentina", "Maggi", "McCormick", "La Costeña"],
        "Enlatados": ["La Costeña", "Herdez"],
        "Higiene": ["Colgate", "Palmolive", "Rexona", "Pantene", "Pétalo"],
        "Limpieza": ["Cloralex", "Ariel", "Pinol", "Fabuloso", "Roma"],
    "Mascotas": ["Pedigree", "Whiskas", "Purina", "Dog Chow", "Cat Chow", "Felix"],
    "Básicos Frescos": ["Genérico"],
    }

    # Proveedor "oficial" por marca (referencial/educativo)
    proveedor_por_marca: Dict[str, str] = {
        # Bebidas
        "Coca-Cola": "FEMSA (Coca-Cola FEMSA)",
        "Sprite": "FEMSA (Coca-Cola FEMSA)",
        "Fanta": "FEMSA (Coca-Cola FEMSA)",
        "Manzanita": "FEMSA (Coca-Cola FEMSA)",
        "Ciel": "FEMSA (Coca-Cola FEMSA)",
        "Pepsi": "PepsiCo Bebidas",
        "Gatorade": "PepsiCo Bebidas",
        "Jarritos": "Jarritos (Novamex)",
        "Peñafiel": "Peñafiel (Keurig Dr Pepper)",
        "Bonafont": "Danone Waters",
        "E-Pura": "PepsiCo Bebidas",
        "Red Bull": "Red Bull",
        "Monster": "Coca-Cola (Monster distribution)",

        # Botanas / galletas
        "Sabritas": "PepsiCo Alimentos",
        "Doritos": "PepsiCo Alimentos",
        "Cheetos": "PepsiCo Alimentos",
        "Ruffles": "PepsiCo Alimentos",
        "Barcel": "Grupo Bimbo (Barcel)",
        "Gamesa": "PepsiCo Alimentos (Gamesa)",
        "Nabisco": "Mondelez",
        "Cuétara": "Cuétara",

        # Pan / dulces
        "Bimbo": "Grupo Bimbo",
        "Tía Rosa": "Grupo Bimbo",
        "Marinela": "Grupo Bimbo (Marinela)",
        "Ricolino": "Ricolino / Mondelēz (según región)",
        "Vero": "Dulces Vero",
        "De La Rosa": "Dulces De La Rosa",
        "Hershey's": "The Hershey Company",

        # Lácteos / embutidos
        "Lala": "Grupo Lala",
        "Alpura": "Alpura",
        "Nestlé": "Nestlé",
        "FUD": "Sigma Alimentos (FUD)",
        "San Rafael": "Sigma Alimentos (San Rafael)",
        "Zwan": "Sigma Alimentos (Zwan)",

        # Abarrotes / condimentos
        "Herdez": "Grupo Herdez",
        "La Costeña": "La Costeña",
        "Verde Valle": "Verde Valle",
        "Kellogg's": "Kellanova (Kellogg's)",
        "Maggi": "Nestlé (Maggi)",
        "McCormick": "McCormick",
        "Valentina": "Salsa Valentina",

        # Limpieza / higiene
        "Colgate": "Colgate-Palmolive",
        "Palmolive": "Colgate-Palmolive",
        "Rexona": "Unilever",
        "Pantene": "P&G",
        "Pétalo": "Kimberly-Clark",
        "Cloralex": "Cloralex",
        "Ariel": "P&G",
        "Pinol": "AlEn",
        "Fabuloso": "Colgate-Palmolive",
        "Roma": "La Corona",

        # Mascotas
        "Pedigree": "Mars Petcare",
        "Whiskas": "Mars Petcare",
    "Purina": "Nestlé Purina",
    "Dog Chow": "Nestlé Purina",
    "Cat Chow": "Nestlé Purina",
    "Felix": "Nestlé Purina",
    }

    empaques: List[Tuple[str, float]] = [
        ("", 1.00),
        (" (Promoción)", 1.05),
        (" (Familiar)", 1.20),
        (" (Mini)", 0.90),
    ]

    productos: List[Dict] = []
    used_codes = set()
    # Evitar repeticiones por nombre+unidad (lo que el usuario percibe como "duplicado")
    used_name_keys = set()

    seq = 1
    for t in templates:
        marcas = marcas_por_categoria.get(t.categoria, ["Genérico"])

        for base_name in t.nombres:
            for marca in marcas:
                for k in range(size_multiplier):
                    for sufijo, factor in empaques:
                        nombre = f"{marca} {base_name}{sufijo}".strip()

                        proveedor = proveedor_por_marca.get(marca, f"Proveedor oficial {marca}")

                        # Precios con pequeñas variaciones controladas
                        precio = round(t.base_precio * factor + (k * 0.5), 2)
                        compra = round(t.base_compra * factor + (k * 0.35), 2)
                        stock = max(0, base_stock + (k % 10) * 3)

                        codigo = make_internal_ean13(prefix, seq)
                        seq += 1

                        # Evitar repetición por nombre+unidad
                        name_key = (nombre.strip().lower(), t.unidad.strip().lower())
                        if name_key in used_name_keys:
                            continue
                        used_name_keys.add(name_key)

                        # Garantizar unicidad de códigos
                        if codigo in used_codes:
                            continue
                        used_codes.add(codigo)

                        productos.append(
                            {
                                "codigo_barras": codigo,
                                "nombre": nombre,
                                "precio": precio,
                                "stock": stock,
                                "categoria": t.categoria,
                                "proveedor": proveedor,
                                "precio_compra": compra,
                                "unidad": t.unidad,
                            }
                        )

    # Ordenar por categoría y nombre para UX
    productos.sort(key=lambda p: (p["categoria"], p["nombre"]))
    return productos


def validate_catalog(productos: List[Dict]) -> List[str]:
    """Valida el catálogo y regresa una lista de errores (vacía si OK)."""
    errors: List[str] = []

    required = {
        "codigo_barras": str,
        "nombre": str,
        "precio": (int, float),
        "stock": int,
        "categoria": str,
        "proveedor": str,
        "precio_compra": (int, float),
        "unidad": str,
    }

    seen = set()
    for i, p in enumerate(productos):
        for k, t in required.items():
            if k not in p:
                errors.append(f"Item {i}: falta campo '{k}'")
                continue
            if not isinstance(p[k], t):
                errors.append(f"Item {i}: campo '{k}' tipo inválido")

        code = p.get("codigo_barras")
        if isinstance(code, str):
            if not (len(code) in (8, 12, 13, 14) or code.isdigit()):
                # permitimos internos EAN-13, pero dejamos esta info por seguridad
                pass
            if code in seen:
                errors.append(f"Item {i}: codigo_barras duplicado '{code}'")
            seen.add(code)

        if isinstance(p.get("precio"), (int, float)) and p["precio"] <= 0:
            errors.append(f"Item {i}: precio <= 0")
        if isinstance(p.get("precio_compra"), (int, float)) and p["precio_compra"] < 0:
            errors.append(f"Item {i}: precio_compra < 0")
        if isinstance(p.get("stock"), int) and p["stock"] < 0:
            errors.append(f"Item {i}: stock < 0")

    return errors
