FROM python:alpine

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD ["python", "__main__.py"]

#ENTRYPOINT ["./main.py"]