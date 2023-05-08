import argparse
# import os
# import json
import subprocess
import time
import requests

from collections import defaultdict


file_path = 'test.json'
prometheus_url = 'http://localhost:9090/api/v1/query'

parser = argparse.ArgumentParser()
# parser.add_argument("--cleanup", type=bool, help="Your age.")
parser.add_argument("--cleanup", action="store_true")
args = parser.parse_args()

#### cleanup ####

if args.cleanup:
    cleanup_commands = [
        ['docker-compose', '-f', 'compare/docker-compose.yml', 'down'],
        ['docker', 'system', 'prune', '-a', '--volumes', '-f'],
        ['docker-compose', '-f', 'compare/docker-compose.yml', 'up', '--build', '-d'],
    ]

    for command in cleanup_commands:
        sub = subprocess.run(
            command,
        )
        sub.check_returncode()

    # give time for services to startup
    print('giving time for services to start...')
    time.sleep(10)

sub = subprocess.run(
    ['k6', 'run', 'load.js']
    # ['k6', 'run', 'load.js', f'--summary-export={file_path}']
)
sub.check_returncode()

# with open(file_path, 'r') as f:
#     result = json.loads(f.read())
# os.remove(file_path)


# wait to be sure that a scrape was done by prometheus
print('sleeping...')
time.sleep(6)


queries = [
    'http_hit_count_total',
    'http_request_duration_seconds_count',
    'http_request_duration_seconds_sum',
    'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))',
    'labeled_counter_total',
    'count(labeled_counter_total{random_string=~".+"}) by (job)',
    'scrape_duration_seconds_sum',
    'histogram_quantile(0.95, rate(scrape_duration_seconds_bucket[5m]))',
]

# for query in queries:
#     resp = requests.get(prometheus_url, params={'query': query})
#     metrics = resp.json()['data']['result']

#     print(f'query: {query}')
#     print((len(query) + 7) * '=')
#     metrics.sort(key=lambda x: x['metric']['job'], reverse=True)
#     for metric in metrics:
#         job = metric['metric']['job'].ljust(22)
#         value = metric['value'][1]
#         print(f'job: {job}    value: {value}')
#     print()


for query in queries:
    resp = requests.get(prometheus_url, params={'query': query})
    metrics = resp.json()['data']['result']

    filtered = defaultdict(list)

    # separate by job and add up different values
    for metric in metrics:
        metric_list = filtered[metric['metric']['job']]
        value = metric['value'][1]
        if value not in metric_list:
            metric_list.append(value)

    print(f'query: {query}')
    print((len(query) + 7) * '=')
    sorted_job = sorted(filtered, reverse=True)
    for job in sorted_job:
        value = filtered[job]
        print(f'job: {job.ljust(22)}    value: {", ".join(value)}')
    print()
