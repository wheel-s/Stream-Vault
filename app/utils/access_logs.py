import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


logger = logging.getLogger("file_access_app")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(f"logs/access.log", maxBytes = 10_000_000, backupCount=5)
formater = logging.Formatter("%(asctime)s | %(levevlname)s | %(message)s")
#handler.setFormatter(formater)
logger.addHandler(handler)



def log_access(user_id, user_name, file_name, size, status):
   logger.info(
       f" user_id={user_id} {user_name} | streamed | filename={file_name} | "
       f"size={size} bytes, | status={status} | at {datetime.now()}"
   )


