from flask import Flask, jsonify, request, render_template
import queue
import threading
import time
import logging
import os
from copilot import CopilotClient

prompt = queue.Queue()
username = 'miikka.karava@outlook.com'
password = 'VxDH6a4Q8'
shadow_element = None  
client = None

def create_app():
    app = Flask(__name__)

    ini_client()

    @app.route('/')
    def home():
        try:
            return render_template('index.html')  # "<body>test</body>" #
        except Exception as e:
            print(f'exception in index {str(e)}')
            return f'exception {str(e)}'


    @app.route('/send-message', methods=['POST'])
    def send_message():
        user_message = request.json.get('userMessage')
        print(user_message)
    

        if not prompt:
            return jsonify({'reply': "no message received."}), 400
        try:
            prompt.put(user_message)
            print(f'added user message: {user_message}')

            response = None
            while response is None:
                time.sleep(2)
                if not prompt.empty():
                    prompt_queue = prompt.get()
                    response = client.pilot_message(shadow_element, prompt_queue)
                    print(response)
            return jsonify({'reply': response})
                     
        except Exception as e:
            print(f'exception in response {str(e)}')
            return f'exception {str(e)}' 
     
    return app  

def ini_client():
    global client
    client = CopilotClient(url="https://copilot.microsoft.com", client_name='CopilotClient')#, verbose=True)
    client.launch_browser()
    client.login(shadow_element, username, password)
