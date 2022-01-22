import random
import time

from flask import Flask

app = Flask(__name__)


@app.route("/health")
def health():
    choices = [True, True, True, False]
    time.sleep(random.randint(1, 3))
    return {"status": random.choice(choices)}
