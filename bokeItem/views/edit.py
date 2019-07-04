from flask import Flask, Blueprint,render_template,request,redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from config import*
from functools import wraps
from datetime import datetime
from sqlalchemy import or_
from werkzeug.security import generate_password_hash,check_password_hash
from app import db,Article,User
from random import random ,randint

edit = Blueprint('edit',__name__)


# 登录限制的装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        # 如果登录状态，则可以执行访问
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            # 否则直接跳转到登录页面
            return redirect(url_for('login.login_index'))
    return wrapper


# 编辑发布文章页
@edit.route('/',methods = ['GET','POST'])
@login_required
def edit_article():
    if request.method == 'GET':
        return render_template('edit/contact.html')
        
    else:
        title = request.form.get('title')
        
        content = request.form.get('content')
        types = request.form.get('types')
        imager=request.files['imager']
        text1=request.form.get('text1')
        # basepath = os.path.dirname(os.path.dirname(__file__))
        # print(basepath)
        num = randint(1,100000000)
        
        imager.save('./static/imager/%d%s' % ( num,imager.filename))
        img= '/static/imager/%d%s' % ( num,imager.filename)
        user = g.user
        article = Article(title=title,content=text1,types=types,user_id=user.id,img=img)
        # 因为有外键所以要指明是哪个作者author，所以从session里取出user_id找出user赋予question的作者
        article.author = user
        # print(article.author)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('boke'))

# 在视图函数钱执行的钩子函数
@edit.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id==user_id).first()
        if user:
            g.user = user


# 可以判断显示登录状态，不登录的状态一直执行
@edit.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}



