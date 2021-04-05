#!/bin/sh

py.test -vvv app/tests/test_backend.py
gunicorn --chdir app backend:app -w 2 --threads 2 -b 0.0.0.0:8080