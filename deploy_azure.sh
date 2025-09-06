#!/bin/bash

# 🚀 GUÍA COMPLETA DE DESPLIEGUE EN AZURE
# =====================================

echo "🌐 Azure FastAPI Fetch Proxy - Deployment Guide"
echo "==============================================="
echo

# Variables que necesitas configurar
APP_NAME="your-unique-app-name"  # CAMBIAR: Debe ser único en Azure
RESOURCE_GROUP="rg-fetch-proxy"
LOCATION="westeurope"
SUBSCRIPTION_ID=""  # OPCIONAL: Tu subscription ID si tienes varias

echo "📋 PASO 1: Configuración inicial"
echo "================================"
echo
echo "1.1. Edita este archivo (deploy_azure.sh) y cambia:"
echo "     - APP_NAME='tu-nombre-unico-aqui'"
echo "     - SUBSCRIPTION_ID='tu-subscription' (si tienes varias)"
echo
echo "1.2. Configura tu API key:"
echo "     - Edita el archivo .env"
echo "     - Cambia 'your-secure-api-key-here' por tu clave real"
echo
echo "1.3. Login en Azure (si no lo has hecho):"
echo "     az login"
echo
read -p "¿Has completado los pasos 1.1, 1.2 y 1.3? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Completa los pasos anteriores antes de continuar"
    exit 1
fi

echo
echo "📋 PASO 2: Crear recursos en Azure"
echo "=================================="
echo

# Verificar login
echo "🔐 Verificando login en Azure..."
if ! az account show &>/dev/null; then
    echo "❌ No estás logueado en Azure. Ejecuta: az login"
    exit 1
fi

# Configurar suscripción si se especifica
if [ -n "$SUBSCRIPTION_ID" ]; then
    echo "🎯 Configurando suscripción: $SUBSCRIPTION_ID"
    az account set --subscription "$SUBSCRIPTION_ID"
fi

echo "✅ Azure CLI configurado correctamente"
echo

# Crear grupo de recursos
echo "📁 Creando grupo de recursos: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION

# Crear plan de App Service
echo "📊 Creando plan de App Service..."
az appservice plan create \
    --name "asp-$APP_NAME" \
    --resource-group $RESOURCE_GROUP \
    --sku B1 \
    --is-linux

# Crear Web App
echo "🌐 Creando Web App: $APP_NAME"
az webapp create \
    --resource-group $RESOURCE_GROUP \
    --plan "asp-$APP_NAME" \
    --name $APP_NAME \
    --runtime "PYTHON:3.11"

echo
echo "📋 PASO 3: Configurar la aplicación"
echo "==================================="
echo

# Configurar comando de inicio
echo "⚙️ Configurando comando de inicio..."
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --startup-file "gunicorn -k uvicorn.workers.UvicornWorker -w 2 -t 120 main:app"

# Configurar variables de entorno desde .env
echo "🔧 Configurando variables de entorno..."

# Leer API_KEY del archivo .env
if [ -f .env ]; then
    API_KEY=$(grep "^API_KEY=" .env | cut -d'=' -f2-)
    if [ -n "$API_KEY" ] && [ "$API_KEY" != "your-secure-api-key-here" ]; then
        echo "✅ Configurando API_KEY..."
        az webapp config appsettings set \
            --resource-group $RESOURCE_GROUP \
            --name $APP_NAME \
            --settings API_KEY="$API_KEY"
    else
        echo "❌ ERROR: API_KEY no configurada en .env"
        echo "   Edita .env y cambia 'your-secure-api-key-here' por tu clave real"
        exit 1
    fi
else
    echo "❌ ERROR: Archivo .env no encontrado"
    echo "   Ejecuta: cp .env.azure .env"
    echo "   Luego edita .env con tu API key"
    exit 1
fi

# Configurar otras variables optimizadas para ChatGPT
echo "🤖 Configurando optimizaciones para ChatGPT..."
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --settings \
        MAX_REQUESTS_PER_MINUTE=100 \
        MAX_REQUESTS_PER_HOUR=2000 \
        MAX_RESPONSE_SIZE_MB=15 \
        CUSTOM_USER_AGENT="ChatGPT-Proxy-Service/1.0"

echo
echo "📋 PASO 4: Desplegar código"
echo "=========================="
echo

# Crear archivo ZIP con el código
echo "📦 Empaquetando aplicación..."
zip -r deploy.zip . -x "*.git*" "*__pycache__*" "*.venv*" ".env" "deploy_azure.sh" "deploy.zip"

# Desplegar
echo "🚀 Desplegando aplicación..."
az webapp deployment source config-zip \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --src deploy.zip

# Limpiar
rm deploy.zip

echo
echo "📋 PASO 5: Verificación"
echo "======================"
echo

# Esperar un momento para que se inicie
echo "⏳ Esperando que la aplicación se inicie..."
sleep 30

# URLs de la aplicación
BASE_URL="https://$APP_NAME.azurewebsites.net"

echo "✅ ¡Despliegue completado!"
echo
echo "🔗 URLs de tu proxy:"
echo "   🏠 Página principal: $BASE_URL"
echo "   ❤️  Health check:    $BASE_URL/healthz"
echo "   🔒 Security info:    $BASE_URL/security-info?api_key=$API_KEY"
echo "   🎯 Proxy endpoint:   $BASE_URL/fetch?url=TARGET_URL&api_key=$API_KEY"
echo

echo "🤖 Ejemplo para ChatGPT:"
echo "----------------------------------------"
echo "Analyze this GitHub repository data:"
echo "$BASE_URL/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=$API_KEY"
echo

echo "🧪 Pruebas rápidas:"
echo "curl $BASE_URL/healthz"
echo "curl '$BASE_URL/fetch?url=https://httpbin.org/json&api_key=$API_KEY'"
echo

echo "🎉 ¡Tu proxy está listo para usar con ChatGPT!"
echo "   💡 Guarda estas URLs en un lugar seguro"
echo "   🔒 Nunca compartas tu API key públicamente"
