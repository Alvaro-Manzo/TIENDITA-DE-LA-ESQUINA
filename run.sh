#!/bin/bash
# Script para ejecutar Tiendita de la Esquina

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Ejecutar aplicación
echo "🏪 Iniciando Tiendita de la Esquina..."
python src/main.py
