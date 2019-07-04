from flask import Blueprint,render_template,request, redirect,url_for
from app import User,db
register = Blueprint('register',__name__)
import hashlib

# 注册页
@register.route('/',methods=['GET','POST'])
def register_index():
    if request.method == 'GET':
        return render_template('login_register/register.html')
    else:
        telephone = request.form.get('register-telephone')
        username = request.form.get('register-username')
        password1 = request.form.get('register-password1')
        password2 = request.form.get('register-password2')
        print(password1)
        print(password2)
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '该手机号已被注册'
        else:
            if password1 != password2:
                return '两次密码不相等，请核对后再填写'
            else:
                #存入数据库之前对密码进行加密
                hash = hashlib.md5(bytes('9385',encoding='utf-8'))#md5对象，md5不能反解，但是加密是固定的，就是关系是一一对应，所以有缺陷，可以被对撞出来
                hash.update(bytes(password1,encoding='utf-8'))#要对哪个字符串进行加密，就放这里
                # print(hash.hexdigest())
                password1 = hash.hexdigest()

                user = User(telephone=telephone,username=username,password=password1,img='https://ps.ssl.qhimg.com/sdmt/133_135_100/t01d63c6c44877e340b.jpg',online='0')
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login.login_index'))