"""Initialization file of talkingheads library"""
from .base_browser import BaseBrowser
from .utils import is_url, check_filetype, detect_chrome_version
from .model_library import CopilotClient

__all__ = [
    "is_url",
    "check_filetype",
    "detect_chrome_version",
    "BaseBrowser",
    "CopilotClient"

]
