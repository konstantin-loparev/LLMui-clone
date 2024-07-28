from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    messages = db.relationship('Message', backref='chat', lazy=True, cascade="all, delete-orphan")

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' или 'bot'
    content = db.Column(db.Text, nullable=False)
