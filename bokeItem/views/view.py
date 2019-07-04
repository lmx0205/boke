from app import app
from views.admin import admin
from views.edit import edit
from views.details import details
from views.login import login
from views.register import register
#这里分别给app注册了两个蓝图admin,user
#参数url_prefix='/xxx'的意思是设置request.url中的url前缀，
#即当request.url是以/admin或者/user的情况下才会通过注册的蓝图的视图方法处理请求并返回
app.register_blueprint(admin,url_prefix='/admin')
app.register_blueprint(edit, url_prefix='/edit')
app.register_blueprint(details,url_prefix='/details')
app.register_blueprint(login,url_prefix='/login')
app.register_blueprint(register,url_prefix='/register')