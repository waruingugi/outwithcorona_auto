import requests
from celery import shared_task
from retry import retry
import requests
from outwithcorona.settings import ENDPOINT_URL
from django.core.cache import cache

# Initiate logging
import logging
import core.core_logger # noqa
# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


@shared_task(name='get_latest_stat_for_kenya')
@retry((Exception), delay=10, backoff=3, max_delay=10)
def get_latest_stat_for_kenya():
    """Function to call rapidapi.com endpoint"""
    logger.info('Executing get_latest_stat_for_kenya shared task')

    url = ENDPOINT_URL
    querystring = {"country":"Kenya"}

    headers = {
        'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
        'x-rapidapi-key': "d901edfb17msh4441a5911a1f674p1994adjsn8397300b588f"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    logger.info(response.text)
    item = cache.get('latest_data', None)
    if item is not None:
        cache.delete('latest_data') # Delete cached data if it exists

    cache.set(
        'latest_data', response.json()['latest_stat_by_country'][0], None
    ) # Cache forever/until another update.
