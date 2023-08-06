import re
from datetime import datetime
import pandas as pd

import requests

from linux_monitoring.data import database


def insert_data(ip):
    url = "http://" + ip + ":9100/metrics"
    params = {
        # "query": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode='idle'}[5m])) * 100)"
    }
    metrics = requests.get(url, params=params)

    conn = database(
        host="linux-server-metrics.codyjzkfz0ge.ap-south-1.rds.amazonaws.com",
        username='admin',
        passwd='12345678',
        database='linux_metrics'
    )

    time_now = datetime.now()

    """*******************************************"""

    updated_metrics = metrics.text
    pattern = r'node_cpu_seconds_total\{cpu="(\d+)",mode="(?:iowait|irq|nice|softirq|steal|system|user)"\} (\d+\.\d+)'

    pattern_idle = r'node_cpu_seconds_total\{cpu="(\d+)",mode="(?:idle)"\} (\d+\.\d+)'
    idle_cpu_seconds = re.findall(pattern_idle, updated_metrics)
    # print(idle_cpu_seconds)

    used_cpu_seconds = re.findall(pattern, updated_metrics)
    # print(used_cpu_seconds)
    cpu_usage_seconds = {}
    for match in used_cpu_seconds:
        if int(match[0]) in cpu_usage_seconds:
            cpu_usage_seconds[int(match[0])] += float(match[1])
        else:
            cpu_usage_seconds[int(match[0])] = float(match[1])

    # print(cpu_usage_seconds)
    total_idle_seconds = 0
    for second in idle_cpu_seconds:
        total_idle_seconds += float(second[1])

    total_used_seconds = 0
    for second in used_cpu_seconds:
        total_used_seconds += float(second[1])

    conn.insert_to_node_cpu_metrics(
        capture_time=time_now,
        total_idle_seconds=total_idle_seconds,
        total_used_seconds=total_used_seconds
    )
    """*******************************************"""

    lines = metrics.content.decode().splitlines()

    node_memory_Active_bytes = -1
    node_memory_MemTotal_bytes = -1

    node_filesystem_avail_bytes = -1
    node_filesystem_size_bytes = -1

    for line in lines:
        if line.startswith("node_memory_Active_bytes"):
            node_memory_Active_bytes = float(line.split()[1])
        elif line.startswith("node_memory_MemTotal_bytes"):
            node_memory_MemTotal_bytes = float(line.split()[1])
        elif line.startswith("node_filesystem_avail_bytes{device=\"/dev/"):
            node_filesystem_avail_bytes += float(line.split()[1])
        elif line.startswith("node_filesystem_size_bytes{device=\"/dev/"):
            node_filesystem_size_bytes += float(line.split()[1])
        # elif line.startswith("node_cpu"):
        #     print(line)

    conn.insert_to_node_memory_metrics(
        capture_time=time_now,
        node_memory_Active_bytes=node_memory_Active_bytes,
        node_memory_MemTotal_bytes=node_memory_MemTotal_bytes
    )
    conn.insert_to_node_filesystem_metrics(
        capture_time=time_now,
        avail_bytes=node_filesystem_avail_bytes,
        size_bytes=node_filesystem_size_bytes
    )
    # time.sleep(10)
    # memory_usage = (node_memory_Active_bytes / node_memory_MemTotal_bytes) * 100
    #
    # free_disk = (node_filesystem_avail_bytes/node_filesystem_size_bytes)*100
    #
    # print("Memory Usage: "+str(memory_usage))
    # print("Free Disk: "+str(free_disk))


def get_memory_metrics(n_datapoints):
    conn = database(
        host="linux-server-metrics.codyjzkfz0ge.ap-south-1.rds.amazonaws.com",
        username='admin',
        passwd='12345678',
        database='linux_metrics'
    )
    data = conn.get_memory_data(n_datapoints)
    data.reverse()
    data_dict = {}
    for x in data:
        data_dict.setdefault('Capture Time', []).append(x[0])
        memory_usage = (float(x[1]) / float(x[2])) * 100
        data_dict.setdefault('Memory Usage', []).append(memory_usage)

    data_dict['Capture Time'] = data_dict['Capture Time'][-10:]
    data_dict['Memory Usage'] = data_dict['Memory Usage'][-10:]

    df = pd.DataFrame(data=data_dict)

    return df


def get_filesystem_metrics(n_datapoints):
    conn = database(
        host="linux-server-metrics.codyjzkfz0ge.ap-south-1.rds.amazonaws.com",
        username='admin',
        passwd='12345678',
        database='linux_metrics'
    )
    data = conn.get_filesystem_data(n_datapoints)
    data.reverse()
    data_dict = {}
    for x in data:
        data_dict.setdefault('Capture Time', []).append(x[0])
        free_disk = (float(x[1]) / float(x[2])) * 100
        data_dict.setdefault('Free Disk', []).append(free_disk)

    # data_dict['Capture Time'] = data_dict['Capture Time'][-10:]
    # data_dict['Free Disk'] = data_dict['Free Disk'][-10:]
    df = pd.DataFrame(data=data_dict)

    return df


def get_cpu_metrics(n_datapoints):
    conn = database(
        host="linux-server-metrics.codyjzkfz0ge.ap-south-1.rds.amazonaws.com",
        username='admin',
        passwd='12345678',
        database='linux_metrics'
    )
    data = conn.get_cpu_data(n_datapoints)

    def calculate_cpu(old_data: tuple, new_data: tuple):
        used_time = float(new_data[1]) - float(old_data[1])
        idle_time = float(new_data[0]) - float(old_data[0])
        print(new_data)
        cpu = (used_time/(used_time+idle_time))*100
        print(cpu)
        return cpu

    data.reverse()

    data_dict = {}
    i = 1
    while i < len(data):
        data_dict.setdefault('Capture Time', []).append(data[i][0])
        print(data[i-1])

        cpu_usage = calculate_cpu(
            (data[i-1][1], data[i-1][3]),
            (data[i][1], data[i][3])
        )
        i += 1
        data_dict.setdefault('CPU Usage', []).append(cpu_usage)

    df = pd.DataFrame(data=data_dict)

    return df
