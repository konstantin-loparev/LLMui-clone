from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from langchain_community.llms.ollama import Ollama

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

ollama_model = Ollama(model="llama3.1")  # Убедитесь, что вы используете правильный метод инициализации

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    is_renamed = db.Column(db.Boolean, default=False, nullable=False)
    messages = db.relationship('Message', backref='chat', lazy=True, cascade="all, delete-orphan")

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' или 'bot'
    content = db.Column(db.Text, nullable=False)

@app.before_request
def create_tables():
    db.create_all()
    if not Chat.query.first():
        new_chat = Chat(title="Новый чат")
        db.session.add(new_chat)
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chats', methods=['GET'])
def get_chats():
    chats = Chat.query.order_by(Chat.id.desc()).all()
    return jsonify([{'id': chat.id, 'title': chat.title} for chat in chats])

@app.route('/chat/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    messages = Message.query.filter_by(chat_id=chat.id).all()
    return jsonify([{'sender': msg.sender, 'content': msg.content} for msg in messages])

@app.route('/chat', methods=['POST'])
def create_chat():
    new_chat = Chat(title="Новый чат")
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({'id': new_chat.id, 'title': new_chat.title})

@app.route('/chat/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    db.session.delete(chat)
    db.session.commit()
    return jsonify({'message': 'Chat deleted'})

@app.route('/chat/<int:chat_id>/message', methods=['POST'])
def add_message(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    data = request.json
    user_message = data['message']
    user_msg = Message(chat_id=chat.id, sender='user', content=user_message)
    db.session.add(user_msg)
    db.session.commit()

    if not chat.is_renamed:
        chat.title = user_message[:30]  # Первые 30 символов первого сообщения
        chat.is_renamed = True
        db.session.commit()

    bot_response = ollama_model.invoke(user_message)
    bot_msg = Message(chat_id=chat.id, sender='bot', content=bot_response)
    db.session.add(bot_msg)
    db.session.commit()

    return jsonify({
        'user_message': {'sender': user_msg.sender, 'content': user_msg.content},
        'bot_response': {'sender': bot_msg.sender, 'content': bot_msg.content}
    })

if __name__ == '__main__':
    app.run(debug=True)
