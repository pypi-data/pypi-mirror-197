from threading import Thread

from zcbot_celery_sdk.client import ZcbotServiceClient
from zcbot_celery_sdk.processor import process_tax
from zcbot_celery_sdk.monitor import CeleryResultMonitor


def produce():
    client = ZcbotServiceClient(
        celery_broker_url='redis://127.0.0.1:6379/1',
        celery_result_backend='redis://127.0.0.1:6379/11',
        client_redis_uri='redis://127.0.0.1:6379/12',
        app_code='partner_staples'
    )
    sku_id = 'D909063752'
    sku_name = '扬帆耐立ERC39-J色带黑色133*90*35mm(支)'
    client.get_tax_by_baiwang(args=[sku_id, sku_name], callback_func=process_tax, callback_data={'tenantCode': 'deli'})


if __name__ == '__main__':
    produce()
