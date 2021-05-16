from django.core.management import BaseCommand
import logging, time
import requests
from curvetime.bc.node import *


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        try:
            count = 1
            while True:
                tx = {'count': count,
                      'timestamp': time.time()}
                blockchain.add_new_transaction(tx)
                sync_mine()
        except Exception as e:
            logger.error(e)

