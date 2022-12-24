#!/usr/bin/env python
import redis
import time
import traceback
import msgpack  # see https://msgpack.org
from datetime import datetime
import os

# The name of your queue from which the worker will pick up jobs
queue_name = "myqueue"

redis_connection = None


def get_redis_connection():
    """Get a connection to Redis. Tries indefinitely but adds a bit of
    waiting time."""

    global redis_connection

    wait = 0  # Waiting time in secs until next connection try

    while redis_connection is None:
        print(f"Waiting for connection {wait} secs")
        time.sleep(wait)

        redis_connection = redis.Redis(
            host='redis',
            port=6379,
            db=0,
            password=os.environ["REDIS_PASSWORD"])

        wait = (wait + 1) ** 2
        if wait > 30:
            wait = 0

    print("Connection established")


def handle_job(job):
    """This is where the job is done. In this example we get the
    number of seconds to sleep."""

    try:
        print(f"Job: {job['name']} received. Running {job['work']} seconds")
        time.sleep(int(job['work']))  # example work to be done
        print("Job completed successfully")

    except Exception:
        print(f"Job failed: {traceback.print_exc()}")


if __name__ == "__main__":
    print("Starting worker")
    while True:
        print("Waiting for job")

        try:
            get_redis_connection()

            # Get job from queue. See https://redis.io/commands/brpop/
            rawjob = redis_connection.brpop(queue_name)

            # Unpack it
            job = msgpack.unpackb(rawjob[1])

            # Job created at
            created = datetime.fromisoformat(job["created"])

            print(job)
            handle_job(job)

            # Calculate running time
            running_time = datetime.now() - created

            print(f"Job took {running_time.seconds} seconds")

        except redis.exceptions.ConnectionError:
            print("Connection error")
            traceback.print_exc()
            get_redis_connection()
            continue
