# 🤖 Uso del Proxy con ChatGPT

## 📋 Configuración Optimizada para ChatGPT

El proxy está configurado específicamente para trabajar con ChatGPT:

- **✅ Todos los dominios permitidos** (excepto redes privadas/locales)
- **🚀 Rate limiting aumentado**: 100 req/min, 2000 req/hora
- **📦 Respuestas más grandes**: Hasta 15MB
- **🔐 Autenticación por API Key**: `AESAPIPAUAS0000LFKSE275FTQO1DA`

## 🔗 Cómo Usar con ChatGPT

### Formato de URL para ChatGPT:
```
http://localhost:8003/fetch?url=<URL_DESTINO>&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA
```

### Ejemplos Prácticos:

#### 1. **Analizar una página de noticias:**
```
Analiza este artículo: http://localhost:8003/fetch?url=https://www.bbc.com/news/technology&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA
```

#### 2. **Obtener datos de una API:**
```
Revisa esta API: http://localhost:8003/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA
```

#### 3. **Analizar documentación técnica:**
```
Lee esta documentación: http://localhost:8003/fetch?url=https://docs.python.org/3/library/requests.html&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA
```

#### 4. **Examinar contenido académico:**
```
Analiza este paper: http://localhost:8003/fetch?url=https://arxiv.org/abs/2103.00020&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA
```

#### 5. **Análisis de sitios web:**
```
Examina este sitio: http://localhost:8003/fetch?url=https://www.python.org&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA
```

## 🎯 Casos de Uso Específicos

### **Para Investigación:**
- Análisis de artículos científicos
- Revisión de documentación técnica
- Comparación de fuentes múltiples

### **Para Desarrollo:**
- Análisis de APIs públicas
- Revisión de código en GitHub
- Análisis de logs o datos

### **Para Negocios:**
- Análisis de competencia
- Investigación de mercado
- Revisión de tendencias

## 🔐 Seguridad

- **API Key obligatoria** para todas las solicitudes
- **Rate limiting** para prevenir abuso
- **Hosts bloqueados**: localhost, redes privadas, servicios de metadata
- **Límite de tamaño** de respuesta: 15MB

## 📊 Monitoreo

- **Estado del servicio**: http://localhost:8003/healthz
- **Info de seguridad**: http://localhost:8003/security-info?api_key=AESAPIPAUAS0000LFKSE275FTQO1DA

## 🚀 Para Desplegar en Azure

1. Usa el script `./start_azure.sh`
2. Configura las variables en `.env.azure`
3. El proxy estará disponible en tu dominio de Azure

## 💡 Consejos para ChatGPT

1. **Siempre incluye la API key** en la URL
2. **Describe qué quieres analizar** antes de pasar la URL
3. **Especifica el tipo de análisis** que necesitas
4. **Usa URLs completas** (con https://)

### Ejemplo de Prompt Completo:
```
"Analiza el contenido técnico de esta página y resume los puntos clave sobre Python async/await: 
http://localhost:8003/fetch?url=https://realpython.com/async-io-python/&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA"
```
