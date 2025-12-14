"""Genera y escribe un inventario 'pro' en src/data/productos.json.

Reglas:
- NO hace backups (por solicitud explícita).
- Valida catálogo antes de escribir.

Uso:
- Ejecutar como módulo o script.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from src.services.catalog_generator import generate_catalog, validate_catalog


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    out_path = repo_root / "src" / "data" / "productos.json"

    # Valores por defecto: catálogo MUY surtido.
    # Nota: por diseño se deduplica por nombre+unidad para evitar "20 repeticiones".
    size_multiplier = int(os.environ.get("TIENDITA_SIZE_MULTIPLIER", "50"))
    base_stock = int(os.environ.get("TIENDITA_BASE_STOCK", "60"))

    productos = generate_catalog(size_multiplier=size_multiplier, base_stock=base_stock)
    errors = validate_catalog(productos)

    if errors:
        print("VALIDACIÓN FALLÓ. No se escribió productos.json")
        for e in errors[:50]:
            print("-", e)
        if len(errors) > 50:
            print(f"... y {len(errors) - 50} errores más")
        return 1

    out_path.write_text(json.dumps(productos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: escrito {out_path} con {len(productos)} productos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
