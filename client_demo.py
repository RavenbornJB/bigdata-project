import requests

print("task 1:")
r = requests.post('http://localhost:9042', data={'query_type': 'domains'})
print(json.loads(r.text))

print("task 2:")
r = requests.post('http://localhost:9042', data={'query_type': 'page_user', 'user_id': 963971})
print(json.loads(r.text))

print("task 3:")
r = requests.post('http://localhost:9042', data={'query_type': 'page_domains', 'domain': 'es.wikipedia.org'})
print(json.loads(r.text))

print("task 4:")
r = requests.post('http://localhost:9042', data={'query_type': 'pages_info', 'page_id': 10260331})
print(json.loads(r.text))

print("task 5:")
r = requests.post('http://localhost:9042', data={'query_type': 'page_users_info', 'start_time': '2018-04-26 14:59:38',
                                                                                   'end_time': '2023-04-26 14:59:38'})
print(json.loads(r.text))
