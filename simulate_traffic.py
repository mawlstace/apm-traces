import requests
import time

URLS = [
    "http://localhost:5000/",
    "http://localhost:5000/slow",
    "http://localhost:5000/transaction",
    "http://localhost:5000/custom-metric"
]

for i in range(10):
    for url in URLS:
        try:
            r = requests.get(url)
            print(f"{url} => {r.status_code}")
        except Exception as e:
            print(f"{url} failed: {e}")
    time.sleep(1)

