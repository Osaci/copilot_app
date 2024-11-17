from flask import Flask, jsonify, request, render_template
import queue
import requests
import threading
import time
import logging
import os
from vertex import VertexClient

app = Flask(__name__)

prompt = queue.Queue()
username = 'miikka.karava@outlook.com'
password = 'VxDH6a4Q8'  
client = VertexClient()

def login():

    global client
    #if client is None:
    try:
        return "logged in"        

    except Exception as e:
        #logging.error(f"Error initializing CopilotClient: {e}")
        client = None
        return False

#login()

@app.route('/')
def home():
    try:
        return render_template('index.html') #"<body>test</body>" #
    except Exception as e:
        print(f'exception in index {str(e)}')
        return f'exception {str(e)}'


#logging.basicConfig(level=logging.DEBUG)
@app.route('/send-message', methods=['POST'])
def send_message():
    try:
    #logging.debug(f'message {request.json} received')

    
        data = request.get_json()

        #response = requests.post('http://host.docker.internal:8080/send-message', json=data)
        #response = response.json()

        user_message = response.get('userMessage', '')
        print(user_message)
    
 
        if not prompt:
            return jsonify({'reply': "no message received."}), 400
        try:
            prompt.put(user_message)
            print(f'added user message: {user_message}')

            response = None
            timeout = 10
            start_time = time.time()
            while response is None #and time.time() - start_time < timeout:
                time.sleep(1)
                if not prompt.empty():
                    prompt_queue = prompt.get()
                    print(f'prompt_queue = {prompt_queue}')
                    response = client.multiturn_generate_content(prompt_queue)
                    print(response)
            if response is None:
                return jsonify({'error': 'error waiting for response'}), 504
            return jsonify({'reply': response})
           
        except Exception as e:
            print(f'exception {e}')
            return jsonify({'error': f'exception {str(e)}'}), 500
       
    except requests.exceptions.RequestException as e:
        print(f'exception during POST request {e}')
        return jsonify({'error': f'exception during POST request {e}'}), 500

if __name__ == '__main__':

    #login()
    print('logged in')
    app.run(host="0.0.0.0", port=8080, debug=False)
