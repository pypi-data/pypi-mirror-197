from typing import Dict
from ..client import CeleryClient
from ..common.model import Callback


class SkuSearchService(object):
    """
    商品搜索服务
    """

    def __init__(self, celery_client: CeleryClient):
        self.celery_client = celery_client

    def search(self, platform: str = None, params: Dict = None, callback: Callback = None, **kwargs):
        return self.celery_client.apply(task_name=f'sku_search.{platform}', task_params=params, callback=callback, **kwargs)

    def search_jd_pc(self, params: Dict = None, callback: Callback = None, **kwargs):
        """
        【商品搜索】京东PC端
        """
        return self.celery_client.apply(task_name='sku_search.jd_pc', task_params=params, callback=callback, **kwargs)

    def search_sn_pc(self, params: Dict = None, callback: Callback = None, **kwargs):
        """
        【商品搜索】苏宁PC端
        """
        return self.celery_client.apply(task_name='sku_search.sn_pc', task_params=params, callback=callback, **kwargs)

    def search_mmb_pc(self, params: Dict = None, callback: Callback = None, **kwargs):
        """
        【商品搜索】慢慢买PC端
        """
        return self.celery_client.apply(task_name='sku_search.mmb_pc', task_params=params, callback=callback, **kwargs)

    def search_mmb_m(self, params: Dict = None, callback: Callback = None, **kwargs):
        """
        【商品搜索】慢慢买手机端
        """
        return self.celery_client.apply(task_name='sku_search.mmb_m', task_params=params, callback=callback, **kwargs)
