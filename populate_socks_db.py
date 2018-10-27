from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from socks_db import Base, User, Sock

engine = create_engine('sqlite:///selling_socks.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(
    id=1,
    name="Cartman",
    email="cartman@southpark.com",
    picture='https://citaty.info/files/styles/' +
    'medium/public/characters/633.jpg')
session.add(user1)
session.commit()

user2 = User(
    id=2,
    name="Catdog",
    email="catdog@nickelodeon.com",
    picture='https://upload.wikimedia.org/wikipedia/' +
    'en/thumb/6/64/CatDog.jpeg/250px-CatDog.jpeg')
session.add(user2)
session.commit()

user3 = User(
    id=3,
    name="BMO",
    email="adventure@time.com",
    picture='http://cdn.shopify.com/s/files/1/2597/4920/products/' +
    'atag2134_1024x1024.jpg?v=1526629221')
session.add(user3)
session.commit()


user4 = User(
    id=4,
    name="Sponge Bob",
    email="sponge@bob.com",
    picture='https://pbs.twimg.com/profile_images/' +
    '1002272769352978433/9S4QWSR0_400x400.jpg')
session.add(user4)
session.commit()

user5 = User(
    id=5,
    name="Cat Lover",
    email="cat@forcats.com",
    picture='https://news.nationalgeographic.com/content/dam/news/' +
    '2018/05/17/you-can-train-your-cat/02-cat-training-Nat' +
    'ionalGeographic_1484324.ngsversion.1526587209178.adapt.1900.1.jpg')
session.add(user5)
session.commit()


sock1 = Sock(
    name="Dirty Socks",
    email="cartman@southpark.com",
    picture="https://decendants.in/" +
    "wp-content/uploads/2018/08/HTB1xgucC79WBuNjSspeq6yz5VXaT.jpg",
    price=10,
    description="These socks are dirty. I wanna sell them.",
    seller=1)
session.add(sock1)
session.commit()

sock2 = Sock(
    name="Super Winner Socks",
    email="sponge@bob.com",
    picture="https://raw.githubusercontent.com/MadinaB/SellingSocks/master" +
    "/static/img/s_6.png",
    price=5,
    description="Perfect socks for perfect people.",
    seller=4)
session.add(sock2)
session.commit()

sock3 = Sock(
    name="Cutie's socks",
    email="cat@forcats.com",
    picture="https://raw.githubusercontent.com/MadinaB/SellingSocks/master/" +
    "static/img/s_4.png",
    price=5,
    description="I have took photo of my son and printed it to many many " +
    "socks to share with the world. 5$, please",
    seller=5)
session.add(sock3)
session.commit()


sock4 = Sock(
    name="Cutie's socks",
    email="cat@forcats.com",
    picture="https://raw.githubusercontent.com/MadinaB/SellingSocks/master/" +
    "static/img/s_5.png",
    price=5,
    description="Selling socks with cats",
    seller=5)
session.add(sock4)
session.commit()


sock5 = Sock(
    name="Singin Bob",
    email="sponge@bob.com",
    picture="https://raw.githubusercontent.com/MadinaB/SellingSocks/master/" +
    "static/img/s_10.jpg",
    price=5,
    description="Perfect socks for perfect people.",
    seller=4)
session.add(sock5)
session.commit()


sock6 = Sock(
    name="Luxury socks",
    email="adventure@time.com",
    picture="https://raw.githubusercontent.com/MadinaB/SellingSocks/master/" +
    "static/img/s_7.png",
    price=50,
    description="Socks from limited collection",
    seller=3)
session.add(sock6)
session.commit()


print "socks for sale set"
