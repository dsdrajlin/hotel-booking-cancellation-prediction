FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY models/ /app/models/

WORKDIR /app/src

EXPOSE 9696

CMD ["python", "serve.py"]
