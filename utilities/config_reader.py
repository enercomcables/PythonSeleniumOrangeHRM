
import os
from pathlib import Path

import yaml


ROOT_DIR = Path(__file__).resolve().parents[1]


def load_config():
    config_path = ROOT_DIR / "config" / "config.yaml"

    with config_path.open(encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    # Environment variables override YAML values.
    config["base_url"] = os.getenv(
        "BASE_URL", config.get("base_url", "")
    )
    config["browser"] = os.getenv(
        "BROWSER", config.get("browser", "chrome")
    ).lower()
    config["headless"] = os.getenv(
        "HEADLESS", str(config.get("headless", False))
    ).lower() in ("true", "1", "yes")
    config["timeout"] = int(
        os.getenv("TIMEOUT", config.get("timeout", 10))
    )
    config["page_load_timeout"] = int(
        config.get("page_load_timeout", 30)
    )

    return config


def get_project_root():
    return ROOT_DIR
