"""Configuration loader supporting .env, environment variables, and legacy config.txt."""

import os
from typing import Dict, Optional


def load_config(
    config_file: str = "config.txt",
    env_file: str = ".env"
) -> Dict[str, str]:
    """Loads settings from environment variables, .env, or config.txt.

    Priority:
    1. OS Environment Variables (NDHU_USERNAME, NDHU_PASSWORD, LOGIN_URL)
    2. .env file
    3. config.txt (legacy format)
    """
    config: Dict[str, str] = {
        "LOGIN_URL": "https://sys.ndhu.edu.tw/aa/class/subjselect/course_sele.aspx",
        "USERNAME": "",
        "PASSWORD": "",
        "RUSH_DELAY": "0.05",
        "QUERY_DELAY": "0.15",
    }

    # 1. Try legacy config.txt if present
    if os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        key, value = line.split("=", 1)
                        config[key.strip()] = value.strip()
        except Exception:
            pass

    # 2. Try .env file if present
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        key, value = line.split("=", 1)
                        k = key.strip()
                        v = value.strip().strip('"').strip("'")
                        if k in ("NDHU_USERNAME", "USERNAME"):
                            config["USERNAME"] = v
                        elif k in ("NDHU_PASSWORD", "PASSWORD"):
                            config["PASSWORD"] = v
                        elif k == "LOGIN_URL":
                            config["LOGIN_URL"] = v
                        elif k in ("RUSH_DELAY", "QUERY_DELAY"):
                            config[k] = v
        except Exception:
            pass

    # 3. Environment variables take precedence
    if os.environ.get("NDHU_USERNAME"):
        config["USERNAME"] = os.environ["NDHU_USERNAME"]
    elif os.environ.get("USERNAME") and not config["USERNAME"]:
        config["USERNAME"] = os.environ["USERNAME"]

    if os.environ.get("NDHU_PASSWORD"):
        config["PASSWORD"] = os.environ["NDHU_PASSWORD"]
    elif os.environ.get("PASSWORD") and not config["PASSWORD"]:
        config["PASSWORD"] = os.environ["PASSWORD"]

    if os.environ.get("LOGIN_URL"):
        config["LOGIN_URL"] = os.environ["LOGIN_URL"]

    if os.environ.get("RUSH_DELAY"):
        config["RUSH_DELAY"] = os.environ["RUSH_DELAY"]

    return config
