from flask import Flask, jsonify, request, render_template
import queue
import threading
import time
import logging
import subprocess
from datetime import datetime


"""Class definition for Copilot client"""

import time
import requests
import re
import pandas as pd
import csv
from pathlib import Path
from typing import Union, Dict, List
import undetected_chromedriver as uc
from undetected_chromedriver import find_chrome_executable

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.shadowroot import ShadowRoot

class CopilotClient():
   
    def __init__(self, url: str, client_name: str, logged_in: bool = False, headless: bool = True, tag: str = None, user_data_dir: str = None, auto_save: bool = False, save_path: str = None, timeout_dur: int = 40, uc_params: dict = None, driver_arguments: Union[List, Dict] = None, wait_time: int = 40, driver_version: int = None): #, verbose: bool = False):
        """
        # Create a new of the logger
        r_level = logging.getLogger().getEffectiveLevel()

        self.logger = logging.getLogger(tag or client_name)
        self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        # If verbose is provided and the current log level is higher
        # than info, it will decrease logging level.
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        """
        self.url = url
        self.client_name = client_name
        self.browser = None
        self.logged_in = logged_in
        self.headless = headless
        self.tag = tag
        self.wait_object = None 
        self.wait_time = wait_time
        self.user_data_dir = user_data_dir
        self.uc_params = uc_params
        self.driver_arguments = driver_arguments
        #self.incognito = incognito
        self.driver_version = driver_version
        self.save_path = save_path
        self.auto_save = auto_save
        self.timeout_dur = timeout_dur


    def launch_browser(self):
        #uc_params = self.uc_params or {}
        chrome_path = r'C:\Power Bi\Ships\Files\chatgpt_selenium_automation\talkingheads-0.5.2\Copilot\src\Chrome\Application\chrome.exe'
