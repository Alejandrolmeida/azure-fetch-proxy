# Usar imagen base de Python oficial
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY main.py .

# Exponer puerto
EXPOSE 8000

# Variables de entorno por defecto
ENV API_KEY=change-me-in-azure
ENV MAX_REQUESTS_PER_MINUTE=100
ENV MAX_REQUESTS_PER_HOUR=2000
ENV MAX_RESPONSE_SIZE_MB=15

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
