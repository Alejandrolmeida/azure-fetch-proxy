# 🌐 Configuración de Dominio Personalizado - proxy.azurebrains.com

Esta guía te ayudará a configurar tu dominio personalizado `proxy.azurebrains.com` para el AzureBrains Fetch Proxy.

## 📋 Requisitos Previos

1. Tener el contenedor desplegado en Azure Container Instances
2. Acceso a la configuración DNS de azurebrains.com
3. (Opcional) Azure Front Door para HTTPS y mejor rendimiento

## 🔧 Opción 1: Configuración DNS Básica

### Paso 1: Obtener la URL del Contenedor
Después de ejecutar `./deploy_container.sh`, obtendrás una URL como:
```
http://fetch-proxy-1234567890.westeurope.azurecontainer.io:8000
```

### Paso 2: Configurar CNAME
En tu proveedor de DNS, añade un registro CNAME:
```
Tipo: CNAME
Nombre: proxy
Valor: fetch-proxy-1234567890.westeurope.azurecontainer.io
TTL: 300
```

### Paso 3: Verificar
Después de la propagación DNS (5-30 minutos):
```bash
# Verificar resolución DNS
nslookup proxy.azurebrains.com

# Probar el proxy
curl "http://proxy.azurebrains.com:8000/healthz"
```

⚠️ **Limitación**: Esta configuración solo soporta HTTP en el puerto 8000.

## 🚀 Opción 2: Azure Front Door (Recomendado)

Azure Front Door proporciona:
- ✅ HTTPS automático
- ✅ Dominio personalizado sin puerto
- ✅ CDN global
- ✅ WAF (Web Application Firewall)

### Paso 1: Crear Azure Front Door
```bash
# Variables
FRONT_DOOR_NAME="azurebrains-proxy-fd"
RESOURCE_GROUP="rg-fetch-proxy"
CONTAINER_FQDN="fetch-proxy-1234567890.westeurope.azurecontainer.io"

# Crear Front Door
az network front-door create \
    --resource-group $RESOURCE_GROUP \
    --name $FRONT_DOOR_NAME \
    --backend-address $CONTAINER_FQDN \
    --backend-host-header $CONTAINER_FQDN \
    --protocol Http \
    --backend-port 8000
```

### Paso 2: Configurar Dominio Personalizado
```bash
# Añadir dominio personalizado
az network front-door frontend-endpoint create \
    --resource-group $RESOURCE_GROUP \
    --front-door-name $FRONT_DOOR_NAME \
    --name proxy-azurebrains \
    --host-name proxy.azurebrains.com
```

### Paso 3: Configurar DNS
En tu proveedor de DNS:
```
Tipo: CNAME
Nombre: proxy
Valor: azurebrains-proxy-fd.azurefd.net
TTL: 300
```

### Paso 4: Habilitar HTTPS
```bash
# Habilitar HTTPS con certificado administrado por Azure
az network front-door frontend-endpoint enable-https \
    --resource-group $RESOURCE_GROUP \
    --front-door-name $FRONT_DOOR_NAME \
    --name proxy-azurebrains \
    --certificate-source FrontDoor
```

## 🛡️ Opción 3: Azure Application Gateway

Para máximo control y características empresariales:

### Beneficios
- ✅ SSL/TLS termination
- ✅ WAF integrado
- ✅ Load balancing
- ✅ Autoscaling
- ✅ Health probes

### Configuración Básica
```bash
# Crear subnet para Application Gateway
az network vnet subnet create \
    --resource-group $RESOURCE_GROUP \
    --vnet-name proxy-vnet \
    --name appgw-subnet \
    --address-prefixes 10.0.1.0/24

# Crear IP pública
az network public-ip create \
    --resource-group $RESOURCE_GROUP \
    --name appgw-public-ip \
    --sku Standard

# Crear Application Gateway
az network application-gateway create \
    --resource-group $RESOURCE_GROUP \
    --name proxy-appgw \
    --location westeurope \
    --vnet-name proxy-vnet \
    --subnet appgw-subnet \
    --public-ip-address appgw-public-ip \
    --servers $CONTAINER_FQDN:8000
```

## 🧪 Verificación Final

Una vez configurado cualquier opción:

### Test de Conectividad
```bash
# Health check
curl "https://proxy.azurebrains.com/healthz"

# Test del proxy
curl "https://proxy.azurebrains.com/fetch?url=https://httpbin.org/json&api_key=YOUR_API_KEY"

# Información de seguridad
curl "https://proxy.azurebrains.com/security-info?api_key=YOUR_API_KEY"
```

### Test con ChatGPT
```
Analiza este repositorio de GitHub y proporciona un resumen:
https://proxy.azurebrains.com/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=YOUR_API_KEY
```

## 📊 Monitoreo

### Métricas Disponibles
- `https://proxy.azurebrains.com/metrics` - Métricas de Prometheus
- `https://proxy.azurebrains.com/healthz` - Estado del servicio
- `https://proxy.azurebrains.com/security-info` - Configuración actual

### Azure Monitor
Configura alertas para:
- Disponibilidad del servicio
- Tiempo de respuesta
- Límites de velocidad alcanzados
- Errores de autenticación

## 🔧 Troubleshooting

### DNS no se resuelve
```bash
# Verificar propagación DNS
dig proxy.azurebrains.com
nslookup proxy.azurebrains.com

# Verificar desde diferentes ubicaciones
# Usar herramientas online como dnschecker.org
```

### HTTPS no funciona
1. Verificar que el certificado esté válido
2. Comprobar la configuración de Front Door/Application Gateway
3. Asegurar que el backend está respondiendo correctamente

### Rendimiento lento
1. Verificar la ubicación del Container Instance
2. Considerar usar múltiples regiones
3. Optimizar la configuración de Front Door

## 💡 Mejores Prácticas

### Seguridad
- ✅ Usar HTTPS siempre en producción
- ✅ Configurar WAF con reglas restrictivas
- ✅ Rotar API keys regularmente
- ✅ Monitorear logs de acceso

### Rendimiento
- ✅ Usar CDN (Front Door) para contenido estático
- ✅ Configurar health probes apropiados
- ✅ Implementar auto-scaling si es necesario

### Costos
- ✅ Monitorear uso de Azure Front Door
- ✅ Optimizar Container Instance resources
- ✅ Usar reserved instances para reducir costos

---

## 🎉 ¡Tu Proxy ya está listo en proxy.azurebrains.com!

Una vez configurado, tu proxy estará disponible en:
**https://proxy.azurebrains.com**

Con todas las características profesionales:
- 🔐 Autenticación segura
- 🚀 Alto rendimiento
- 📊 Monitoreo completo
- 🛡️ Protección WAF
- 🌐 CDN global
