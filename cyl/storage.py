import json
import logging
import logging.handlers
from pathlib import Path

from pydantic import ValidationError

from .schema import Config

logger = logging.getLogger(__name__)

CONFIG_PATH = Path.home() / ".cyl" / "config.json"


def load_config() -> Config | None:
    if not CONFIG_PATH.exists():
        return None
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return Config.model_validate(data)
    except (json.JSONDecodeError, ValidationError, OSError) as e:
        logger.warning("config load failed: %s", e)
        return None


def save_config(config: Config) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(config.model_dump_json(), encoding="utf-8")
    logger.debug("config saved to %s", CONFIG_PATH)


def setup_logging() -> None:
    log_dir = Path.home() / ".cyl"
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        log_dir / "cyl.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[handler],
    )
