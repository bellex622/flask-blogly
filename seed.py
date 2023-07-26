from models import db, User
from app import app

db.drop_all()
db.create_all()

user1 = User(first_name = 'Stuart', last_name='Fleisher')
user2 = User(first_name='Belle',last_name='Xu')

db.session.add(user1)
db.session.add(user2)
db.session.commit()