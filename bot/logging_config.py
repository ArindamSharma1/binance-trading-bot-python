import sys
from pathlib import Path
from loguru import logger

def setup_logging() -> None:
    """
    Configure Loguru with a two-level logging setup:
    1. Minimal, clean console output (INFO level).
    2. Verbose, rotating file output (DEBUG level).
    """
    # Remove default handler
    logger.remove()

    # 1. Console Handler (Minimal & Clean)
    logger.add(
        sys.stdout,
        format="<level>{message}</level>",
        level="INFO",
        colorize=True
    )

    # 2. File Handler (Verbose & Rotating)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "bot_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{level: <8}</level> | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip"
    )

# Initialize logging when the module is imported
setup_logging()
