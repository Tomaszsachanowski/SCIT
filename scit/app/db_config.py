from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'flaskusr1'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345abc'
app.config['MYSQL_DATABASE_DB'] = 'shopingdatabase'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)