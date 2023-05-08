# pytheus-bench

Sitting around while automated tools tell me if the [pytheus](https://github.com/Llandy3d/pytheus) library is correct and its performance.

## Intro

Comparing the official prometheus client & the pytheus library in both single process & multiprocess mode to compare correctness & performance.

with docker-compose spawn 4 services (one for each lib in each mode) and a prometheus instance scraping them. Load test them and see the results 🔍

**The services**

A simple flask server with three endpoints:
  - `/`: returning `Hello, World!`
  - `/metrics`: returning metrics
  - `/users/create`: accepting json to create an user saved in a local sqlite database.

The scrapes are happening every `5s`.

**The metrics**

- `http_hit_count_total`: an increasing counter for everytime the `/` path gets hit
- `http_request_duration_seconds`: an histogram tracking request duration for both `/` & `/users/create`
- `labeled_counter_total`: testing the presence of a metric with many labels, used to assure that the correct amount is in all services
- `scrape_duration_seconds`: histogram observing the `/metrics` endpoint, this gets hit by prometheus every `5s`~

To have some meat `labeled_counter_total` is created with childs, representing a single metric with many labels. (100)

Also 100 metrics are created with the name starting with `counter_` so that the scrape logic has something to process.

## Running the bench

Clone the repository and run `python load.py` and wait for the result :)

The duration of the load is defined in the `load.js` file, 10 seconds by default for quick iteration but results like the one belows are run on `5 minutes & 10 seconds` as the rate is calculated on the last 5min of data.

**Multiple runs**

For running multiple times with a clean state the `--cleanup` flag can be used so `python load.py --cleanup`.

**Note**: `--cleanup` will clear all unused docker images & volumes. It will basically run `docker system prune -a --volumes -f`.

**Note2.0**: also the containers will still be running after you run the bench™️ , this is so that prometheus can be queried manually. When you are done do a `docker-compose down` in the `pytheus-bench/compare` folder or just stop them as you prefer :)

## The Results 🧭

_**The bad**_

Seems to fare very well with the slowest part being the pytheus multiprocessing scrape (this was expected as the logic is currently not optimized, so it's on track 🚀)

_**The good**_

Pytheus multiprocess when working on a metric seems to be faster compared to the official client. Pytheus single process & official client seems to be similar in this.

Pytheus singleproces scrape is the fastest 🎉


**Summary**  

_(20 VUs, 5m10s)_

| 95th percentile                                                      | pytheus-singleprocess | pytheus-multiprocess | old-singleprocess | old-multiprocess |
|------------------------------------------------------------|-----------------------|----------------------|--------------------|-------------------|
| http_request_duration_seconds | `7ms` | `21ms` | `7ms` | `55ms` |
| scrape_duration_seconds       | `4ms` | `98ms` | `8ms` | `23ms` |

**Raw data**

```
query: http_hit_count_total
===========================
job: pytheus-singleprocess     value: 6000
job: pytheus-multiprocess      value: 6000
job: old-singleprocess         value: 6000
job: old-multiprocess          value: 6000

query: http_request_duration_seconds_count
==========================================
job: pytheus-singleprocess     value: 12000
job: pytheus-multiprocess      value: 12000
job: old-singleprocess         value: 12000
job: old-multiprocess          value: 12000

query: http_request_duration_seconds_sum
========================================
job: pytheus-singleprocess     value: 24.008896752860892
job: pytheus-multiprocess      value: 60.82827993882165
job: old-singleprocess         value: 24.138205040002504
job: old-multiprocess          value: 102.58362351097821

query: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
===============================================================================
job: pytheus-singleprocess     value: 0.007111913357400719
job: pytheus-multiprocess      value: 0.021321839080459787
job: old-singleprocess         value: 0.007076167076167067
job: old-multiprocess          value: 0.055111111111111014

query: labeled_counter_total
============================
job: pytheus-singleprocess     value: 0
job: pytheus-multiprocess      value: 0
job: old-singleprocess         value: 0
job: old-multiprocess          value: 0

query: count(labeled_counter_total{random_string=~".+"}) by (job)
=================================================================
job: pytheus-singleprocess     value: 100
job: pytheus-multiprocess      value: 100
job: old-singleprocess         value: 100
job: old-multiprocess          value: 100

query: scrape_duration_seconds_sum
==================================
job: pytheus-singleprocess     value: 0.11175767199893016
job: pytheus-multiprocess      value: 4.509488498002611
job: old-singleprocess         value: 0.2145954180014087
job: old-multiprocess          value: 0.5115620429933188

query: histogram_quantile(0.95, rate(scrape_duration_seconds_bucket[5m]))
=========================================================================
job: pytheus-singleprocess     value: 0.00475
job: pytheus-multiprocess      value: 0.09898936170212766
job: old-singleprocess         value: 0.008156249999999999
job: old-multiprocess          value: 0.023607142857142854
```
