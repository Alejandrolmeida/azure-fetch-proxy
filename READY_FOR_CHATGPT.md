# 🎯 **GUÍA PRÁCTICA: Proxy para ChatGPT**

## ✅ **Estado Actual - TODO FUNCIONANDO**

🔗 **URL Base del Proxy:** `http://localhost:8003/fetch`
🔑 **API Key:** `AESAPIPAUAS0000LFKSE275FTQO1DA`

---

## 🚀 **Ejemplos Listos para Usar con ChatGPT**

### **📰 Análisis de Noticias**
```
Analiza las principales noticias de tecnología en esta página:
http://localhost:8003/fetch?url=https://httpbin.org/html&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA
```

### **📊 APIs y Datos**
```
Analiza la información del repositorio de VS Code:
http://localhost:8003/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA
```

### **🔍 Investigación Web**
```
Examina el contenido de este sitio web:
http://localhost:8003/fetch?url=https://www.python.org&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA
```

---

## 💬 **Prompts Efectivos para ChatGPT**

### **🎯 Prompt Completo de Ejemplo:**
```
"Analiza el contenido técnico de la API de GitHub del repositorio de VS Code y dame un resumen de:
1. Información general del proyecto
2. Estadísticas importantes (estrellas, forks, issues)
3. Tecnologías utilizadas
4. Estado actual del proyecto

URL: http://localhost:8003/fetch?url=https://api.github.com/repos/microsoft/vscode&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA"
```

### **📝 Estructura de Prompt Recomendada:**
1. **Instrucción clara** de lo que quieres analizar
2. **Contexto específico** del tipo de análisis
3. **URL del proxy** con api_key incluida
4. **Formato de respuesta** deseado (opcional)

---

## 🔧 **Configuración Actual**

✅ **Rate Limiting:** 100 solicitudes/minuto, 2000 solicitudes/hora
✅ **Tamaño máximo:** 15MB por respuesta  
✅ **Autenticación:** API Key requerida
✅ **Dominios:** Todos permitidos (excepto redes privadas)
✅ **User Agent:** `ChatGPT-Proxy-Service/1.0`

---

## 📋 **Checklist Pre-uso**

- [x] Servidor corriendo en puerto 8003
- [x] API Key configurada: `AESAPIPAUAS0000LFKSE275FTQO1DA`
- [x] Rate limiting activo
- [x] Seguridad SSRF activada
- [x] Soporte para query parameters
- [x] Decompresión de contenido funcionando

---

## 🎯 **Casos de Uso Ideales**

### **🔬 Investigación Académica**
- Papers de arXiv
- Documentación técnica
- Artículos científicos

### **💼 Análisis de Negocio**
- APIs públicas
- Datos de mercado
- Información de competencia

### **🛠️ Desarrollo**
- Repositorios de GitHub
- Documentación de librerías
- APIs REST

### **📚 Educación**
- Tutoriales
- Ejemplos de código
- Recursos educativos

---

## 🌐 **Para Usar en Azure (Cuando Despliegues)**

Simplemente reemplaza `localhost:8003` por tu dominio de Azure:
```
https://tu-app.azurewebsites.net/fetch?url=https://ejemplo.com&api_key=AESAPIPAUAS0000LFKSE275FTQO1DA
```

---

## 🔍 **Verificaciones Rápidas**

### **Estado del Servicio:**
```bash
curl http://localhost:8003/healthz
```

### **Información de Seguridad:**
```bash
curl "http://localhost:8003/security-info?api_key=AESAPIPAUAS0000LFKSE275FTQO1DA"
```

---

## 💡 **Consejos Pro**

1. **🎯 Sé específico:** Dile a ChatGPT exactamente qué quieres analizar
2. **📝 Contextualiza:** Explica el tipo de contenido antes de dar la URL
3. **🔄 Itera:** Puedes pedirle que analice múltiples URLs relacionadas
4. **📊 Estructura:** Pide respuestas en formato específico (listas, tablas, etc.)

---

## ✨ **¡El proxy está listo para usar con ChatGPT!**

Simplemente copia cualquiera de los ejemplos de arriba y úsalos directamente en tu conversación con ChatGPT.
