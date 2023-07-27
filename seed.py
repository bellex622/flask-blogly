from models import db, User, Post
from app import app

db.drop_all()
db.create_all()

user1 = User(first_name = 'Stuart', last_name='Fleisher')
user2 = User(first_name='Belle',last_name='Xu')

post1 = Post(title="title1",content="content", user_id=1)
post2 = Post(title="title2",content="content", user_id=2)

db.session.add(user1)
db.session.add(user2)
db.session.add(post1)
db.session.add(post2)
db.session.commit()