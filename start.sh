#!/bin/bash
pip install -r requirements.txt
gunicorn app:app -w 2 -b 0.0.0.0:3000 --timeout 120
