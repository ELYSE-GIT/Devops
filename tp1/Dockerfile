
FROM python:3.8.13-alpine3.15 

WORKDIR /tp1 

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY Curl.py . 

EXPOSE 5000 
ENTRYPOINT [ "python", "Curl.py" ]

