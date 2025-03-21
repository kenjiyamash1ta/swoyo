import logging
from pathlib import Path


log_path = Path(__file__).resolve().parent.parent / "log"

logging.basicConfig(
    filename=log_path / "app.log",
    level="INFO",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
