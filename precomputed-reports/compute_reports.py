import pandas as pd
import requests


REPORT_HOURS = 6


def compute_reports(data, start_hour):
    """
    sends reports to reports-server, where it stores them until someone
    sends a GET request, or until we send new ones after 1 hour
    """
    data = data[:-1]
    r = requests.post('http://reports-server:1729', json={
        'first_query': first_query(data, start_hour),
        'second_query': second_query(data, start_hour),
        'third_query': third_query(data, start_hour)
    })
    print('request done')


def first_query(data, start_hour):
    return [{
        'time_start': f'{(start_hour + i):02}:00',
        'time_end': f'{(start_hour + i + 1) % 24:02}:00',
        'statistics': {domain: count for domain, count in data[i].groupby('domain').domain.count().iteritems()}
    } for i in range(REPORT_HOURS)]


def second_query(data, start_hour):
    data = pd.concat(data, axis=0)
    if len(data) > 0:
        data = data[data.is_bot]

    stats = data.groupby('domain').domain.count()

    return {
        'time_start': f'{start_hour:02}:00',
        'time_end': f'{(start_hour + 6) % 24:02}:00',
        'statistics': [{'domain': domain, 'created_by_bots': by_bots} for (domain, by_bots) in stats.iteritems()]
    }


def third_query(data, start_hour):
    data = pd.concat(data, axis=0)

    stats = (data.groupby('uid').agg({'title': list, 'uname': 'first'})
             .sort_values('title', key=lambda x: x.map(len), ascending=False))[:20]

    return {
        'time_start': f'{start_hour:02}:00',
        'time_end': f'{(start_hour + 6) % 24:02}:00',
        'top_users': [{'uid': uid, 'uname': row[1], 'titles': row[0], 'num_created': len(row[0])}
                      for (uid, row) in stats.iterrows()]
    }
