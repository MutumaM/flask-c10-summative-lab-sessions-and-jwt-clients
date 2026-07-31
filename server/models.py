from sqlalchemy.orm import validates
from config import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)

    _password_hash = db.Column('password_hash', db.String, nullable=False)

    notes = db.relationship('Note', back_populates='user', cascade='all, delete-orphan')

    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username.strip()) == 0:
            raise ValueError('Username cannot be empty')
        return username

    @property
    def password_hash(self):
        raise AttributeError('password_hash is not a readable attribute')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))


class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='notes')

    @validates('title')
    def validate_title(self, key, title):
        if not title or len(title.strip()) == 0:
            raise ValueError('Title cannot be empty')
        return title