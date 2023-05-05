#!/bin/bash
rm -rf /old_multiprocess_data/* && gunicorn -w 4 --bind 0.0.0.0:5003 server_old:app

