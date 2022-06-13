import requests
import json


print("task 1:")
r = requests.post('http://localhost:5050', data={'query_type': 'domains'})
print(list(map(lambda x: x[0], r.json())))

print('\n', '-' * 50, '\n')
print("task 2:")
r = requests.post('http://localhost:5050', data={'query_type': 'page_user', 'user_id': 3628797})
print(r.json())

print('\n', '-' * 50, '\n')
print("task 3:")
r = requests.post('http://localhost:5050', data={'query_type': 'page_domains', 'domain': 'es.wikipedia.org'})
print(r.json()[0][0])

print('\n', '-' * 50, '\n')
print("task 4:")
r = requests.post('http://localhost:5050', data={'query_type': 'pages_info', 'page_id': 70998957})
print(r.json()[0])

print('\n', '-' * 50, '\n')
print("task 5:")
r = requests.post('http://localhost:5050', data={'query_type': 'page_users_info', 'start_time': '2022-06-13 03:45:00',
                                                 'end_time': '2022-06-13 03:47:00'})
print(r.json())

print('\n', '-' * 50, '\n')
print("pre-computed reports (last 6 hours):")
r = requests.get('http://localhost:1729')
with open('project-results/queries.json', 'w') as f:
    json.dump(r.json(), f)
print('Saved to `project-results/queries.json')
