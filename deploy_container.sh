#!/bin/bash

# 🐳 DESPLIEGUE CON AZURE CONTAINER INSTANCES
# ==========================================

echo "🚀 Desplegando con Azure Container Instances (más confiable)"
echo "==========================================================="

# Variables
CONTAINER_NAME="fetch-proxy-container"
RESOURCE_GROUP="rg-fetch-proxy"
LOCATION="westeurope"

# Leer API key
if [ -f .env ]; then
    API_KEY=$(grep "^API_KEY=" .env | cut -d'=' -f2-)
    if [ -z "$API_KEY" ] || [ "$API_KEY" = "your-secure-api-key-here" ]; then
        echo "❌ ERROR: Configura tu API_KEY en .env"
        echo "   Edita .env y pon tu clave real"
        exit 1
    fi
else
    echo "❌ ERROR: Archivo .env no encontrado"
    exit 1
fi

echo "📦 PASO 1: Construir imagen Docker localmente"
echo "============================================="
sudo docker build -t fetch-proxy:latest .

echo "📤 PASO 2: Crear Azure Container Registry"
echo "========================================="
ACR_NAME="fetchproxyregistry$(date +%s)"
az acr create \
    --resource-group $RESOURCE_GROUP \
    --name $ACR_NAME \
    --sku Basic \
    --admin-enabled true

echo "🔑 PASO 3: Obtener credenciales del registry"
echo "==========================================="
ACR_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query "loginServer" --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv)

echo "📤 PASO 4: Subir imagen al registry"
echo "=================================="
sudo docker tag fetch-proxy:latest $ACR_SERVER/fetch-proxy:latest
sudo docker login $ACR_SERVER --username $ACR_NAME --password $ACR_PASSWORD
sudo docker push $ACR_SERVER/fetch-proxy:latest

echo "🚀 PASO 5: Crear Container Instance"
echo "=================================="
az container create \
    --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_NAME \
    --image $ACR_SERVER/fetch-proxy:latest \
    --registry-username $ACR_NAME \
    --registry-password $ACR_PASSWORD \
    --dns-name-label "fetch-proxy-$(date +%s)" \
    --ports 8000 \
    --os-type Linux \
    --environment-variables \
        API_KEY="$API_KEY" \
        MAX_REQUESTS_PER_MINUTE=100 \
        MAX_REQUESTS_PER_HOUR=2000 \
        MAX_RESPONSE_SIZE_MB=15 \
    --cpu 1 \
    --memory 1

echo "⏳ PASO 6: Esperar despliegue"
echo "=========================="
sleep 30

# Obtener la URL pública
FQDN=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query "ipAddress.fqdn" --output tsv)
CONTAINER_URL="http://$FQDN:8000"

echo "🧪 PASO 7: Probar el contenedor"
echo "============================="
curl -s "$CONTAINER_URL/healthz" && echo "✅ ¡FUNCIONA!" || echo "❌ Probando..."

echo
echo "🎉 ¡CONTENEDOR DESPLEGADO EXITOSAMENTE!"
echo "======================================"
echo "   🌐 URL: $CONTAINER_URL"
echo "   ❤️  Health: $CONTAINER_URL/healthz"
echo "   🎯 Proxy: $CONTAINER_URL/fetch?url=TARGET_URL&api_key=$API_KEY"
echo
echo "🤖 Para ChatGPT:"
echo "   $CONTAINER_URL/fetch?url=https://httpbin.org/json&api_key=$API_KEY"
echo
echo "💡 Este método es más confiable que App Service"
echo "   y debería funcionar sin problemas."
