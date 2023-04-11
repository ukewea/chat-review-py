import logging

logger = logging.getLogger("chat-review")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(name)s] %(message)s"))
logger.addHandler(handler)
