import requests


r = requests.get("http://0.0.0.0:5000/profile", cookies=None)
print(r.json())
assert r.status_code == 403