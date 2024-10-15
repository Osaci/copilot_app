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
from ..utils import check_filetype, is_url
from ..base_browser import BaseBrowser


class CopilotClient(BaseBrowser):
    """
    PiClient class to interact with Pi.
    It helps you to connect to https://copilot.microsoft.com/.
    Apart from core functionality Copilot supports web search.
    It is not possible to regenerate a response by using Copilot
    """

    def __init__(self, **kwargs):
        super().__init__(
            client_name="Copilot",
            url="https://copilot.microsoft.com", #https://copilot.microsoft.com/
            credential_check=False,
            cold_start=False,
            **kwargs,
        )
        self.logged_in = False

    def login(self, shadow_element, username: str = None, password: str = None):
        """
        Performs the login process with the provided username and password.
        You don't need to login to use Pi
        
        This function operates on the login page.
        It finds and clicks the login button,
        fills in the email and password textboxes

        Args:
            username (str): The username to be entered.
            password (str): The password to be entered.

        Returns:
            bool : True
        """       
        
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

    def reiterate(self, shadow_element, name, decade, prompt: str):
        prompt = f"{user_message}"

        try:
            get_response = self.interact(shadow_element, prompt)

            if get_response:
                if "I'm sorry" in get_response:  
                    return False    
 
                else:
                    return True

        except Exception as e:
            print(f'exception processing {decade} naval ship: {name}: {str(e)}')
            time.sleep(5)

        return False

    def pilot_message(self, shadow_element, name, decade, prompt: str):

        try:

            description = self.interact(shadow_element, prompt)         


            if description:
                return description
            else:
                return False

        except Exception as e:
            print(f'pilot exception {str(e)}')
            time.sleep(30)

            return True
       
    def postload_custom_func(self) -> None:
        """Copilot requires to accept privacy terms, the cookie below provides the response."""
        self.browser.add_cookie({"name": "BCP", "value": "AD=0&AL=0&SM=0"})
        self.browser.get(self.url)
        time.sleep(1)

    def is_ready_to_prompt(self, shadow_element, text_area) -> bool:
        """
        Checks if the Copilot is ready to be prompted.
        The indication for an ongoing message generation process
        is a disabled send button. The indication for no input is the same
        disabled button. Therefore we put a dummy dot into the textarea
        and we are left with the only reason for the button to be disabled,
        that is, a message being generated.

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
        
        time.sleep(55) 

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

    def upload_image(self, action_bar: ShadowRoot, image_path: Union[str, Path]) -> bool:
        """Upload an image or a url and wait until it is uploaded,
        then returns.

        Args:
            action_bar (ShadowRoot): Action bar shadow root to find sub elements.
            image_path (str): the file path to image or the url.

        Returns:
            bool: True if the image loaded properly, False otherwise
        """
        if isinstance(image_path, Path):
            image_path = str(image_path)
        url = is_url(image_path)
        file = Path(image_path).exists() and check_filetype(image_path, self.markers.file_types)

        if not (url or file):
            self.logger.warning("Given path is neither an image path nor a url")
            return False
        if url:
            camera_button = self.find_or_fail(
                By.ID,
                self.markers.cam_btn_iq,
                dom_element=action_bar
            )
            camera_button.click()
            vs = self.find_or_fail(
                By.CLASS_NAME,
                self.markers.vis_srch_cq,
                dom_element=action_bar
            )
            url_bar = self.find_or_fail(
                By.ID,
                self.markers.url_iq,
                dom_element=vs.children()[0].shadow_root
            )
            url_bar.send_keys(image_path)
            url_bar.send_keys(Keys.ENTER)
        elif file:
            im_input_element = self.find_or_fail(
                By.ID,
                self.markers.img_upload_iq,
                dom_element=action_bar,
            )
            im_input_element.send_keys(image_path)

        at_list = self.find_or_fail(
            By.CSS_SELECTOR, self.markers.at_list_cq, dom_element=action_bar, return_shadow=True
        )
        file_item = self.find_or_fail(
            By.CSS_SELECTOR, self.markers.file_item_cq, dom_element=at_list, return_shadow=True
        )
        condition = EC.presence_of_element_located((By.CLASS_NAME, self.markers.thumbnail_cq))
        WebDriverWait(file_item, 10).until(condition)
        return True

    
    def interact(self, shadow_element, prompt: str, image_path: Union[str, Path] = None) -> str:
        """Sends a prompt and retrieves the response from the Copilot system.

        This function interacts with the Copilot.
        It takes the prompt as input and sends it to the system.
        The prompt may contain multiple lines separated by '\\n'.
        In this case, the function simulates pressing SHIFT+ENTER for each line.
        Upon arrival of the interaction, the function waits for the response.
        Once the response is ready, the function will return the response.
        """

        text_area = self.find_or_fail(By.CSS_SELECTOR, "textarea[id='userInput']", dom_element=shadow_element)

        if not text_area:
            self.logger.error("Unable to locate text area, interaction fails.")
            return ""

        for each_line in prompt.split("\n"):
            text_area.send_keys(each_line)
            text_area.send_keys(Keys.SHIFT + Keys.ENTER)

        # Click enter and send the message
        text_area.send_keys(Keys.ENTER)

        if not self.is_ready_to_prompt(shadow_element, text_area):
            self.logger.info("Cannot retrieve the response, something is wrong")
            return ""

        text = self.get_last_response()
        self.logger.info("response is ready")
        self.log_chat(prompt=prompt, response=text)
        return text










