FROM python:3.7

WORKDIR /docker_tesis_python

COPY ./docker_tesis_python /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "docker_tesis_python.main:app", "--host", "0.0.0.0", "--port", "8000"]
