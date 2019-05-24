FROM python:3.6-alpine
RUN apk add --update bash
ADD . /code
WORKDIR /code
RUN apk add --update py3-pip
RUN pip install -r requirements.txt

#EXPOSE 8000

#CMD ["sender/wait-for-it.sh", "rabbit:5672", "--", "python3", "sender/app.py"]
CMD ["python3", "/code/app.py"]