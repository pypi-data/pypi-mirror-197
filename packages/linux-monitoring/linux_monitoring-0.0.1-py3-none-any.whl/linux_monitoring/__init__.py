import threading
from linux_monitoring.visualization import *
from linux_monitoring.dao import insert_data
import time

__version__ = '0.0.1'
__author__ = 'Dheeraj banodha'


def task_1(ip: str):
    """
    :param ip: ip address
    :return:
    """
    while True:
        insert_data(ip)
        time.sleep(29)


def task_2(n_datapoints):
    """
    :param n_datapoints: no. of datapoints to generate reports
    :return:
    """
    while True:
        generate_memory_usage_report(n_datapoints=10)
        generate_filesystem_usage_report(n_datapoints=10)
        generate_cpu_usage_report(n_datapoints=10)
        # generate_common_report()
        time.sleep(29)


def generate_reports(ip: str, n_datapoints: int):
    """
    :param ip: ip address of the linux server
    :param n_datapoints: no. of datapoints to generate the reports
    :return:
    """
    t1 = threading.Thread(target=task_1, args=(ip,))
    t2 = threading.Thread(target=task_2, args=(n_datapoints,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

