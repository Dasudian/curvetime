from django.core.management import BaseCommand
import logging, time
import requests
from curvetime.oracle.stocks import *
from curvetime.env.online_stock import *
from curvetime.ai.ac_nasnet import *
from curvetime.ai.ac_nasnet_agent import *
from curvetime.bc.blockchain import *


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        try:
            o = StockOracle()
            env = StockEnv(o)
            model = NasNet(env, filepath='data/models/ac_nasnet.h5')
            agent = Agent(model, env)
            while True:
                agent.step()
        except Exception as e:
            logger.error(e)


def main():
    o = StockOracle()
    env = StockEnv(o)
    model = NasNet(env, filepath='data/models/ac_nasnet.h5')
    agent = Agent(model, env)
    while True:
        a, r, f = agent.step()
        if f:
            break


if __name__ == '__main__':
    main()
