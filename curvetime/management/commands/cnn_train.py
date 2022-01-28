from django.core.management import BaseCommand
import logging, time
import requests
from curvetime.oracle.stocks import *
from curvetime.env.stock_env import *
from curvetime.ai.cnn import *
from curvetime.ai.cnn_agent import *
from curvetime.bc.blockchain import *


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        try:
            o = StockOracle()
            env = StockEnv(o)
            model = CNN(env, filepath='data/models/model.h5')
            target_model = CNN(env, filepath='data/models/target_model.h5')
            agent = Agent(model, target_model, env)
            while True:
                agent.step()
        except Exception as e:
            logger.error(e)

