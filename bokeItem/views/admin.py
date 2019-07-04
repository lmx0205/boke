from flask import Blueprint,render_template,request,g,session,redirect,url_for
admin = Blueprint('admin',__name__)
from app import Article,User,Comment,db
import os
from werkzeug.utils import secure_filename
# print(Article)

# 个人主页消息页
@admin.route('/')
def admin_message():
    user = g.user
    print(user.username)
    # comments = Comment.query.filter(Comment.user_id==1).all()
    # print(comments)
    return render_template('admin/admin_message.html',user=user)

# 个人文章页
@admin.route('/article')
def admin_article():
    user = g.user
    print(user)
    admin_articles = Article.query.filter(Article.user_id==user.id).order_by('-id').all()
    # print(admin_articles)
    return render_template('admin/admin_article.html',admin_articles=admin_articles,user=user)

# 删除文章
@admin.route('/admin_delete_article/<article_id>')
def admin_delete_article(article_id):
    user = g.user
    delete_articles = Article.query.filter(Article.id==article_id).first()
    # delete_comments = Comment.query.filter(Comment.article_id==delete_articles.id).all()
    # print(delete_articles,delete_comments)
    # db.session.delete(delete_articles)
    # for delete_comment in delete_comments:
    #     db.session.delete(delete_comment)
    # db.session.commit()
    delete_articles.isexit=1
    db.session.add(delete_articles)
    db.session.commit()
    return redirect(url_for('admin.admin_article'))

# 个人好友页
@admin.route('/friend')
def admin_friend():
    user=g.user
    return render_template('admin/admin_friend.html',user = user)

# 个人资料页
@admin.route('/mydata')
def mydata():
    user=g.user
    user = User.query.filter(User.id==user.id).first()
    return render_template('admin/admin_mydata.html',user=user)

# 修改个人资料
@admin.route('/editdata',methods=['GET','POST'])
def editdata():
    user = g.user
    if request.method == 'POST':
        try:
            image = request.files['image']
            username = request.form['username']
        
            user = User.query.filter(User.id==user.id).first()
            if username:
                user.username = username
                db.session.commit()
            if image:
                basepath = os.path.dirname(os.path.dirname(__file__))
                upload_path = os.path.join(basepath, 'static/img/admin/touxiang',secure_filename(image.filename))
                image.save(upload_path)
                path = ('/static/img/admin/touxiang/'+ secure_filename(image.filename))
                user.img = path
                db.session.commit()
            return render_template('admin/admin_mydata.html',user=user)
        except:
            return render_template('admin/admin_mydata.html',user=user)


    else:
        return render_template('admin/admin_editdata.html',user=user)
    
    return render_template('admin/admin_editdata.html',user=user)

# 评论页
@admin.route('/commentContent')
def commentContent():
    # comments_1 = Comment.query.filter(Comment.article_id==1).all()
    # 用户确定，确定该用户文章，再确认该文章评论
    user = g.user
    comments_self = Article.query.filter(Article.user_id==user.id).all()
    comments_else = {}
    for i in comments_self:
        comments_all = Comment.query.filter(Comment.article_id==i.id).all()
        if len(comments_all)>0:
            comments_else[i] = comments_all

    print(comments_else)

    return render_template('admin/comment.html',comments_else=comments_else,user=user)



# 在视图函数钱执行的钩子函数
@admin.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id==user_id).first()
        if user:
            g.user = user


# 可以判断显示登录状态，不登录的状态一直执行
@admin.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}