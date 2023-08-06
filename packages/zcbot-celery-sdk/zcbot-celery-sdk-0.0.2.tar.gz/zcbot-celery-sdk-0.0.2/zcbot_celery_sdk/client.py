# -*- coding: utf-8 -*-
import logging
from typing import Callable, Dict, List, Union
from celery import Celery, Task
from celery.result import AsyncResult
from redis import Redis

from exceptions import BizException
from .callback import Callback
from .keys import get_result_key

LOGGER = logging.getLogger(__name__)


class CeleryClient(object):

    def __init__(self, celery_broker_url: str, celery_result_backend: str, client_redis_uri: str, app_code: str):
        self.broker_url = celery_broker_url
        self.backend_uri = celery_result_backend
        self.client_redis_uri = client_redis_uri
        self.app_code = app_code
        self.default_expire_seconds = 12 * 3600
        self.celery_client = Celery(
            'zcbot-service',
            broker=self.broker_url,
            backend=self.backend_uri,
            task_acks_late=True
        )
        self.rds_client = Redis.from_url(url=client_redis_uri, decode_responses=True)
        self.task_map = dict()

    # 异步结果处理函数绑定
    def bind_callback(self, task_name: str, async_result: AsyncResult, callback_func: Callable = None, callback_data: dict = None):
        rs_key = get_result_key(app_code=self.app_code, task_name=task_name, task_id=async_result.id)
        callback = Callback(callback_func, callback_data)
        self.rds_client.set(rs_key, callback.as_json(), ex=self.default_expire_seconds)

    # 异步请求
    def apply_async(self, task_name: str, args: list = None, callback_func: Callable = None, callback_data: dict = None):
        LOGGER.info(f'[服务]异步调用 task={task_name}')
        task = self.task_map.get(task_name)
        if not task:
            task = Task()
            task.bind(self.celery_client)
            task.name = task_name
            self.task_map[task_name] = task
        _args = args or []
        if not isinstance(_args, list):
            _args = [_args]
        try:
            async_result = task.apply_async(_args)
            self.bind_callback(task_name, async_result, callback_func, callback_data)
        except Exception as e:
            LOGGER.error(f'处理异常：task_name={task_name}, args={args}, callback={callback_data}, e={e}')
            raise e

    # 同步请求
    def sync_get(self, task_name: str, args: list = None, timeout: float = None):
        LOGGER.info(f'[服务]同步调用 task={task_name}')
        task = self.task_map.get(task_name)
        if not task:
            task = Task()
            task.bind(self.celery_client)
            task.name = task_name
            self.task_map[task_name] = task
        _args = args or []
        if not isinstance(_args, list):
            _args = [_args]
        try:
            async_result = task.apply_async(_args)
            return async_result.get(timeout=timeout)
        except Exception as e:
            LOGGER.error(f'处理异常：task_name={task_name}, args={args}, e={e}')
            raise e

    def call(self, task_name: str, args: Union[List, Dict], is_async: bool = True, callback_func: Callable = None, callback_data: dict = None) -> dict:
        """
        兼容方式请求调用
        """
        _args = [args]
        if is_async:
            # 异步
            if not callback_func:
                raise BizException(f'异步调用必须指定回调方法 task_name={task_name}, is_sync={is_async}')
            result = self.apply_async(task_name=task_name, args=_args, callback_func=callback_func, callback_data=callback_data)
        else:
            # 同步
            result = self.sync_get(task_name=task_name, args=_args)

        return result


class CeleryApi(CeleryClient):

    def get_tax_by_baiwang(self, args: list = None, callback_func: Callable = None, callback_data: dict = None):
        return self.apply_async('tax.demo', args, callback_func, callback_data)

    def search_same_sku(self, keyword: str = None, platform: str = None, page: int = 1) -> dict:
        args = [keyword, page]
        result = self.sync_get(task_name=f"same_sku.{platform}", args=args)

        return result

    def search_same_sku_jd(self, keyword: str, page: int = 1) -> dict:
        """
        京东pc端，搜同款接口
        """
        args = [keyword, page]
        result = self.sync_get(task_name=f"same_sku.jd_pc", args=args)

        return result

    def search_same_sku_sn(self, keyword: str, page: int = 1) -> dict:
        """
        苏宁pc端，搜同款接口
        """
        args = [keyword, page]
        result = self.sync_get(task_name=f"same_sku.sn_pc", args=args)

        return result

    def search_same_sku_mmbpc(self, keyword: str, page: int = 1) -> dict:
        """
        慢慢买pc端，搜同款接口
        """
        args = [keyword, page]
        result = self.sync_get(task_name=f"same_sku.mmb_pc", args=args)

        return result

    def search_same_sku_mmbm(self, keyword: str, page: int = 1) -> dict:
        """
        慢慢买手机端端，搜同款接口
        """
        args = [keyword, page]
        result = self.sync_get(task_name=f"same_sku.mmb_m", args=args)

        return result

    def sku_extract_by_chatgpt(self, item: Dict, is_async: bool = False, callback_func: Callable = None, callback_data: dict = None):
        """
        chatgpt 抽取信息
        """
        args = [item]
        result = self.call(task_name="sku_extract.chat_gpt", args=args, is_async=is_async, callback_func=callback_func, callback_data=callback_data)
        return result

    def batch_sku_extract_by_chatgpt(self, item_list: List[Dict], is_async: bool = False, callback_func: Callable = None, callback_data: dict = None):
        """
        chatgpt 批量抽取信息
        """
        args = [item_list]
        result = self.call(task_name="sku_extract.chat_gpt_batch", args=args, is_async=is_async, callback_func=callback_func, callback_data=callback_data)
        return result
