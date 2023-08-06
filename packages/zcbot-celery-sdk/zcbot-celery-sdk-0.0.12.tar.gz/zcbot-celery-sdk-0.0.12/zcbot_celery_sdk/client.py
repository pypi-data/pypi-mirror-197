# -*- coding: utf-8 -*-
import logging
from redis import Redis
from typing import Callable, Dict, Union, List
from celery import Celery, Task
from celery.result import AsyncResult
from .common.exceptions import BizException
from .common.utils import obj_to_ref, singleton
from .common.keys import get_result_key
from .common.model import Callback

LOGGER = logging.getLogger(__name__)


# @singleton
class CeleryClient(object):
    """
    Celery服务客户端
    注意：此类不建议手动初始化，可通过CeleryClientHolder初始化，方便各service类自动获取
    """

    def __init__(self, celery_broker_url: str, celery_result_backend: str, client_redis_uri: str, app_code: str):
        self.broker_url = celery_broker_url
        self.backend_uri = celery_result_backend
        self.client_redis_uri = client_redis_uri
        self.app_code = app_code
        self.default_expire_seconds = 12 * 3600
        self.celery_client = Celery(
            'zcbot-celery',
            broker=self.broker_url,
            backend=self.backend_uri,
            task_acks_late=True
        )
        self.rds_client = Redis.from_url(url=client_redis_uri, decode_responses=True)
        self.task_map = dict()

    # 异步结果处理函数绑定
    def _bind_callback(self, task_name: str, async_result: AsyncResult, callback: Callback):
        rs_key = get_result_key(app_code=self.app_code, task_name=task_name, task_id=async_result.id)
        self.rds_client.set(rs_key, callback.json(), ex=self.default_expire_seconds)

    def apply_async(self, task_name: str, task_params: Dict = None, callback: Callback = None, **kwargs):
        """
        异步请求
        :param task_name: 任务名
        :param task_params: 任务参数
        :param callback: 回调对象
        :param kwargs: 扩展参数
        :return:
        """
        LOGGER.info(f'[服务]异步调用 task={task_name}')
        try:
            _headers = dict()
            if callback:
                _headers.update(callback.dict())
            _headers['app_code'] = _headers.get('app_code', None) or self.app_code

            # 异步调用
            async_result = self._get_task(task_name).apply_async(kwargs=task_params, queue=f'task.{task_name}', headers=_headers)
            # 绑定回调处理函数
            self._bind_callback(task_name, async_result, callback)
            return async_result
        except Exception as e:
            LOGGER.error(f'处理异常: task_name={task_name}, kwargs={task_params}, callback={callback}, e={e}')
            raise e

    def apply_sync(self, task_name: str, task_params: Dict = None, **kwargs):
        """
        同步请求
        :param task_name: 任务名
        :param task_params: 任务参数
        :param kwargs: 扩展参数
        :return:
        """
        LOGGER.info(f'[服务]同步调用 task={task_name}')
        try:
            _headers = {'app_code': self.app_code}
            # 异步调用
            async_result = self._get_task(task_name).apply_async(kwargs=task_params, queue=f'task.{task_name}', headers=_headers)
            # 等待结果
            _timeout = 60
            if kwargs and kwargs.get('timeout', None):
                _timeout = float(kwargs.get('timeout'))
            rs = async_result.get(timeout=_timeout)
            async_result.forget()
            return rs
        except Exception as e:
            LOGGER.error(f'处理异常: task_name={task_name}, kwargs={task_params}, e={e}')
            raise e

    # 兼容方式请求调用
    def apply(self, task_name: str, task_params: Dict = None, callback: Callback = None, **kwargs):
        """
        兼容方式请求调用
        有callback怎为异步
        """
        if callback:
            # 异步
            return self.apply_async(task_name=task_name, task_params=task_params, callback=callback)
        else:
            # 同步
            return self.apply_sync(task_name=task_name, task_params=task_params, **kwargs)

    # 缓存Celery任务对象
    def _get_task(self, task_name: str):
        task = self.task_map.get(task_name)
        if not task:
            task = Task()
            task.bind(self.celery_client)
            task.name = task_name
            self.task_map[task_name] = task

        return task

    # 构建回调对象
    def build_callback(self, callback_func: Union[str, Callable] = None, callback_data: Union[str, Dict, List] = None, app_code: str = None, tenant_code: str = None):
        callback = Callback()
        callback.app_code = app_code or self.app_code
        callback.tenant_code = tenant_code or None
        callback.callback_data = callback_data or None
        if isinstance(callback_func, str):
            callback.callback_func = callback_func
        else:
            callback.callback_func = obj_to_ref(callback_func)

        return callback


class CeleryClientHolder(object):
    __default_instance = None

    @staticmethod
    def init_default_instance(celery_broker_url: str, celery_result_backend: str, client_redis_uri: str, app_code: str):
        CeleryClientHolder.__default_instance = CeleryClient(celery_broker_url, celery_result_backend, client_redis_uri, app_code)

    @staticmethod
    def default_instance():
        if not CeleryClientHolder.__default_instance:
            raise BizException(f'默认实例尚未初始化，请先初始化实例！')
        return CeleryClientHolder.__default_instance
