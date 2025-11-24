# Redis Distributed Caching Demo

This project demonstrates how Redis can be used as a distributed cache
to speed up an "expensive" operation under parallel load using multiple
processes.

## Features

-   Flask API simulating an expensive operation\
-   Redis cache layer with optional TTL\
-   Multi-process load generator using Python multiprocessing\
-   Demonstrates parallelism + distributed caching\
-   Easy to run locally (macOS/Linux/Windows)

## Requirements

-   Python 3.8+
-   Redis installed locally
-   pip for Python dependencies

## Installation

Clone the repository:

    git clone https://github.com/your/repo.git](https://github.com/Anthonyvillaaa/Redis-Distributed-Caching-Demo
    cd repo

## Virtual Environment Setup

    python3 -m venv venv
    source venv/bin/activate   # macOS/Linux
    pip install flask redis requests

## Start Redis

    redis-server

## Run the Flask Service

Without caching:

    USE_CACHE=0 python3 service.py

With caching:

    USE_CACHE=1 python3 service.py

## Run the Load Test

    python3 load_test.py

## Expected Results

-   Without Redis: almost all requests are slow\
-   With Redis: only first requests per key are slow; remaining are
    instant

## Troubleshooting

ModuleNotFoundError: activate the venv:

    source venv/bin/activate

Redis connection error: ensure Redis is running:

    redis-server

## License

MIT License.
