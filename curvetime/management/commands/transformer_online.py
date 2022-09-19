from django.core.management import BaseCommand
import logging, time
import requests
from curvetime.oracle.stocks import *
from curvetime.env.online_stock import *
from curvetime.ai.transformer import *
from curvetime.ai.transformer_agent import *
from curvetime.bc.blockchain import *


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        try:
            o = StockOracle()
            env = StockEnv(o)
            model = Transformer(env, filepath='data/models/transformer.h5')
            target_model = Transformer(env, filepath='data/models/target_transformer.h5')
            agent = Agent(model, target_model, env, gamma=0.6, epsilon=0.3, epsilon_min=0.2, update_target_network=100)
            while True:
                agent.step()
        except Exception as e:
            logger.error(e)


def main():
    o = StockOracle()
    env = StockEnv(o)
    model = Transformer(env, filepath='data/models/transformer.h5')
    target_model = Transformer(env, filepath='data/models/target_transformer.h5')
    agent = Agent(model, target_model, env, gamma=0.6, epsilon=0.4, epsilon_min=0.2, update_target_network=100)
    while True:
        agent.step()


if __name__ == '__main__':
    main()
