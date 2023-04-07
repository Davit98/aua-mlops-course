FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install connexion[swagger-ui]==2.14.2

COPY . .

RUN chmod +x start_service.sh

# Informing Docker that the container will listen on the specified network port (8000) at runtime.
EXPOSE 8000  
ENTRYPOINT ["./start_service.sh"]