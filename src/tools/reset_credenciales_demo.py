"""Resetea credenciales demo (OWNER/ADMIN/CAJERO) a valores conocidos.

Solicitado para evitar errores de login tras ediciones manuales de usuarios.json.

Acción:
- Actualiza password_hash de los usuarios existentes si coinciden por username.
- NO crea backups automáticamente.

Credenciales resultantes:
- owner / owner123
- admin / admin123
- cajero / cajero123

Uso:
  python3 -m src.tools.reset_credenciales_demo
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def _hash(p: str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    path = repo_root / "src" / "data" / "usuarios.json"

    users = json.loads(path.read_text(encoding="utf-8"))

    desired = {
        "owner": "owner123",
        "admin": "admin123",
        "cajero": "cajero123",
    }

    touched = 0
    for u in users:
        username = str(u.get("username", ""))
        if username in desired:
            u["password_hash"] = _hash(desired[username])
            touched += 1

    if touched == 0:
        print("No se actualizó ningún usuario (usernames no encontrados).")
        return 1

    path.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK: credenciales demo reseteadas:")
    print("- owner / owner123")
    print("- admin / admin123")
    print("- cajero / cajero123")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
