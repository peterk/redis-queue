# Minimal set up of a queue using Docker compose / Redis / Python

This is an example setup of a docker compose solution where a frontend (web) adds jobs to a queue and multiple workers (worker) pick jobs and executes them. I could not find a similar solution that did not rely on a specific library. This solution only uses the standard redis library and msgpack (for passing job data to workers).

This solution may be useful if you have long running jobs and want to use Redis as a simple queue. If the [Redis](https://redis.io) connection is lost the worker will try to reconnect. 

If you have any suggestions for improvement, please add an issue.

## Run this example

First, clone this repository:

```bash
git clone --depth=1 https://github.com/peterk/redis-queue
```

Enter the folder and create a .env file by copying the example file:
```bash
cd redis-queue
cp .env_example .env
```

Build and start the system with two workers:
```bash
docker compose build
docker compose up --scale worker=2
```

Open http://127.0.0.1:8080 to add jobs. Look at the log to see what happens.

After adding a couple of long running jobs (increase the number of seconds), try stopping the Redis server from a different terminal:
```bash
docker compose stop redis
```

The workers should start trying to reconnect. Start the Redis server to see jobs getting worked on again.
```bash
docker compose start redis
```

## Notes

1. Please note the default information in the .env file. Not suitable for production.
2. Update versions of all libraries/images in requirements.txt, Dockerfile and docker-compose.yml if you start from this solution in your own project.