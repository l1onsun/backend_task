from web_app import db
from web_app.models import User

all_users = User.query.all()
for user in all_users:
    db.session.delete(user)
db.session.commit()