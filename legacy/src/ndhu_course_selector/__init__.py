"""NDHU Course Selector - 東華大學自動選課與預排檢視系統."""

__version__ = "1.0.0"
__author__ = "NDHU Course Selector Team"

from ndhu_course_selector.tools.config import load_config
from ndhu_course_selector.core.browser import create_browser_session
from ndhu_course_selector.core.auth import perform_login
from ndhu_course_selector.core.parser import query_and_parse_courses
from ndhu_course_selector.core.selector import execute_course_selection

__all__ = [
    "load_config",
    "create_browser_session",
    "perform_login",
    "query_and_parse_courses",
    "execute_course_selection",
]
