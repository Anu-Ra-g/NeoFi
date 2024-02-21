from api import db
from datetime import datetime

owners_table = db.Table('owners_table',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('note_id', db.Integer, db.ForeignKey('notes.id'))
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(355), nullable=False)

    notes = db.relationship('Note', secondary=owners_table, backref='owners')

    def save(self):
        db.session.add(self)
        db.session.commit()

class NoteVersion(db.Model):
    __tablename__ = 'note_versions'

    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    changes = db.Column(db.String(2000), nullable=False)

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    owners = db.relationship('User', secondary=owners_table, backref='notes')
    versions = db.relationship('NoteVersion', backref='note', lazy='dynamic')
    
    def save(self):
        db.session.add(self)
        db.session.commit()