from flask import Flask, jsonify, request, render_template
import queue
import threading
import time

"""Class definition for Copilot client"""

import time
import requests
import re
import pandas as pd
import csv
from pathlib import Path
from typing import Union, Dict


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.shadowroot import ShadowRoot
from talkingheads utils import check_filetype, is_url

app = Flask(__name__)

class CopilotClient:
    def __init__(self):
        self.url="https://copilot.microsoft.com", 
        self.browser = None
        self.logged_in = False


    def launch_browser(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)
        self.browser.maximize_window()
        time.sleep(5)

app = Flask(__name__)

class CopilotClient:
    def __init__(self):
        self.url = "https://copilot.microsoft.com"
        self.browser = None
        self.logged_in = False

    def launch_browser(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)
        self.browser.maximize_window()
        time.sleep(5)


    def login(self, shadow_element, prompt_queue: str, username: str = None, password: str = None):
        
        try:
            accept = self.find_or_fail(By.CSS_SELECTOR, "button[title='Accept']", dom_element=shadow_element)
            accept.click()
        except Exception as e:
            time.sleep(2)

            username = 'm11kk4@windowslive.com'
            password = 'VxDH6a4Q8'

            log_in = self.find_or_fail(By.ID, ':ra:', dom_element=shadow_element)
            # (By.XPATH, "//input[@value='sign in']")
            log_in.click()
            
            time.sleep(2)

            account = self.find_or_fail(By.CSS_SELECTOR, "button[title='Sign in']", dom_element=shadow_element)
            account.click()

            time.sleep(5)

            username_field = self.find_or_fail(By.ID, 'i0116', dom_element=shadow_element)
            username_field.click()
            username_field.send_keys(username)
            username_field.send_keys(Keys.ENTER)

            time.sleep(5)

            password_field = self.find_or_fail(By.ID, 'i0118', dom_element=shadow_element)
            password_field.click()
            password_field.send_keys(password)
            password_field.send_keys(Keys.ENTER)

            time.sleep(5)

            accept = self.find_or_fail(By.ID, 'acceptButton', dom_element=shadow_element)
            accept.click()
            
            time.sleep(5)

            """
            get_started = self.find_or_fail(By.CSS_SELECTOR, "button[title='Get started']", dom_element=shadow_element)
            get_started.click()
            
            time.sleep(5)
            """
            self.logged_in = True
            return True
            

        except Exception as e:
            print('login exception')
            time.sleep(5)
            self.logged_in = True
            return True

    def reiterate(self, shadow_element, name, decade, prompt_queue: str):
        prompt_queue = f"{user_message}"

        try:
           
            get_response = self.interact(shadow_element, prompt_queue: str)

            if get_response:
                if "I'm sorry" in get_response:  
                    return False    
 
                else:
                    return True

        except Exception as e:
            print(f'exception processing: {str(e)}')
            time.sleep(5)

        return False

    def pilot_message(self, shadow_element, name, decade, prompt_queue: str):

        try:
            while True:

            description = self.interact(shadow_element, prompt_queue)         


            if description:
                return description
            else:
                return False

        except Exception as e:
            print(f'pilot exception {str(e)}')
            time.sleep(30)

            return True
      

    def is_ready_to_prompt(self, shadow_element, text_area) -> bool:

        Returns:
            bool : return if the system is ready to be prompted.

        button = self.find_or_fail(
            By.CLASS_NAME, self.markers.button_cq, dom_element=shadow_element
        )
        button = self.find_or_fail(By.TAG_NAME, "button", dom_element=button)

        """
        text_area = self.find_or_fail(By.CSS_SELECTOR, "textarea[id='userInput']", dom_element=shadow_element)

        text_area.send_keys(".")

        button = self.find_or_fail(By.CSS_SELECTOR, "button[title='Submit message']", dom_element=shadow_element)

        if not button:
            return False

        self.wait_object.until(EC.element_to_be_clickable(button))

        # Then, we clear the text area to make space for new interacton :)
        text_area.send_keys(Keys.CONTROL + "a", Keys.DELETE)
        return True

    def get_last_response(self, check_greeting: bool = False) -> str:
        """Returns the last response in the chat view.

        Args:
            check_greeting (bool): If set, checks the greeting message, provided after clicking New Topic.

        Returns:
            str: The last generated response
        """

        get_response = self.browser.find_elements(By.CSS_SELECTOR, "div[class='space-y-3 break-words']")
        
        time.sleep(5) 

        #text = description.replace('\r', ' ').strip()
        text_response = get_response[-1]
        text = text_response.text
        text = re.sub(r'\d+\s*', '', text)
        text = re.sub(r'\s+\.', '', text)
        text = re.sub(r'\s+\Does this capture.*', '', text)

        #text = re.sub(r'^\s*$', '', text, flags=re.MULTILINE)
        print(text)
        #text = "\n\n".join(get_response.text(separator=' ')).strip()
        # Fix citations
        #text = re.sub(r"\n(\d{1,2})", r"[\g<1>]", text)

        return text



    def interact(self, shadow_element, prompt_queue: str, image_path: Union[str, Path] = None) -> str:

        text_area = self.find_or_fail(By.CSS_SELECTOR, "textarea[id='userInput']", dom_element=shadow_element)

        if not text_area:
            self.logger.error("Unable to locate text area, interaction fails.")
            return ""

        for each_line in prompt_queue.split("\n"):
            text_area.send_keys(each_line)
            text_area.send_keys(Keys.SHIFT + Keys.ENTER)

        # Click enter and send the message
        text_area.send_keys(Keys.ENTER)

        if not self.is_ready_to_prompt(shadow_element, text_area):
            self.logger.info("Cannot retrieve the response, something is wrong")
            return ""

        text = self.get_last_response()
        self.logger.info("response is ready")
        self.log_chat(prompt_queue=prompt_queue, response=text)
        return text

client = CopilotClient()
client.launch_browser()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
    def send_message():
        data = request.get_json()
        user_message = data.get('userMessage')

        if not user_message:
            return jsonify({'reply': "no message received."})

       shadow_element = None
       login = client.login(shadow_element, username, password)
       response = client.interact(shadow_element, prompt_queue)

       return jsonify({'reply', response})

   if __name__ == '__main__':
       app.run(debug=True)





