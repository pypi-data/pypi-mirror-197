from typing import Dict

from .base import BaseService
from ..common.model import Callback


class TaxService(BaseService):

    def get_tax_by_baiwang(self, task_params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='tax.baiwang', task_params=task_params, callback=callback, **kwargs)

    def get_tax_by_demo(self, task_params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name='tax.demo', task_params=task_params, callback=callback, **kwargs)
