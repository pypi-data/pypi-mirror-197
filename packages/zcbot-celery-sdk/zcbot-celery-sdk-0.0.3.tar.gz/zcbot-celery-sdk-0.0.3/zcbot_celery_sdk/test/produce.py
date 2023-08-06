from zcbot_celery_sdk.client import CeleryClient
from zcbot_celery_sdk.service.tax import TaxService
from zcbot_celery_sdk.test.processor import process_tax

# 全局只需创建一次
client = CeleryClient(
    celery_broker_url='amqp://root:Dangerous!@rabbit_host:5672/zcbot_celery',
    celery_result_backend='redis://redis_host:6379/14',
    client_redis_uri='redis://redis_host:6379/15',
    app_code='partner'
)
# 各服务直接引用client
service = TaxService(client)


def produce(sn, name):
    rs = service.get_tax_by_baiwang(kwargs={'sn': sn, 'name': name}, callback_func=process_tax, callback_data={'tenantCode': 'deli'})
    print(rs)


if __name__ == '__main__':
    for sn in range(100, 999):
        produce(sn, f'{sn} --> vvvvvvvv')
