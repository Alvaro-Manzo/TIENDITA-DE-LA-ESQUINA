"""Recalibra precios del catálogo a rangos coherentes (MXN) para 2025.

- No toca nombres/categorías/códigos.
- Ajusta `precio` y `precio_compra`.
- Fuerza precio > 0 y compra <= precio.

Reglas:
- Usa rangos por categoría (min/max) y un margen de ganancia típico.
- Aplica un ajuste suave según el nombre (tamaño/keywords) para dar variedad.

Uso:
  python3 -m src.tools.recalibrar_precios_2025

Opcional:
  TIENDITA_MARGIN=0.28  (margen promedio)
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path


RANGES = {
    # Rangos aproximados (ventas al público) para tiendita / 2025; se pueden ajustar.
    "Refrescos": (16.0, 35.0),     # 355ml-2L (muy variable)
    "Agua": (12.0, 30.0),          # 600ml-1.5L
    "Jugos": (18.0, 45.0),
    "Botanas": (15.0, 45.0),
    "Dulces": (6.0, 30.0),
    "Lácteos": (18.0, 90.0),
    "Abarrotes": (10.0, 120.0),
    "Higiene": (12.0, 140.0),
    "Limpieza": (12.0, 170.0),
}


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _keyword_factor(nombre: str) -> float:
    n = nombre.lower()

    # tamaños
    if re.search(r"\b2l\b|\b2 l\b", n):
        return 1.55
    if re.search(r"\b1\.5l\b|\b1\.5 l\b", n):
        return 1.35
    if re.search(r"\b1l\b|\b1 l\b", n):
        return 1.20
    if re.search(r"\b600ml\b|\b600 ml\b", n):
        return 1.00
    if re.search(r"\b355ml\b|lata", n):
        return 0.95

    # packs/tamaño familiar
    if "familiar" in n:
        return 1.25
    if "mini" in n:
        return 0.90
    if "promoción" in n or "promocion" in n:
        return 1.05

    # higiene/limpieza: presentaciones más caras
    if re.search(r"1kg|1 kg|\b850ml\b|\b850 ml\b", n):
        return 1.15

    return 1.00


def _stable_hash01(s: str) -> float:
    # hash estable y reproducible (0..1)
    h = 2166136261
    for ch in s.encode("utf-8", "ignore"):
        h ^= ch
        h = (h * 16777619) & 0xFFFFFFFF
    return (h % 10000) / 10000.0


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    productos_path = repo_root / "src" / "data" / "productos.json"

    productos = json.loads(productos_path.read_text(encoding="utf-8"))

    margin = float(os.environ.get("TIENDITA_MARGIN", "0.30"))  # 30% promedio
    margin = _clamp(margin, 0.05, 0.60)

    updated = 0
    for p in productos:
        cat = p.get("categoria", "")
        nombre = str(p.get("nombre", ""))

        lo, hi = RANGES.get(cat, (10.0, 120.0))

        # base dentro del rango usando hash del nombre para que sea "estable" y variado
        r = _stable_hash01(nombre)
        base = lo + (hi - lo) * r

        factor = _keyword_factor(nombre)
        precio = _clamp(base * factor, lo, hi)

        # precio_compra con margen; compra nunca debe ser mayor que venta
        compra = precio / (1.0 + margin)

        # redondeo comercial
        precio = round(precio, 2)
        compra = round(compra, 2)

        if precio <= 0:
            precio = round(lo, 2)
        if compra < 0:
            compra = 0.0
        if compra > precio:
            compra = round(precio * 0.9, 2)

        p["precio"] = precio
        p["precio_compra"] = compra
        updated += 1

    productos_path.write_text(json.dumps(productos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: recalibrados {updated} productos (margin={margin:.2f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
