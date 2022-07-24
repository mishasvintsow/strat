import logging
import os
import time
from datetime import timedelta

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strat.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from django.utils import timezone

from connect import connect

from main.models import Symbol
from process_data import update_5minutes

logger = logging.getLogger(__name__)


def cron_5minutes():
    client = connect()
    logger.warning(client.ping())
    for symbol in Symbol.objects.all():
        update_5minutes(symbol)
    return True


if __name__ == '__main__':
    cron_5minutes()
