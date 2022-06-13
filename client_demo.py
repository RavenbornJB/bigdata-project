import requests


# print("\npre-computed reports (last 6 hours):")
# r = requests.post('http://localhost:1729', data={'query_type': 'domains'})
# print(r.json())

print("\ntask 1:")
r = requests.post('http://localhost:5050', data={'query_type': 'domains'})
print(r.json())

print("\ntask 2:")
r = requests.post('http://localhost:5050', data={'query_type': 'page_user', 'user_id': 963971})
print(r.json())

print("\ntask 3:")
r = requests.post('http://localhost:5050', data={'query_type': 'page_domains', 'domain': 'es.wikipedia.org'})
print(r.json())

print("\ntask 4:")
r = requests.post('http://localhost:5050', data={'query_type': 'pages_info', 'page_id': 11858484})
print(r.json())

print("\ntask 5:")
r = requests.post('http://localhost:5050', data={'query_type': 'page_users_info', 'start_time': '2018-04-26 14:59:38',
                                                                                   'end_time': '2023-04-26 14:59:38'})
print(r.json())
