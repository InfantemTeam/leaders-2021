#!/usr/bin/env python3

from flask_sqlalchemy import SQLAlchemy
from .app import *

db = SQLAlchemy(app)


readings_table = db.Table('readings', db.metadata,
	db.Column('user_id', db.ForeignKey('user.id')),
	db.Column('book_id', db.ForeignKey('book.id')),
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	name = db.Column(db.String(255))
	surname = db.Column(db.String(255))
	bdate = db.Column(db.String(10))
	vk_id = db.Column(db.Integer, unique=True)
	telegram_id = db.Column(db.Integer, unique=True)
	read_books = db.relationship('Book', secondary=readings_table, back_populates='read_by')

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	read_by = db.relationship('User', secondary=readings_table, back_populates='read_books')


db.create_all()
if (not User.query.filter_by(id=0).first()):
	default_user = User(id=0)
	db.session.add(default_user)
db.session.commit()

# by InfantemTeam, 2021
# infantemteam@sdore.me
