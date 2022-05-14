from models import User, Post, connect_db, db
from app import app

# delete and create tables
db.drop_all()
db.create_all()

# clear tables if not already
User.query.delete()
Post.query.delete()

# adding users
user1=User(first_name='Dom', last_name='Shuey')
user2=User(first_name='Alex', last_name='Rider')
user3=User(first_name='Jessica', last_name='Alba') 
user4=User(first_name='Dwayne', last_name='Johnson')

# adding posts
post1 = Post(title='This car is awesome', content='Ferrari 911', user_id=3)
post2 = Post(title='I like dogs', content='Look at this German Sheperd', user_id=2)
post3 = Post(title='Cupcake Recipe', content='This is my recipe for the best cupcakes!', user_id=1)
post4 = Post(title='Woodworking 101', content='Here"s Part 1 to how to work with wood!', user_id=1)
post5 = Post(title='I lift heavy things', content='Look. I lift weight. It heavy.', user_id=4)

# adding users first bc fk
db.session.add_all([user1,user2, user3, user4])
db.session.commit()

# finally, adding posts
db.session.add_all([post1, post2, post3, post4, post5])
db.session.commit()

