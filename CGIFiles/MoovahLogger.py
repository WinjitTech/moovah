import logging

logger = logging.getLogger("Schedular")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/home/pi/Schedular.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

