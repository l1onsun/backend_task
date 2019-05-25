FROM python:3.6-alpine
RUN apk add --update bash
ADD . /code
WORKDIR /code
RUN apk add --update py3-pip
RUN pip install -r requirements.txt

EXPOSE 587

CMD ["/code/wait-for-it.sh", "RabbitMQ:5672", "--", "python3", "/code/app.py"]
#CMD ["python3", "/code/app.py"]