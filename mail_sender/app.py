from flask import Flask
import pika
import traceback, sys
from config import Config
from flask_mail import Mail, Message
import pickle

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

# with app.app_context():
#     print("__pre")
#     mail.send(Message("test mail, sorry if misaddressed ", body="www.vk.com/",recipients=['lionson@mail.ru'], sender=app.config['MAIL_USERNAME']))
#     print("__after")

conn_params = pika.ConnectionParameters('RabbitMQ', port=5672, socket_timeout=10)
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.queue_declare(queue='RabbitMQ')


def callback(ch, method, properties, body):
    email, url = pickle.loads(body)
    print("email", email, "sent")
    # serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    # token = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
    with app.app_context():
        mail.send(Message("confirm your email plz",
                          recipients=[email],
                          sender=app.config['MAIL_USERNAME'],
                          body="folow this url to confim your email: " + url))


channel.basic_consume(callback, queue='RabbitMQ', no_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)
