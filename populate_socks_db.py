from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from socks_db import Base, User, Sock

engine = create_engine('sqlite:///selling_socks.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(id=1,
            name="Cartman",
            email="cartman@southpark.com",
            picture='https://citaty.info/files/styles/medium/public/characters/633.jpg')
session.add(user1)
session.commit()

sock1 = Sock(name="Dirty Socks",
            email="cartman@southpark.com",
            picture="https://decendants.in/wp-content/uploads/2018/08/HTB1xgucC79WBuNjSspeq6yz5VXaT.jpg",
            price=100,
            description="These socks are dirty. I wanna sell them.",
            seller=1)
session.add(sock1)
session.commit()

sock2 = Sock(name="Dirty Socks",
            email="cartman@southpark.com",
            picture="https://decendants.in/wp-content/uploads/2018/08/HTB1xgucC79WBuNjSspeq6yz5VXaT.jpg",
            price=100,
            description="These socks are dirty. I wanna sell them.",
            seller=1)
session.add(sock2)
session.commit()


user2 = User(id=2,
             name="Cartman Clone",
             email="cartmanclone@southpark.com",
             picture='https://citaty.info/files/styles/medium/public/characters/633.jpg')
session.add(user2)
session.commit()

sock3 = Sock(name="Dirty Socks",
             email="cartman@southpark.com",
             picture="https://decendants.in/wp-content/uploads/2018/08/HTB1xgucC79WBuNjSspeq6yz5VXaT.jpg",
             price=100,
             description="These socks are dirty. I wanna sell them.",
             seller=2)
session.add(sock3)
session.commit()



print "socks for sale set"
