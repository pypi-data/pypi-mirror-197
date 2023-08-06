from typing import Dict
from ..client import CeleryClient
from ..common.model import Callback


class TaxService(object):

    def __init__(self, celery_client: CeleryClient):
        self.celery_client = celery_client

    def get_tax_by_baiwang(self, params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='tax.baiwang', task_params=params, callback=callback, **kwargs)

    def get_tax_by_demo(self, params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='tax.demo', task_params=params, callback=callback, **kwargs)
