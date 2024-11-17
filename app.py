from flask import Flask, jsonify, request, render_template
import queue
import threading
import time
import logging
from copilot_vm_new import CopilotClient

app = Flask(__name__)

prompt = queue.Queue()
username = None #'miikka.karava@outlook.com'
password = None #'VxDH6a4Q8'
shadow_element = None  
client = None
prompt_queue = "test message"

def login():

    global client
   # if client is None:
    try:
        client = CopilotClient(url="https://copilot.microsoft.com", client_name='CopilotClient')#, verbose=True)
        client.launch_browser()
        client.login(shadow_element, username, password)
        return "logged in"        

    except Exception as e:
        #logging.error(f"Error initializing CopilotClient: {e}")
        client = None
        return False

login()

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
    #logging.debug(f'message {request.json} received')
    data = request.get_json()
    user_message = data.get('userMessage', '')
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
                print(f'prompt_queue = {prompt_queue}')
                response = client.pilot_message(shadow_element, prompt_queue)
                print(response)
        return jsonify({'reply': response})
                  
    except Exception as e:
        print(f'exception in response {str(e)}')
        return f'exception {str(e)}'        


if __name__ == '__main__':

    #login()
    print('logged in')
    app.run(host="0.0.0.0", port=8080, debug=False)
