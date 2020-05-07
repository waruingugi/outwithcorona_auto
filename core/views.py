from django.shortcuts import render
from django.http import HttpRequest
from django.core.cache import cache
from core.tasks import get_latest_stat_for_kenya
import json

# Initiate logging
import logging
import core.core_logger # noqa
# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
    """ Handles the home page"""
    assert isinstance(request, HttpRequest)
    logger.info('Rendering home page.')

    data = cache.get('latest_data', None)
    if data is None:
        logger.error('Cached data does not exist')
        get_latest_stat_for_kenya()

    latest_data = cache.get('latest_data')

    cases = latest_data['cases']
    deaths = latest_data['deaths']
    tests = latest_data['tests']

    return render(
        request,
        'core/home.html',
        {
            'title': 'Results',
            'cases': cases,
            'deaths': deaths,
            'tests': tests
        }
    )
