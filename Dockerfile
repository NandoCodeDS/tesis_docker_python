FROM python:3.7

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo el contenido de la carpeta fuente
COPY ./docker_tesis_python ./docker_tesis_python

# Copiar también el requirements.txt
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar FastAPI desde el archivo docker_tesis_python/main.py
CMD ["uvicorn", "docker_tesis_python.main:app", "--host", "0.0.0.0", "--port", "8000"]
