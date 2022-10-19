from django.core.management import BaseCommand
from curvetime.oracle.cn_debts import fetch_price

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            print("----Start fetcing real-time data of Chinese Debts Market----")
            fetch_price(3)
        except Exception as e:
            logger.error(e)

if __name__ == '__main__':
    main()

def main():
    print("----Start fetcing real-time data of Chinese Debts Market----")
    fetch_price(3)
