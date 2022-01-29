from django.core.management import BaseCommand
import logging, time
import requests
from curvetime.oracle.stocks import *
from curvetime.env.stock_env import *
from curvetime.ai.nasnet import *
from curvetime.ai.nasnet_agent import *
from curvetime.bc.blockchain import *


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        try:
            o = StockOracle()
            env = StockEnv(o)
            model = NasNet(env, filepath='data/models/nasnet.h5')
            target_model = NasNet(env, filepath='data/models/target_nasnet.h5')
            agent = Agent(model, target_model, env)
            while True:
                agent.step()
        except Exception as e:
            logger.error(e)

