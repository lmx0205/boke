DEBUG = True

HOSTNAME = '127.0.0.1'  # 主机名
PORT = 3306  # 端口号
DATABASE = 'boke'  # 数据库名称
USERNAME = 'root'  # 用户名
PASSWORD = 'root'  # 密码

SECRET_KEY = '123456'


# 数据库SQLAlchemy，SQLALCHEMY_DATABASE_URI
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False
