
class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    img = db.Column(db.String(100),nullable=False)
    online = db.Column(db.Integer,nullable=False)


class Article(db.Model):
    __tablename__='article'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.TEXT,nullable=False)
    # now()获取的是服务器第一次运行的时间，now就是每次创建一个模型的时候，都获取当前的时间
    time = db.Column(db.DateTime,default=datetime.now)
    types = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User',backref=db.backref('articles'))

class Comment(db.Model):
    __tablename__ ='comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.TEXT,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    article_id = db.Column(db.Integer,db.ForeignKey('article.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # 降序排序 id从大到小
    article = db.relationship('Article',backref = db.backref('comments'))
    user = db.relationship('User',backref = db.backref('comments'))

db.create_all()