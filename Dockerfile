FROM python:3.8-slim
LABEL maintainer="gonozov0@yandex.com"
RUN apt-get update && apt-get upgrade
COPY . /app
WORKDIR /app 
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "flask_app.py"]
EXPOSE 5000