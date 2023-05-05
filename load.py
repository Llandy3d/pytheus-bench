import os
import json
import subprocess
import time
import requests


file_path = 'test.json'
prometheus_url = 'http://localhost:9090/api/v1/query'


sub = subprocess.run(
    ['k6', 'run', 'load.js', f'--summary-export={file_path}']
)
sub.check_returncode()

with open(file_path, 'r') as f:
    result = json.loads(f.read())
os.remove(file_path)


# wait to be sure that a scrape was done by prometheus
print('sleeping...')
time.sleep(6)


queries = [
    'http_hit_count_total',
    'http_request_duration_seconds_count',
    'http_request_duration_seconds_sum',
    'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))',
]

for query in queries:
    resp = requests.get(prometheus_url, params={'query': query})
    metrics = resp.json()['data']['result']

    print(f'query: {query}')
    print((len(query) + 7) * '=')
    for metric in metrics:
        job = metric['metric']['job']
        value = metric['value'][1]
        print(f'job: {job}    value: {value}')
    print()
