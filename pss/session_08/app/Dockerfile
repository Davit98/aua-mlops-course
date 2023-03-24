FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install connexion[swagger-ui]==2.14.2

COPY . .

EXPOSE 8000
CMD ["python", "openapi_main.py"]