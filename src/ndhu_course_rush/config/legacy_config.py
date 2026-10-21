"""Configuration loader supporting .env, environment variables, and legacy config.txt."""

from __future__ import annotations

import os
from pathlib import Path


def _parse_key_value_file(path_str: str) -> dict[str, str]:
    """Parse key=value pairs from a text or dotenv file.

    Args:
        path_str: Path to file.

    Returns:
        Mapping of parsed key-value pairs.
    """
    path = Path(path_str)
    if not path.is_file():
        return {}
    results: dict[str, str] = {}
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if "=" in stripped and not stripped.startswith("#"):
                key, _, value = stripped.partition("=")
                results[key.strip()] = value.strip().strip("\"'")
    except Exception:
        return {}
    return results


def _apply_env_overrides(config: dict[str, str]) -> None:
    """Override configuration values with environment variables.

    Args:
        config: Configuration dictionary to update in-place.
    """
    env_username = os.environ.get("NDHU_USERNAME") or os.environ.get("USERNAME")
    if env_username:
        config["USERNAME"] = env_username
    env_password = os.environ.get("NDHU_PASSWORD") or os.environ.get("PASSWORD")
    if env_password:
        config["PASSWORD"] = env_password
    if os.environ.get("LOGIN_URL"):
        config["LOGIN_URL"] = os.environ["LOGIN_URL"]
    if os.environ.get("RUSH_DELAY"):
        config["RUSH_DELAY"] = os.environ["RUSH_DELAY"]
    if os.environ.get("QUERY_DELAY"):
        config["QUERY_DELAY"] = os.environ["QUERY_DELAY"]


def load_config(
    config_file: str = "config.txt",
    env_file: str = ".env",
) -> dict[str, str]:
    """Load settings from environment variables, .env, or config.txt.

    Priority:
    1. OS Environment Variables (NDHU_USERNAME, NDHU_PASSWORD, LOGIN_URL)
    2. .env file
    3. config.txt (legacy format)

    Args:
        config_file: Path to legacy configuration text file.
        env_file: Path to dotenv configuration file.

    Returns:
        Dictionary containing configuration key-value mappings.
    """
    config: dict[str, str] = {
        "LOGIN_URL": "https://sys.ndhu.edu.tw/aa/class/subjselect/course_sele.aspx",
        "USERNAME": "",
        "PASSWORD": "",
        "RUSH_DELAY": "0.05",
        "QUERY_DELAY": "0.15",
    }
    # 1. Try legacy config.txt
    config.update(_parse_key_value_file(config_file))
    # 2. Try .env file
    env_pairs = _parse_key_value_file(env_file)
    for k, v in env_pairs.items():
        if k in ("NDHU_USERNAME", "USERNAME"):
            config["USERNAME"] = v
        elif k in ("NDHU_PASSWORD", "PASSWORD"):
            config["PASSWORD"] = v
        elif k in ("LOGIN_URL", "RUSH_DELAY", "QUERY_DELAY"):
            config[k] = v
    # 3. Environment variables take precedence
    _apply_env_overrides(config)
    return config
