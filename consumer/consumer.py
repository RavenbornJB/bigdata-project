from kafka import KafkaConsumer
import pandas as pd
from datetime import datetime
import json

from compute_reports import compute_reports, REPORT_HOURS
from cassandra_client import CassandraClient


def unpack_message(message):
    payload = json.loads(message.value.decode('utf-8'))

    page_domain = payload['meta']['domain']
    page_title = payload['page_title']
    user_id = payload['performer']['user_id']
    user_name = payload['performer']['user_text']
    is_bot = payload['performer']['user_is_bot']

    return page_domain, page_title, user_id, user_name, is_bot


if __name__ == '__main__':
    # REPORT_HOURS + 1 dataframes: REPORT_HOURS for batch processing, last one for last hour
    # initialized empty to imply no data in the REPORT_HOURS hours before server launch
    columns = ['domain', 'title', 'uid', 'uname', 'is_bot']
    stored_data = [
        pd.DataFrame(columns=columns) for _ in range(REPORT_HOURS + 1)
    ]
    last_hour_data = []
    cur_hour = datetime.now().hour

    # init consumer
    cons = KafkaConsumer('wiki-create', bootstrap_servers='kafka-server')
    client = CassandraClient('cassandra-server', 9042, 'project_keyspace')

    # receive incoming messages, gracefully quit on Ctrl+C
    try:
        for msg in cons:
            # recompute reports when hour changes
            if datetime.now().second != cur_hour:
                cur_hour = datetime.now().second
                stored_data.pop(0)
                stored_data.append(pd.DataFrame(last_hour_data, columns=columns))
                last_hour_data = []

                compute_reports(stored_data, (cur_hour - REPORT_HOURS - 1) % 24)

            try:
                data = unpack_message(msg)
                last_hour_data.append(data)  # for precomputed reports
                client.insert(data)  # TODO: actually make insert in client
            except KeyError:  # incomplete entries
                pass

    except KeyboardInterrupt:
        cons.close()
        client.shutdown()
