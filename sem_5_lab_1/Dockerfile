FROM python:3.6.1-alpine
RUN pip install --upgrade pip
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt

CMD ["python", "api.py"]

# docker build -t fsapi .
# docker run -d -p 5000:5000 fsapiapp
# docker ps <- check processes