from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api

app = Flask(__name__)
app.secret_key = b'\xf3\x9a\x1c\xd4\x8e\x02\x91\xbb'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db = SQLAlchemy()
db.init_app(app)              

migrate = Migrate(app, db)     
bcrypt = Bcrypt(app)
api = Api(app)