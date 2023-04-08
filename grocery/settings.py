import os
from ticketreader.settings import BASE_DIR

UPLOAD_PATH_TICKETS = os.path.join(
    BASE_DIR, "grocery", "static", "grocery", "ticket_tmp")
