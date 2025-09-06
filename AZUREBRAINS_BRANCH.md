# 🌿 Rama AzureBrains - Personalización del Proxy

Esta rama contiene la **personalización completa** del Azure FastAPI Fetch Proxy para el dominio **proxy.azurebrains.com**.

## 🎯 ¿Por qué una rama separada?

- **Rama `main`**: Código genérico y reutilizable para cualquier usuario
- **Rama `azurebrains`**: Personalización específica con branding y dominio personalizado

## 🔄 Diferencias con la rama main

### 📝 Archivos Modificados:
- **`README.md`**: Título actualizado a "AzureBrains Fetch Proxy", ejemplos con proxy.azurebrains.com
- **`.env.example`**: User-Agent personalizado y variable CUSTOM_DOMAIN
- **`deploy_container.sh`**: Instrucciones para configuración de dominio personalizado
- **`requests.http`**: Ejemplos listos para proxy.azurebrains.com

### 📁 Archivos Nuevos:
- **`CUSTOM_DOMAIN_SETUP.md`**: Guía completa para configurar dominio personalizado
- **`AZUREBRAINS_BRANCH.md`**: Este archivo (documentación de la rama)

## 🚀 Uso de esta Rama

### 1. Clonar la rama específica:
```bash
git clone -b azurebrains https://github.com/Alejandrolmeida/azure-fetch-proxy.git
cd azure-fetch-proxy
```

### 2. O cambiar a esta rama:
```bash
git checkout azurebrains
```

### 3. Desplegar con configuración personalizada:
```bash
# Configurar entorno
cp .env.example .env
# Editar .env con tu API key

# Desplegar
chmod +x deploy_container.sh
./deploy_container.sh
```

### 4. Configurar dominio personalizado:
- Seguir instrucciones en `CUSTOM_DOMAIN_SETUP.md`
- Configurar DNS para proxy.azurebrains.com
- Opcional: Configurar Azure Front Door para HTTPS

## 🔄 Mantener Sincronizado

Para mantener esta rama actualizada con los cambios de la rama main:

```bash
# Cambiar a main y actualizar
git checkout main
git pull origin main

# Cambiar a azurebrains y merge cambios
git checkout azurebrains
git merge main

# Resolver conflictos si es necesario y push
git push origin azurebrains
```

## 🎯 URLs Finales

- **Desarrollo**: `http://localhost:8000`
- **Producción**: `https://proxy.azurebrains.com`
- **ChatGPT**: `https://proxy.azurebrains.com/fetch?url=TARGET&api_key=YOUR_KEY`

## 📊 Características Específicas

### 🏷️ Branding Personalizado:
- Título: "AzureBrains Fetch Proxy"
- User-Agent: "AzureBrains-Proxy-Service/1.0"
- Badge personalizado en README
- Enlaces a proxy.azurebrains.com

### 🌐 Dominio Personalizado:
- Configuración DNS automatizada
- Guías para HTTPS con Azure Front Door
- Ejemplos listos para producción
- Scripts de verificación

### 🎯 Optimizado para ChatGPT:
- URLs de ejemplo con el dominio personalizado
- Prompts listos para usar
- Configuración de seguridad optimizada

## 💡 Ventajas de este Enfoque

1. **Separación Clara**: Código genérico vs personalizado
2. **Contribuciones Limpias**: Los PR van a main sin personalización
3. **Mantenimiento**: Fácil merge de actualizaciones desde main
4. **Profesional**: Tu marca sin afectar el proyecto base
5. **Flexibilidad**: Otros usuarios pueden crear sus propias ramas personalizadas

## 🤝 Contribuciones

Para contribuir al proyecto base:
1. Hacer cambios en la rama `main`
2. Crear PR hacia `main`
3. Después hacer merge a `azurebrains` si es necesario

Para cambios específicos de AzureBrains:
1. Trabajar directamente en la rama `azurebrains`
2. No hacer PR de estos cambios a `main`

---

**🚀 Esta rama está lista para desplegar tu proxy personalizado en proxy.azurebrains.com**
