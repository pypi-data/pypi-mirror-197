from datetime import datetime

from linux_monitoring.dao import *
import matplotlib.pyplot as plt
import pandas as pd


def generate_memory_usage_report(n_datapoints):
    memory_data = get_memory_metrics(n_datapoints)
    var_df = pd.DataFrame(memory_data, columns=['Capture Time', 'Memory Usage'])

    var_df.plot(x='Capture Time', y='Memory Usage', kind='line', marker='o')

    # plt.show()
    filename = 'mem_'+str(datetime.now())+'.png'
    filename = filename.replace(':', '')
    # print(filename)
    plt.ylim(0, max(memory_data['Memory Usage']) + 10)
    plt.savefig('reports\\'+filename)
    plt.close()


def generate_filesystem_usage_report(n_datapoints):
    filesystem_data = get_filesystem_metrics(n_datapoints)
    # print(filesystem_data)
    var_df = pd.DataFrame(filesystem_data, columns=['Capture Time', 'Free Disk'])

    var_df.plot(x='Capture Time', y='Free Disk', kind='line', marker='o')

    # plt.show()
    filename = 'filesystem_'+str(datetime.now())+'.png'
    filename = filename.replace(':', '')
    # print(filename)
    plt.ylim(0, max(filesystem_data['Free Disk'])+10)
    plt.savefig('reports\\'+filename)
    plt.close()


def generate_cpu_usage_report(n_datapoints):
    cpu_data = get_cpu_metrics(n_datapoints)
    print(cpu_data)
    var_df = pd.DataFrame(cpu_data, columns=['Capture Time', 'CPU Usage'])

    var_df.plot(x='Capture Time', y='CPU Usage', kind='line', marker='o')

    # plt.show()
    filename = 'cpu_'+str(datetime.now())+'.png'
    filename = filename.replace(':', '')
    # print(filename)
    plt.ylim(0, max(cpu_data['CPU Usage'])+5)
    plt.savefig('reports\\'+filename)
    plt.close()


def generate_common_report(n_datapoints):
    filesystem_data = get_filesystem_metrics(n_datapoints)
    memory_data = get_memory_metrics(n_datapoints)
    cpu_data = get_cpu_metrics(n_datapoints)

    fig = plt.figure()
    ax_memory = fig.add_subplot(2, 2, 1)
    ax_filesystem = fig.add_subplot(2, 2, 2)
    ax_cpu = fig.add_subplot(2, 2, 3)

    var_df = pd.DataFrame(filesystem_data, columns=['Capture Time', 'Free Disk'])
    var_df.plot(ax=ax_filesystem, x='Capture Time', y='Free Disk', kind='line')

    var_df = pd.DataFrame(memory_data, columns=['Capture Time', 'Memory Usage'])
    var_df.plot(ax=ax_memory, x='Capture Time', y='Memory Usage', kind='line')

    var_df = pd.DataFrame(cpu_data, columns=['Capture Time', 'CPU Usage'])
    var_df.plot(ax=ax_cpu, x='Capture Time', y='CPU Usage', kind='line')

    filename = 'Stats_'+str(datetime.now())+'.png'
    filename = filename.replace(':', '')
    # print(filename)
    # plt.ylim(min(filesystem_data['Free Disk'])-1, max(filesystem_data['Free Disk'])+1)
    plt.savefig('reports\\'+filename)
    plt.close()



