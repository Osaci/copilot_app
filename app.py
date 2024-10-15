from flask import Flask, jsonify, request, render_template
import queue
import threading
import time
import logging
from copilot import CopilotClient

app = Flask(__name__)

prompt = queue.Queue()
username = 'miikka.karava@gmail.com'
password = 'tvJ6w/1d8TW4=x6'
shadow_element = None  

@app.route('/')

def home():
    try:
        return render_template('index.html') #"<body>test</body>" #
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

if __name__ == '__main__':

    client = CopilotClient(url="https://copilot.microsoft.com", client_name='CopilotClient')#, verbose=True)
    client.launch_browser()
    client.login(shadow_element, username, password)

    app.run(debug=False)