#find_chrome_executable()
        if not chrome_path:
            raise ValueError('unable to find chrome path')

      
        options = uc.ChromeOptions()
        options.binary_location = chrome_path
        options.headless = self.headless 


        browser_arguments = {

            #headless flags
            "disable-blink-features": "AutomationControlled",
            "disable-dev-shm-usage": True,
            "no-sandbox": True,
            "disable-infobars": True,

            #browser mimicing
            "enable-gpu": True,
            "window-size": "1920,1080",
            "start-maximized": True,
            "disable-extensions": True,
            "disable-software-rasterizer": True,

            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.100 Safari/537.36",

            "disable-features": "ChromeDetection,OutOfBlinkColors"

            }

        if self.user_data_dir:
            options.add_argument(f"--user_data_dir={self.user_data_dir}")

        if self.driver_arguments:
            if isinstance(self.driver_arguments, dict):
                driver_arguments = {**browser_arguments,  **self.driver_arguments}              
            else: 
                driver_arguments = browser_arguments
        else:
            driver_arguments = browser_arguments

        driver_arguments = list(map(
            lambda kv: f"--{kv[0]}" + ("" if kv[1] is True else f"={kv[1]}"),
            driver_arguments.items()
        ))

        _ = list(map(options.add_argument,driver_arguments))
               

        self.browser = uc.Chrome(
            #user_data_dir=self.user_data_dir,
            options=options,
            headless=self.headless,
            #version_main=self.detect_chrome_version(self.driver_version),
            #**uc_params,
        )


        #self.browser = webdriver.Chrome(options=options)
        #self.logger.info(f'launching browser for {self.client_name}...')
        self.browser.set_page_load_timeout(self.wait_time)
        self.wait_object = WebDriverWait(self.browser, self.wait_time)
        self.browser.get(self.url)
        self.logged_in = False
        #self.browser.maximize_window()
        self.chat_history = pd.DataFrame(columns=["role", "is_regen", "content"]) 
        self.set_save_path(self.save_path)       

        time.sleep(5)


    def login(self, shadow_element, username: str = None, password: str = None):
        
        try:
            accept = self.find_or_fail(By.CSS_SELECTOR, "button[title='Accept']", dom_element=shadow_element)
            if accept:
                accept.click()
                time.sleep(2)
            else:
                print('no cookies')
           
            username = 'miikka.karava@gmail.com'
            password = 'tvJ6w/1d8TW4=x6'


            log_in = self.find_or_fail(By.ID, ':ra:', dom_element=shadow_element)
            # (By.XPATH, "//input[@value='sign in']")
            if log_in:
                log_in.click()
                time.sleep(2)
            else:
                print('proceed loggin in')

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

            next = self.find_or_fail(By.ID, 'iNext', dom_element=shadow_element)
            if next:
                next.click()             
                time.sleep(2)
            else:
                print('no next button')

            time.sleep(5)
            accept = self.find_or_fail(By.ID, 'acceptButton', dom_element=shadow_element)
            if accept:
                accept.click()             
                time.sleep(2)
            else:
                print('no accept button')
  
            time.sleep(5)

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
           
            get_response = self.interact(shadow_element, prompt_queue)

            if get_response:
                if "I'm sorry" in get_response:  
                    return False    
 
                else:
                    return True

        except Exception as e:
            print(f'exception processing: {str(e)}')
            time.sleep(5)

        return False

    def pilot_message(self, shadow_element, prompt_queue: str):

        description = self.interact(shadow_element, prompt_queue)         

        if description:
            print(description)
            return description
        else:
            return False

      

    def is_ready_to_prompt(self, shadow_element, text_area) -> bool:
        """
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

        wait = 20       

        #wait.until(EC.element_to_be_clickable(button))
        time.sleep(20)
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
        try:
            get_response = self.browser.find_elements(By.CSS_SELECTOR, "div[class='space-y-3 break-words']")
            if get_response:
 
                text_response = get_response[-1]
                print(text_response)
            #text = text_response.replace('\r', ' ').strip()
                text = text_response.text
            else:      
                print("No response")

            print(text)
            return text

            #text = re.sub(r'\d+\s*', '', text)
            #text = re.sub(r'\s+\.', '', text)

        #text = re.sub(r'^\s*$', '', text, flags=re.MULTILINE)

        except Exception as e:
            print('get_response exception: {str(e)}')
            return False         



    def interact(self, shadow_element, prompt_queue: str, image_path: Union[str, Path] = None) -> str:

        text_area = self.find_or_fail(By.CSS_SELECTOR, "textarea[id='userInput']", dom_element=shadow_element)

        if not text_area:
            print("Unable to locate text area, interaction fails.")
            #self.logger.error("Unable to locate text area, interaction fails.")
            return ""

        for each_line in prompt_queue.split("\n"):
            text_area.send_keys(each_line)
            text_area.send_keys(Keys.SHIFT + Keys.ENTER)

        # Click enter and send the message
        text_area.send_keys(Keys.ENTER)

        if not self.is_ready_to_prompt(shadow_element, text_area):
            print("Cannot retrieve the response, something is wrong")
            self.logger.info("Cannot retrieve the response, something is wrong")
            return ""
        try:
            text = self.get_last_response()
            print(f"response is ready: {text}")
        #self.logger.info("response is ready")
            self.log_chat(prompt=prompt_queue, response=text)
            return text

        except Exception as e:
            print('interact exception: {str(e)}')
            return False


    def set_save_path(self, save_path: str):
        """Sets the path to save the file

        Args:
            save_path (str): The saving path
        """
        self.save_path = save_path or datetime.now().strftime(f"{self.tag}_%Y_%m_%d_%H_%M_%S.csv")
        self.file_type = save_path.split(".")[-1] if save_path else "csv"


    def save(self) -> bool:
        """Saves the conversation."""
        save_func = self.save_func_map.get(self.file_type, None)
        if save_func:
            save_func = getattr(self.chat_history, save_func)
            save_func(self.save_path)
            self.logger.info("File saved to %s", self.save_path)
            return True

        self.logger.error("Unsupported file type %s", self.file_type)
        return False


    def find_or_fail(
        self,
        by: By,
        elem_query: str,
        return_type: str = "first",
        return_shadow: bool = False,
        fail_ok: bool = False,
        dom_element: WebElement = None,
    ):
        """Finds a list of elements given elem_query, if none of the items exists, throws an error

        Args:
            by (selenium.webdriver.common.by.By): The method used to locate the element.
            elem_query (str): The elem_query string to locate the element.
            return_type (str): first|all|last. Return first element, all elements or the last one.
            fail_ok (bool): Do not produce error if it is ok to fail.
            dom_element (WebElement): If set, finds within that element.
        Returns:
            WebElement: Web element or None if not found.
        """

        if return_type not in {"first", "last", "all"}:
            return ValueError("Unrecognized return type")

        if dom_element is None:
            dom_element = self.browser.find_elements(by, elem_query)
        else:
            dom_element = dom_element.find_elements(by, elem_query)

        if not dom_element:
            if not fail_ok:
                print(f"%s is not located. Please raise an issue with verbose=True {elem_query}")
                """
                self.logger.error(
                    " %s is not located. Please raise an issue with verbose=True", elem_query
                )
                """
            else:
                print(f'%s is not located. {elem_query}')
                #self.logger.info(" %s is not located.", elem_query)
            return None
        print(f'%s is located. {elem_query}')
        #self.logger.info(" %s is located.", elem_query)

        element = {
            "first": lambda x: x[0],
            "all": lambda x: x,
            "last": lambda x: x[-1],
        }[return_type](dom_element)

        if return_shadow:
            return element.shadow_root
        return element


    def detect_chrome_version(self, version_num: int = None) -> Union[int, None]:
        """
        Detects the Google Chrome version on Linux and macOS machines.

        Args
            version_num (int, optional): The chromedriver version number. Default: None.

        Returns:
            int: The detected Google Chrome version number.

        Note:
        - If version_num is provided, it will be returned without any detection.

        - Uses subprocess to execute the 'google-chrome --version' command for detection.

        - If the command output doesn't match the expected format, it returns None.

        - Logs information about the detected or default version using the logging module.
        """

        if version_num:
            logging.debug("Version number is provided: %d", version_num)
            return version_num

        chrome_path = r'C:\Power Bi\Ships\Files\chatgpt_selenium_automation\talkingheads-0.5.2\Copilot\src\Chrome\Application\chrome.exe'

#find_chrome_executable()

        out = subprocess.check_output([chrome_path, "--version"])
        out = re.search(r"Google\s+Chrome\s+(\d{3})", out.decode())

        if not out:
            logging.error("There was an error obtaining Chrome version")
            return None

        version_num = int(out.group(1))
        logging.info("The version is %d", version_num)
        return version_num


    def log_chat(
        self, prompt: str = None, response: str = None, regenerated: bool = False
    ) -> bool:
        """
        Log a chat interaction in the chat history.

        Args:
            prompt (str): The user's prompt to be logged.
            response (str): The response to the user's prompt to be logged.

        Returns:
            bool: True if the interaction is logged, False otherwise.
        """
        if not self.auto_save:
            return False

        if prompt:
            self.chat_history.loc[len(self.chat_history)] = [
                "user",
                regenerated,
                prompt,
            ]

        if response:
            self.chat_history.loc[len(self.chat_history)] = [
                self.client_name,
                regenerated,
                response,
            ]
        return True


    save_func_map = {
        "csv": "to_csv",
        "h5": "to_hdf",
        "html": "to_html",
        "json": "to_json",
        "orc": "to_orc",
        "pkl": "to_pkl",
        "xlsx": "to_xlsx",
        "xml": "to_xml",
    }

