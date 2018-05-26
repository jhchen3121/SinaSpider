#!/bin/bash

#celery -A  tasks worker -c 20 --loglevel=info
celery -A  tasks worker --loglevel=info
