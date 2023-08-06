# -*- coding: utf-8 -*-
import json
import logging
import threading
from threading import Thread
from celery import Celery
from celery.result import AsyncResult
from redis import Redis

from . import thread_pool
from .keys import get_result_key_filter, get_task_id_from_key
from .utils import ref_to_obj

LOGGER = logging.getLogger(__name__)


class CeleryRedisResultMonitor(object):

    def __init__(self, celery_broker_url: str, celery_result_backend: str, client_redis_uri: str, app_code: str):
        self.broker_url = celery_broker_url
        self.backend_uri = celery_result_backend
        self.client_redis_uri = client_redis_uri
        self.app_code = app_code

        self.celery_client = Celery(
            'zcbot-celery',
            broker=self.broker_url,
            backend=self.backend_uri,
            task_acks_late=True
        )
        self.rds_client = Redis.from_url(url=client_redis_uri, decode_responses=True)

    def start(self):
        LOGGER.info(f'启动结果监听...')
        Thread(target=self._watch, name='result-monitor').start()

    def _watch(self):
        # 当前：每个app一个结果监视器
        while True:
            filter_key = get_result_key_filter(app_code=self.app_code)
            keys = self.rds_client.keys(filter_key)
            LOGGER.debug(f'扫描[{threading.currentThread()}]: keys={len(keys)}')
            if keys:
                for key in keys:
                    task_id = get_task_id_from_key(key)
                    if task_id:
                        async_result = AsyncResult(id=task_id, app=self.celery_client)
                        if async_result.successful():
                            # 完成
                            result = async_result.get()
                            callback = json.loads(self.rds_client.get(key))
                            callback_func = callback.get('callback_func', None)
                            callback_data = callback.get('callback_data', None)
                            if callback_func:
                                func = ref_to_obj(callback_func)
                                thread_pool.submit(func, result, callback_data)
                                LOGGER.debug(f'结果: task={task_id}, func={callback_func}')
                            else:
                                LOGGER.debug(f'未处理: task={task_id}')
                            self._remove_task(key, async_result)
                        elif async_result.failed():
                            # 失败
                            self._remove_task(key, async_result)
                            LOGGER.error(f'失败: task={task_id}')

    def _remove_task(self, key, async_result):
        # 清理任务
        async_result.forget()
        self.rds_client.delete(key)
