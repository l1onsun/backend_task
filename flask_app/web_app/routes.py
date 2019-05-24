from flask import render_template, flash, redirect, url_for, request
from web_app import app, db
from web_app.forms import LoginForm, RegistrationForm
from web_app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from itsdangerous import URLSafeTimedSerializer
import pika
import pickle


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }]
    return render_template('index.html', user=user, title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        if not user.confirmed:
            flash('Plz confirm your email first')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, confirmed=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are almost registered user! Just confirm your email now!')

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))

        channel = connection.channel()
        channel.queue_declare(queue='RabbitMQ')

        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = serializer.dumps(user.email, salt=app.config['SECURITY_PASSWORD_SALT'])

        confirm_url = url_for('confirm', token=token, _external=True)

        channel.basic_publish(exchange='', routing_key='RabbitMQ',
                              body=pickle.dumps((user.email, confirm_url)))

        connection.close()

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#@login_required
@app.route('/confirm/<token>')
def confirm(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=600)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    return redirect(url_for('index'))
