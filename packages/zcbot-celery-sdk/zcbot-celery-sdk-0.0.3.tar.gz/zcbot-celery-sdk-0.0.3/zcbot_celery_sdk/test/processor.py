import threading
import time
from datetime import datetime

from dateutil import tz

from ..common import thread_pool


def process_tax(result, callback_data):

    # print(f'处理[{threading.currentThread()}, {thread_pool.get_pool_size()}] result={result}, callback_data={callback_data}')
    print(f'处理开始[{result.get("sn")}][{threading.currentThread()}, {thread_pool.get_pool_size()}] start={datetime.now(tz.gettz("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S.%f")}  result={result}')
    time.sleep(0.5)
    print(f'处理完成[{result.get("sn")}][{threading.currentThread()}, {thread_pool.get_pool_size()}] end={datetime.now(tz.gettz("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S.%f")}  result={result}')
