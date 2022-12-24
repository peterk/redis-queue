from flask import Flask, render_template, request
import redis
import msgpack
from datetime import datetime
import os

app = Flask(__name__)

# Set up Redis connection
r = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    password=os.environ["REDIS_PASSWORD"])

# The name of your queue
queue_name = "myqueue"


@app.route('/', methods=['GET', 'POST'])
def home():
    """A tiny homepage. The html template is in the templates folder."""

    # Print the queue length to the console
    print(f"Current queue length: {r.llen(queue_name)}")

    if request.method == 'POST':
        now = datetime.now().isoformat()

        # This dict is used to pass information to workers.
        # It can contain anything you need.
        jobdata = {
            "name": "a job name",
            "created": now,
            "work": int(request.form["jobsecs"])
        }

        # Add job to queue (pack job data with messagepack)
        # See https://redis.io/commands/lpush/
        r.lpush(queue_name, msgpack.packb(jobdata))

    return render_template('index.html', qlen=r.llen(queue_name))


if __name__ == "__main__":
    # Start flask server in debug mode
    app.run(host='0.0.0.0', debug=True, port=8000)
