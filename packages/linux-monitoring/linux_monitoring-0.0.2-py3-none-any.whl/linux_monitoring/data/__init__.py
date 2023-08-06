import mysql.connector


class database:
    def __init__(self, host: str, username: str, passwd: str, database: str):
        self.mydb = mysql.connector.connect(
            host=host,
            username=username,
            password=passwd,
            database=database
        )

    def insert_to_node_memory_metrics(self, capture_time, node_memory_Active_bytes, node_memory_MemTotal_bytes):
        my_cursor = self.mydb.cursor()

        query = "INSERT INTO node_memory_metrics (capture_time, active_bytes, mem_total_bytes) VALUES (%s, %s, %s)"
        val = (str(capture_time), node_memory_Active_bytes, node_memory_MemTotal_bytes)

        my_cursor.execute(query, val)
        self.mydb.commit()

    def insert_to_node_filesystem_metrics(self, capture_time, avail_bytes, size_bytes):
        my_cursor = self.mydb.cursor()

        query = "INSERT INTO node_filesystem_metrics (capture_time, avail_bytes, size_bytes) VALUES (%s, %s, %s)"
        val = (str(capture_time), avail_bytes, size_bytes)

        my_cursor.execute(query, val)
        self.mydb.commit()

    def insert_to_node_cpu_metrics(self, capture_time, total_idle_seconds, total_used_seconds):
        my_cursor = self.mydb.cursor()

        query = "INSERT INTO node_cpu_metrics (capture_time, idle_seconds, used_seconds) VALUES (%s, %s, %s)"
        val = (str(capture_time), total_idle_seconds, total_used_seconds)

        my_cursor.execute(query, val)
        self.mydb.commit()

    def get_memory_data(self, n_datapoints):
        my_cursor = self.mydb.cursor()

        query = "SELECT * FROM node_memory_metrics ORDER BY id DESC LIMIT "+str(n_datapoints)

        my_cursor.execute(query)
        result = my_cursor.fetchall()

        return result

    def get_filesystem_data(self, n_datapoints):
        my_cursor = self.mydb.cursor()

        query = "SELECT * FROM node_filesystem_metrics ORDER BY id DESC LIMIT "+str(n_datapoints)

        my_cursor.execute(query)
        result = my_cursor.fetchall()

        return result

    def get_cpu_data(self, n_datapoints):
        my_cursor = self.mydb.cursor()

        query = "SELECT * FROM node_cpu_metrics ORDER BY id DESC LIMIT "+str(n_datapoints+1)

        my_cursor.execute(query)
        result = my_cursor.fetchall()

        return result








