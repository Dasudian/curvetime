import json
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from curvetime.db import couch
from curvetime.utils.utils import util_response
from app.settings import CONNECTED_NODE_ADDRESS



class Test(APIView):
    def get(self, request):
        subprocess.run(["git", "pull", "origin", "dev"])
        return Response("test", status=status.HTTP_200_OK)



class Transaction(APIView):
    def get(self, request):
        """
        Function to fetch the chain from a blockchain node, parse the
        data and store it locally.
        """
        hash = request.GET.get('hash')
        node = random.choice(CONNECTED_NODE_ADDRESS)
        node = "{}/node/transaction?hash={}".format(node, hash)
        response = requests.get(node)
        if response.status_code == 200:
            content = response.json()
            return util_response(content)
        else:
            return util_response(code=response.status_code)



    def post(self, request):
        """
        Endpoint to create a new transaction.
        """
        data = request.data
        node = random.choice(CONNECTED_NODE_ADDRESS)
        # Submit a transaction
        new_tx_address = "{}/node/transaction".format(node)
        res = requests.post(new_tx_address,
                  json=data,
                  headers={'Content-type': 'application/json'})

        if res.status_code == 200:
            return util_response(res.json())
        else:
            return util_response(code=res.status_code)
