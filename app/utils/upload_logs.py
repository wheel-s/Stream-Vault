import logging
from logging.handlers import RotatingFileHandler





logger = logging.getLogger("file_upload_app")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(f"logs/app.log", maxBytes = 10_000_000, backupCount=5)
formater = logging.Formatter("%(asctime)s | %(levevlname)s | %(message)s")
#handler.setFormatter(formater)
logger.addHandler(handler)


def log_upload(user_id, file_name, size, status):
   logger.info(
       f" user_id={user_id} | upload | filename={file_name} | "
       f"size={size} bytes, | status={status}"
   )


