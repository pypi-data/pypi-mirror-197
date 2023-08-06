from zcbot_celery_sdk.client import CeleryApi
from zcbot_celery_sdk.monitor import CeleryResultMonitor
from zcbot_celery_sdk.test.processor import process_tax


def product():
    client = CeleryApi(
        celery_broker_url='amqp://root:Dangerous!@rabbit_host:5672/zcbot_celery',
        celery_result_backend='redis://redis_host:6379/14',
        client_redis_uri='redis://redis_host:6379/12',
        app_code='partner_staples'
    )
    sku_id = 'D909063752'
    sku_name = '扬帆耐立ERC39-J色带黑色133*90*35mm(支)'
    client.get_tax_by_baiwang(args=[sku_id, sku_name], callback_func=process_tax, callback_data={'tenantCode': 'deli'})


def consume():
    monitor = CeleryResultMonitor(
        celery_broker_url='amqp://root:Dangerous!@rabbit_host:5672/zcbot_celery',
        celery_result_backend='redis://redis_host:6379/14',
        client_redis_uri='redis://redis_host:6379/12',
        app_code='partner_staples'
    )
    monitor.start()


if __name__ == '__main__':
    product()
    # consume()
