from flask import Flask, request, jsonify, send_file
from chatbot import SimpleChatbot
import os

app = Flask(__name__)
chatbot = SimpleChatbot()

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    response = chatbot.get_response(data['message'])
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)