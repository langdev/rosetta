from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import sql

db = SQLAlchemy()

class Topic(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.Unicode(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           default=sql.functions.now())

    __tablename__ = 'topics'


class Code(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    topic_id = db.Column(db.BigInteger, db.ForeignKey(Topic.id),
                         nullable=False)
    topic = db.relationship(Topic,
                            backref=db.backref('codes', lazy='dynamic'))
    lang = db.Column(db.Unicode(100), nullable=False)
    body = db.Column(db.UnicodeText, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           default=sql.functions.now())

    __tablename__ = 'codes'
