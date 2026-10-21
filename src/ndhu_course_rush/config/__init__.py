"""Configuration layer (only layer allowed to read environment variables) and logging setup."""

from ndhu_course_rush.config.legacy_config import load_config as load_legacy_config
from ndhu_course_rush.config.logging_setup import setup_logging
from ndhu_course_rush.config.settings import AppConfig, load_config

__all__ = [
    "AppConfig",
    "load_config",
    "load_legacy_config",
    "setup_logging",
]
