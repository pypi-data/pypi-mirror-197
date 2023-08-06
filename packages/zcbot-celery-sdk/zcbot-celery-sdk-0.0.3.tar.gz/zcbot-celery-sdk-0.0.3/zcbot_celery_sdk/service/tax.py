from typing import Callable, Dict, Union, List
from ..client import CeleryClient
from ..common.model import Callback


class TaxService(object):

    def __init__(self, celery_client: CeleryClient):
        self.celery_client = celery_client

    def get_tax_by_baiwang(self, kwargs: Dict = None, callback: Callback = None, callback_func: Union[str, Callable] = None, callback_data: Union[str, Dict, List] = None, app_code: str = None, tenant_code: str = None):
        _callback = callback or self.celery_client.build_callback(callback_func, callback_data, app_code, tenant_code)

        return self.celery_client.apply_async(task_name='tax.demo', kwargs=kwargs, callback=_callback)
