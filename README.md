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
- `scrape_duration_seconds`: histogram observing the `/metrics` endpoint, this also gets hit by prometheus every `5s`~

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

_**The good**_

Pytheus multiprocess when working on a metric seems to be faster compared to the official client. Pytheus single process & official client seems to be similar in this.

Pytheus multiprocess scraping is faster than the official client 🎉


**Summary**  

_(20 VUs, 5m10s)_

| 95th percentile                                                      | pytheus-singleprocess | pytheus-multiprocess | old-singleprocess | old-multiprocess |
|------------------------------------------------------------|-----------------------|----------------------|--------------------|-------------------|
| http_request_duration_seconds | `7ms` | `11ms` | `7ms` | `43ms` |
| scrape_duration_seconds       | `4ms` | `9ms` | `4ms` | `18ms` |

**Raw data**

```
query: http_hit_count_total
===========================
job: pytheus-singleprocess     value: 5900
job: pytheus-multiprocess      value: 5900
job: old-singleprocess         value: 5900
job: old-multiprocess          value: 5900

query: http_request_duration_seconds_count
==========================================
job: pytheus-singleprocess     value: 11800
job: pytheus-multiprocess      value: 11800
job: old-singleprocess         value: 11800
job: old-multiprocess          value: 11800

query: http_request_duration_seconds_sum
========================================
job: pytheus-singleprocess     value: 24.08901406941004
job: pytheus-multiprocess      value: 36.49198011102271
job: old-singleprocess         value: 23.01847539495793
job: old-multiprocess          value: 95.25116192756104

query: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
===============================================================================
job: pytheus-singleprocess     value: 0.007551652892561981
job: pytheus-multiprocess      value: 0.011822183098591565
job: old-singleprocess         value: 0.007182906458797334
job: old-multiprocess          value: 0.043567639257294524

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

query: scrape_duration_seconds_count
====================================
job: pytheus-singleprocess     value: 5964
job: pytheus-multiprocess      value: 5963
job: old-singleprocess         value: 5963
job: old-multiprocess          value: 5964

query: scrape_duration_seconds_sum
==================================
job: pytheus-singleprocess     value: 4.644447718921583
job: pytheus-multiprocess      value: 27.741890347999288
job: old-singleprocess         value: 7.73627702932572
job: old-multiprocess          value: 30.317366370465606

query: histogram_quantile(0.95, rate(scrape_duration_seconds_bucket[5m]))
=========================================================================
job: pytheus-singleprocess     value: 0.004769734465317919
job: pytheus-multiprocess      value: 0.009795581395348835
job: old-singleprocess         value: 0.00483637934169849
job: old-multiprocess          value: 0.018114776951672858
```
