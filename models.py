from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.util import KeyedTuple
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


import os

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = '~t\x86\xc9\x1ew\x8bOcX\x85O\xb6\xa2\x11kL\xd1\xce\x7f\x14<y\x9e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'spellchecker.db')
db = SQLAlchemy(app)

class LoginRecord(db.Model):
    record_number = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    time_off = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_by_user_id(user_id):
        return LoginRecord.query.filter_by(user_id=user_id).first()

    def __repr__(self):
        return "<User '{}'>".format(self.user_id)

class QueryRecord(db.Model):
    query_number = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    results = db.Column(db.Text, nullable=False)


    @staticmethod
    def get_by_user_id(user_id):
        return LoginRecord.query.filter_by(user_id=user_id).first()

    def __repr__(self):
        return "<User '{}'>".format(self.user_id)




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    twofa_hash = db.Column(db.String)
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    def twofa(self):
        raise AttributeError('twofa: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def twofa(self, password):
        self.twofa_hash = generate_password_hash(twofa)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)



