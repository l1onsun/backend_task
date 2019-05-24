FROM python:3.6-alpine
RUN apk add --update bash
ADD . /code
COPY . /code
WORKDIR /code
RUN apk add --update py3-pip
RUN pip install -r requirements.txt

#ENV FLASK_APP /code/app.py

EXPOSE 5000
#CMD ["/code/wait-for-it.sh", "rabbit:5672", "--", "flask", "run"]
CMD ["python3", "/code/app.py"]