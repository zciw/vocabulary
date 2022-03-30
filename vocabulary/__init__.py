from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from vocabulary import settings

print('settingsngs: ', settings)
s = settings.Settings()
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = s.db_uri
app.secret_key = s.secret_key

from vocabulary import routes

