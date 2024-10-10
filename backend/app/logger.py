import logging
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

def setup_logger(name: str = "app"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, f"{name}.log")),
            logging.StreamHandler()  # Log to console
        ]
    )
    logger = logging.getLogger(name)
    return logger
