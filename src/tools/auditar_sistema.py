"""Auditoría rápida del sistema (sin GUI).

Objetivo:
- Detectar errores comunes por ediciones manuales en JSON.
- Validar roles (OWNER/ADMIN/CAJERO).
- Validar que no haya productos duplicados por nombre+unidad.

No modifica ningún archivo.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    usuarios_path = repo_root / "src" / "data" / "usuarios.json"
    productos_path = repo_root / "src" / "data" / "productos.json"

    try:
        usuarios = _load_json(usuarios_path)
    except Exception as e:
        print(f"ERROR: usuarios.json inválido: {e}")
        return 1

    roles = sorted({u.get("rol") for u in usuarios})
    print("roles_encontrados:", roles)
    expected = {"OWNER", "ADMIN", "CAJERO"}
    missing = sorted(expected - set(roles))
    if missing:
        print("ERROR: faltan roles:", missing)
        return 1

    try:
        productos = _load_json(productos_path)
    except Exception as e:
        print(f"ERROR: productos.json inválido: {e}")
        return 1

    def key(p):
        return (str(p.get("nombre", "")).strip().lower(), str(p.get("unidad", "")).strip().lower())

    c = Counter(key(p) for p in productos)
    dupes = [(k, v) for k, v in c.items() if v > 1]
    dupes.sort(key=lambda t: t[1], reverse=True)

    print("productos_total:", len(productos))
    print("duplicados_nombre_unidad:", len(dupes))
    if dupes:
        print("ejemplos_duplicados_top5:")
        for k, v in dupes[:5]:
            print("-", k, "x", v)
        return 1

    print("OK auditoría")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
