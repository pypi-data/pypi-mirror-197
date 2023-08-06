import os
import logging
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from streambot import StreamBot

class StreamBotAPI:
    def __init__(self, streambots, host='0.0.0.0', port=80, origins=['*'], verbosity = 0, log_file=None, debug=False):
        self.host = host
        self.port = port
        self.streambots = streambots
        self.origins = origins
        self.verbosity = verbosity
        self.log_file = log_file
        self.debug = debug

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*", websocket=True)
        self.init_cors()
        self.init_routes()

        self.messages = {}

        # Configure logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if self.log_file:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def init_cors(self):
        CORS(self.app, resources={r"/api/*": {"origins": self.origins}})

    def init_routes(self):
        self.app.route('/api/getmessages/<context_id>/<user_id>', methods=['GET', 'POST'])(self.get_messages)
        self.app.route('/api/messages', methods=['POST'])(self.handle_messages)
        self.app.route('/api/newchat', methods=['POST'])(self.reset_chat)
        self.app.route('/api/addmessages', methods=['POST'])(self.add_messages)

    def chat_stream(self, messages, context_id):
        print(f'Context ID: {context_id}')
        print(self.streambots[int(context_id)].messages)
        for event in self.streambots[int(context_id)].chat_stream(messages):
            yield event

    def get_messages(self, context_id, user_id):
        connection_id = f"{context_id}_{user_id}"
        if connection_id in self.messages:
            return jsonify(self.messages[connection_id])
        else:
            self.messages[connection_id] = self.streambots[int(context_id)].messages.copy()
            return jsonify(self.messages[connection_id])

    def handle_messages(self):
        context_id = request.json.get('context_id')
        user_id = request.json.get('user_id')
        connection_id = f"{context_id}_{user_id}"
        message = request.json.get('message')
        if self.verbosity >= 1:
            self.logger.info(f'{connection_id} added: {message}')
        if connection_id in self.messages:
            self.messages[connection_id].append({"role": "user", "content": message})
        else:
            self.messages[connection_id] = [{"role": "user", "content": message}]

        response = ""

        for event in self.chat_stream(self.messages[connection_id], context_id=context_id):
            response += event
            self.socketio.emit('message', {'message': event, 'connection_id': connection_id}, room=user_id, broadcast=True)

        self.messages[connection_id].append({"role": "assistant", "content": response})
        return jsonify(self.messages[connection_id])
    
    def add_messages(self):
        #use this method to add messages without triggering ChatGPT response
        context_id = request.json.get('context_id')
        user_id = request.json.get('user_id')
        connection_id = f"{context_id}_{user_id}"
        message = request.json.get('message')
        role = request.json.get('role')

        if self.verbosity >= 1:
            self.logger.info(f'{connection_id} added: {message} to {role}')

        if connection_id in self.messages:
            self.messages[connection_id].append({"role":role,"content":message})
        else:
            self.messages[connection_id] = self.streambots[int(context_id)].messages
            self.messages[connection_id].append({"role":role,"content":message})
        
        return jsonify(True)

    def reset_chat(self):
        context_id = request.json.get('context_id')
        user_id = request.json.get('user_id')
        connection_id = f"{context_id}_{user_id}"
        if self.verbosity >= 1:
            self.logger.info(f'{user_id} reset chat to Context {context_id}')
        if connection_id in self.messages:
            self.messages[connection_id] = self.streambots[int(context_id)].messages.copy()
            if self.verbosity >= 1:
                print(f"{connection_id} messages: {self.messages[connection_id]}")
                print(f"{context_id} messages: {self.streambots[int(context_id)].messages}")
        return jsonify(True)

    def start(self):
        if self.verbosity >= 1:
            self.logger.info(f'server started on {self.host} on port {self.port}')
        self.app.run(host=self.host, port=self.port, debug=self.debug)
