import logging
import sys

def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Optional: reduce noisy logs
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
