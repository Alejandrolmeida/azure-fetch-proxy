#!/bin/bash

# Azure FastAPI Fetch Proxy - Script de inicio para Conda
# Uso: ./start_conda.sh

echo "🚀 Azure FastAPI Fetch Proxy - Enhanced Version (Conda)"
echo "======================================================="
echo

# Verificar si conda está disponible
if ! command -v conda &> /dev/null; then
    echo "❌ Error: Conda no está disponible. Usa ./start.sh para pip/venv."
    exit 1
fi

# Verificar si el entorno existe
if ! conda env list | grep -q "proxy"; then
    echo "❌ Entorno 'proxy' no encontrado."
    echo "Ejecuta primero: ./setup_conda.sh"
    exit 1
fi

echo "🐍 Activando entorno conda: proxy"
# Nota: No podemos activar conda en un script bash de forma tradicional
# El usuario debe activar manualmente o usar conda run

echo "📦 Verificando dependencias..."
conda run -n proxy python -c "
import fastapi, httpx, uvicorn, pytest, loguru, cachetools, prometheus_client
print('✅ Todas las dependencias están instaladas')
"

if [ $? -ne 0 ]; then
    echo "❌ Error en las dependencias. Ejecuta: ./setup_conda.sh"
    exit 1
fi

echo
echo "🧪 Ejecutando tests..."
conda run -n proxy pytest tests/ -v

echo
echo "🔧 Opciones de configuración:"
echo "- API_KEY: Configura para requerir autenticación con clave API"
echo "- ALLOWED_HOSTS: Lista de hosts permitidos separados por comas" 
echo "- BLOCKED_HOSTS: Lista de hosts bloqueados separados por comas"
echo

echo "🌟 Funcionalidades implementadas:"
echo "✅ 1. Autenticación con clave API via header x-api-key"
echo "✅ 2. Soporte para métodos HEAD/POST via parámetro 'method'"
echo "✅ 3. Cache LRU en memoria (128 elementos, 120s TTL) con headers X-Cache"
echo "✅ 4. Reenvío de headers selectivo con protección safelist"
echo "✅ 5. Soporte para allowlist/blocklist de hosts"
echo "✅ 6. Protección SSRF mejorada para IPv6"
echo "✅ 7. Mejores heurísticas AMP (soporte ?output=amp)"
echo "✅ 8. Auto Content-Disposition para PDFs e imágenes"
echo "✅ 9. Logging estructurado con loguru + métricas Prometheus"
echo "✅ 10. Suite de pruebas completa con pytest"
echo

echo "📊 Endpoints disponibles:"
echo "- GET /          - Documentación y ejemplos de uso"
echo "- GET /healthz   - Verificación de salud"
echo "- GET /metrics   - Métricas de Prometheus"
echo "- GET /robots.txt - Robots.txt"
echo "- GET|HEAD|POST /fetch - Endpoint principal del proxy"
echo

echo "🔗 Ejemplos de uso:"
echo "# Fetch básico"
echo "curl 'http://localhost:8000/fetch?url=https://httpbin.org/get'"
echo
echo "# Con clave API (si la variable API_KEY está configurada)"
echo "curl -H 'x-api-key: tu-clave' 'http://localhost:8000/fetch?url=https://httpbin.org/get'"
echo
echo "# Método POST con cuerpo"
echo "curl -X POST 'http://localhost:8000/fetch?url=https://httpbin.org/post&method=POST' -d 'datos de prueba'"
echo
echo "# User agent móvil"
echo "curl 'http://localhost:8000/fetch?url=https://httpbin.org/get&ua=mobile'"
echo

echo "🚀 Iniciando servidor con conda..."
echo "Usa Ctrl+C para detener"
echo

# Iniciar el servidor usando conda run
conda run -n proxy uvicorn main:app --host 0.0.0.0 --port 8000 --reload
