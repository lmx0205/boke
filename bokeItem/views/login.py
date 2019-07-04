from flask import Blueprint,Flask, render_template, request, redirect, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
import time
from app import User,db,Article,Comment
login = Blueprint('login',__name__)
import hashlib

# 登录首页
@login.route('/',methods = [ 'GET','POST'] )
def login_index():
    if request.method == 'GET':
        return render_template('login_register/login.html')
    else:
        telephone = request.form.get('login-telephone')
        password = request.form.get('login-password')
        #对用户输入的密码进行加密
        hash = hashlib.md5(bytes('9385',encoding='utf-8'))#md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来
        hash.update(bytes(password,encoding='utf-8'))#要对哪个字符串进行加密，就放这里
        password = hash.hexdigest()
        #验证
        vcode= request.form.get('vcode')
        print(vcode)
        user = User.query.filter(User.telephone==telephone).first()
        if user and user.password==password:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('boke'))
        else:
            # return redirect(url_for('login.login_index'))
            return render_template('login_register/login.1.html')

# 管理员登录页
@login.route('/login_gl',methods=['GET','POST'])
def login_gl_index():
    if request.method == 'GET':
        return render_template('login_register/login_gl.html')
    else:
        username = request.form.get('username')
        password = request.form.get('pw')
        #对用户输入的密码进行加密
        # md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来
        hash = hashlib.md5(bytes('9385', encoding='utf-8'))
        hash.update(bytes(password, encoding='utf-8'))  # 要对哪个字符串进行加密，就放这里
        password = hash.hexdigest()
        
        user = User.query.filter(User.id==1).first()        
        if user and user.password==password:
                session['user_id'] = user.id
                session.permanent = True
                return render_template('X-admin/index.html',user=user)
        else:
            return render_template('login_register/login_gl.html')
# 欢迎首页
@login.route('/welcome.html',methods=['GET','POST'])
def welcome():
    users = User.query.filter(User.id!=1).all()  
    articles = Article.query.filter().all()
    comments = Comment.query.filter().all()
    readcount = 0
    agreecount = 0
    for article in articles:
        readcount += article.readcount
        agreecount += article.agreecount
    return render_template('X-admin/welcome.html',users=users,articles=articles,comments=comments,readcount=readcount,agreecount=agreecount) 

# 成员列表页
@login.route('/member-list.html',methods=['GET','POST'])
def member_list():
    users = User.query.filter(User.id!=1).all()
    return render_template('X-admin/member-list.html',users=users) 

# 删除成员
@login.route('/member-list.html/<user_id>') 
def member_list_del(user_id):
    delete_users = User.query.filter(User.id==user_id).first()
    delete_users.online = 1
    db.session.add(delete_users)
    db.session.commit()
    time.sleep(2)
    return redirect(url_for('login.member_list'))   
# 恢复成员
@login.route('/member-del.html/<user_id>') 
def member_list_huihu(user_id):
    delete_users = User.query.filter(User.id==user_id).first()
    delete_users.online = 0
    db.session.add(delete_users)
    db.session.commit()
    time.sleep(2)
    return redirect(url_for('login.member_del'))

# 成员恢复页
@login.route('/member-del.html',methods=['GET','POST'])
def member_del():
    users = User.query.filter(User.id!=1).all()
    return render_template('X-admin/member-del.html',users=users) 

# 文章列表页
@login.route('/article-list.html',methods=['GET','POST'])
def article_list():
    articles = Article.query.filter().all()
    return render_template('X-admin/article-list.html',articles=articles)

# 删除文章
@login.route('/article-list.html/<article_id>') 
def article_list_del(article_id):
    delete_articles = Article.query.filter(Article.id==article_id).first()
    delete_articles.isexit = 1
    db.session.add(delete_articles)
    db.session.commit()
    time.sleep(2)
    return redirect(url_for('login.article_list'))
# 文章恢复
@login.route('/article-del.html/<article_id>') 
def article_del_huihu(article_id):
    delete_articles = Article.query.filter(Article.id==article_id).first()
    delete_articles.isexit = 0
    db.session.add(delete_articles)
    db.session.commit()
    time.sleep(2)
    return redirect(url_for('login.article_del'))

# 文章恢复页
@login.route('/article-del.html',methods=['GET','POST'])
def article_del():
    articles = Article.query.filter().all()
    return render_template('X-admin/article-del.html',articles=articles) 

# 评论页
@login.route('/order-list.html',methods=['GET','POST'])
def order_list():
    comments = Comment.query.filter().all()
    return render_template('X-admin/order-list.html',comments=comments) 
# 分类页
@login.route('/cate.html',methods=['GET','POST'])
def cate():
    articles = Article.query.filter().all()
    return render_template('X-admin/cate.html',articles=articles) 

# 审核页
@login.route('/check-list.html',methods=['GET','POST'])
def check_article():
    articles = Article.query.filter().all()
    return render_template('X-admin/check-list.html',articles=articles)
# 审核文章通过
@login.route('/check-list.html/<article_id>') 
def article_list_check(article_id):
    delete_articles = Article.query.filter(Article.id==article_id).first()
    delete_articles.isexit = 0
    db.session.add(delete_articles)
    db.session.commit()
    time.sleep(2)
    return redirect(url_for('login.check_article'))


# 注销跳转登录页
@login.route('/logout')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login.login_index'))
