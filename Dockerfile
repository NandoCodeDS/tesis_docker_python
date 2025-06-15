FROM python:3.7

# Usar /app como directorio de trabajo
WORKDIR /docker_tesis_python

# Copiar todo el paquete al contenedor en /app
COPY ./docker_tesis_python /app/docker_tesis_python
COPY ./requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar FastAPI desde el módulo docker_tesis_python
CMD ["uvicorn", "docker_tesis_python.main:app", "--host", "0.0.0.0", "--port", "8000"]
