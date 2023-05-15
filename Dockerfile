FROM python:3.9-alpine

WORKDIR /e_commerce_api
RUN apk add gcc musl-dev postgresql-dev
COPY . .
RUN pip install -r requirements.txt 

CMD ["python", "app.py"]

# docker build -t e_commerce_api .
# docker run -d --name e_commerce_api --restart always -p 5115:5115 e_commerce_api