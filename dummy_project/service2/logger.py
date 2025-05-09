from loguru import logger

# Configure logger to write to a file
logger.add("logs/s2.log", rotation="1 MB", retention="7 days", compression="zip")

logger.info("This is an info message.")
logger.error("This is an error message.")