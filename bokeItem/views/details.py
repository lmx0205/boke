from flask import Blueprint, render_template, request, redirect, url_for, session, g
from app import Article, Comment, User, db, Reply
from functools import wraps
details = Blueprint('details', __name__)
from .tts import *

# from pydub import AudioSegment

# 登录限制的装饰器


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 如果登录状态，则可以执行访问
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            # 否则直接跳转到登录页面
            return redirect(url_for('login.login_index'))
    return wrapper


# 描述详情页
@details.route('/<article_id>', methods=['GET', 'POST'])
def detail(article_id):
    article = Article.query.filter(Article.id == article_id).first()
    TEXT = article.content
    TEXTindex = len(TEXT)

    print(TEXTindex)
    if len(TEXT) > 800:
        pass
    else:
        vedio(TEXT, article_id)
    print(len(TEXT))

    article.readcount += 1
    db.session.add(article)
    db.session.commit()
    comment = Comment.query.filter(Comment.article_id == article.id).first()
    reply = Reply.query.filter(Reply.article_id == article.id).first()
    comment_count = Comment.query.filter(
        Comment.article_id == article.id).count()
    return render_template('details/article.html', article=article, comment=comment, reply=reply, comment_count=comment_count)


# 增加评论页
@details.route('/add_comoment', methods=['POST', 'GET'])
@login_required
def add_comment():
    user = g.user
    content = request.form.get('comment_content')
    article_id = request.form.get('article_id')
    comment = Comment(content=content)
    # 有两个外键，得知道这个评论的作者和这个问题
    article = Article.query.filter(Article.id == article_id).first()

    comment.user = User.query.filter(User.id == user.id).first()
    comment.article = article
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('details.detail', article_id=article_id))


@details.route('/add_reply', methods=['POST', 'GET'])
@login_required
def add_reply():
    user = g.user
    content = request.form.get('reply_content')
    comment_id = request.form.get('comment_id')
    article_id = request.form.get('article_id')
    reply = Reply(content=content)
    # 有两个外键，得知道这个评论的作者和这个问题
    comment = Comment.query.filter(Comment.id == comment_id).first()
    article = Article.query.filter(Article.id == article_id).first()
    reply.user = User.query.filter(User.id == user.id).first()
    reply.comment = comment
    reply.article = article
    db.session.add(reply)
    db.session.commit()

    return redirect(url_for('details.detail', article_id=article_id))


# 在视图函数钱执行的钩子函数

@details.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


# 可以判断显示登录状态，不登录的状态一直执行
@details.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


@details.route('../')
def article_go_index():
    # return render_template('indexs/index.html')
    return redirect(url_for('boke'))

# @details.route('../admin/')


@details.route('/go_boke')
@login_required
def article_go_admin():
    return redirect(url_for('admin.admin_message'))
    # return render_template('admin/admin_message.html')


@details.route('/detail_agree/<article_id>')
@login_required
def detail_agree(article_id):
    detail_agrees = Article.query.filter(Article.id == article_id).first()
    detail_agrees.agreecount += 1
    db.session.add(detail_agrees)
    db.session.commit()
    return redirect(url_for('details.detail', article_id=detail_agrees.id))


@details.route('/article_id')
def playsound(article_id):
    article_id = article_id+'.mp3'
    song = AudioSegment.from_wav("6.wav")
    print(article_id)
    return redirect(url_for('details.detail', article_id=article_id))
