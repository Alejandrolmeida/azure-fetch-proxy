#!/bin/bash

# Script de configuración para Azure FastAPI Fetch Proxy con Miniconda
# Uso: chmod +x setup_conda.sh && ./setup_conda.sh

echo "🐍 Configurando entorno Miniconda para Azure FastAPI Fetch Proxy"
echo "=================================================================="

# Verificar si conda está instalado
if ! command -v conda &> /dev/null; then
    echo "❌ Error: Conda no está instalado."
    echo "Por favor instala Miniconda desde: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✅ Conda encontrado: $(conda --version)"

# Crear el entorno desde environment.yml
echo "📦 Creando entorno conda 'proxy'..."
conda env create -f environment.yml

if [ $? -eq 0 ]; then
    echo "✅ Entorno creado exitosamente"
else
    echo "❌ Error al crear el entorno"
    exit 1
fi

echo ""
echo "🎯 Configuración completada. Para usar el entorno:"
echo ""
echo "# Activar el entorno:"
echo "conda activate proxy"
echo ""
echo "# Ejecutar tests:"
echo "pytest tests/ -v"
echo ""
echo "# Iniciar el servidor:"
echo "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "# Desactivar el entorno cuando termines:"
echo "conda deactivate"
echo ""
echo "# Para eliminar el entorno (si es necesario):"
echo "conda env remove -n proxy"
echo ""
echo "🚀 ¡Listo para desarrollar!"
