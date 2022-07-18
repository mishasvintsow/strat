import logging
import os
import sys
import time
from datetime import timedelta

import django
from django.utils import timezone

from connect import connect
from load_data import update_symbol_klines

from main.models import Coin, Symbol
from process_data import update_pnl

logger = logging.getLogger(__name__)

sys.path.insert(0, '../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strat.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()


def test():
    time_start = timezone.now()
    client = connect()
    logger.warning(client.ping())
    for symbol in Symbol.objects.all().order_by('last_update'):
        if (timezone.now()-time_start).total_seconds() < 58:
            logger.warning(str(symbol))
            update_symbol_klines(client,
                                 symbol,
                                 timezone.now()-timedelta(minutes=10),
                                 timezone.now())
            update_pnl(symbol)
            logger.warning("continue task...")
            time.sleep(1)
        else:
            logger.warning("finish task")
            break
    return True
