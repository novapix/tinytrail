import logging
from pathlib import Path

log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)


def setup_logger(name: str = "app") -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / f"{name}.log"),
            logging.StreamHandler(),  # Log to console
        ],
    )
    return logging.getLogger(name)


logger = setup_logger("tinytrail")