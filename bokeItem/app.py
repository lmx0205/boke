from flask import Flask, render_template, session, request, redirect, url_for
app = Flask(__name__, static_url_path=None,
            static_folder='static', template_folder='templates')
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# 因为sqlAlchemy模块默认是采用mysqldb模块进行数据库连接，python3数据库连接mysqldb不支持，
import pymysql
pymysql.install_as_MySQLdb()
# python3需要加上以上2句语句
import config
from sqlalchemy import *

app = Flask(__name__)
app.config.from_object('config')  # 通过配置对象来配置整个应用程序网站的配置

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(100), nullable=False)
    online = db.Column(db.Integer, nullable=False)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    # now()获取的是服务器第一次运行的时间，now就是每次创建一个模型的时候，都获取当前的时间
    time = db.Column(db.DateTime, default=datetime.now)
    types = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(100), nullable=False)
    readcount = db.Column(db.Integer, default=0) #阅读量
    agreecount = db.Column(db.Integer, default=0) #点赞数
    isexit = db.Column(db.Integer, default=2)  # 是否存在，0就是存在,1为删除，2为审核
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('articles'))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 降序排序 id从大到小
    article = db.relationship('Article', backref=db.backref('comments'))
    user = db.relationship('User', backref=db.backref('comments'))


class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    # 降序排序 id从大到小
    comment = db.relationship('Comment', backref=db.backref('replys'))
    user = db.relationship('User', backref=db.backref('replys'))
    article = db.relationship('Article', backref=db.backref('replys'))


db.create_all()


@app.route('/')
def boke():
    # article = Article.query.filter().all()
    article = Article.query.order_by('-id').all()  # 这是改过之后的排序(按时间排序)
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
    else:
        user = 0
    # print(article)
    # print(user)
    return render_template('indexs/index.html', article=article, user=user)

# 导航栏查找


@app.route('/search')
def search():
    q = request.args.get('q')
    userName = User.query.filter(User.username == q).first()
    if userName:
        article = Article.query.filter(Article.user_id == userName.id).all()
    else:
        article = Article.query.filter(or_(Article.title.contains(
            q), Article.content.contains(q), Article.types.contains(q)))

    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
    else:
        user = 0

    return render_template('indexs/index.html', article=article, user=user)

# 左边导航栏类型查找


@app.route('/searchType')
def searchType():
    t = request.args.get('t')
    article = Article.query.filter(Article.types.contains(t))

    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
    else:
        user = 0
    return render_template('indexs/index.html', article=article, user=user)


@app.route('/agree/<article_id>')
def agree(article_id):
    agrees = Article.query.filter(Article.id == article_id).first()
    agrees.agreecount += 1
    db.session.add(agrees)
    db.session.commit()
    return redirect(url_for('boke'))
