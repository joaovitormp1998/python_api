FROM python:3.12-slim
COPY . /code

WORKDIR /code

# Instalação de dependências
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Execução das migrações do Alembic
# RUN alembic upgrade head

# Comando principal
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
