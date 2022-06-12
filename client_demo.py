import requests


r = requests.post('http://localhost:1729', json={'lol': 'kek'})
print(r.status_code, r.text)

r = requests.post('http://localhost:1729', json=[{'lol': 'kek'}, 3, 'five'])
print(r.status_code, r.text)

r = requests.get('http://localhost:1729')
print(r.status_code, r.text)

