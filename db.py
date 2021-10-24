#!/usr/bin/env python3

from flask_sqlalchemy import SQLAlchemy
from .app import *

db = SQLAlchemy(app)


readings_table = db.Table('readings', db.Base.metadata,
	db.Column('user_id', db.ForeignKey('user.id')),
	db.Column('book_id', db.ForeignKey('book.id')),
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	vk_id = db.Column(db.Integer, unique=True)
	telegram_id = db.Column(db.Integer, unique=True)
	read_books = db.relationship('Book', secondary=readings_table)

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	read_by = db.relationship('User', secondary=readings_table)


db.create_all()
db.session.commit()

# by InfantemTeam, 2021
# infantemteam@sdore.me
