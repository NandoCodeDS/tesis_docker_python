FROM python:3.7

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el contenido del código fuente
COPY ./docker_tesis_python /app/docker_tesis_python

# Copiar también el archivo de requerimientos
COPY ./requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar la app FastAPI ubicada en docker_tesis_python/main.py
CMD ["uvicorn", "docker_tesis_python.main:app", "--host", "0.0.0.0", "--port", "8000"]
