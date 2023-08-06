from typing import Any, Dict

import requests

from knapsack.api import Api
from knapsack.knapsack_dataset import KnapsackDataset

def post(
    endpoint: str,
    info: Dict[str, Any] = None,
    **kwargs
) -> None:
    json = dict(kwargs)
    json['info'] = info
    api = Api()
    result = requests.post(api.get_base_url() + "/" + endpoint, json=json)
    return result
