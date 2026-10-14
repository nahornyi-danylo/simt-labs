import os
import socket

import redis
from flask import Flask, jsonify

app = Flask(__name__)

redis_client = redis.Redis(
    host="database",
    port=6379,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
)

@app.get("/")
def index():
    try:
        counter = redis_client.incr("lab1:counter")
        return jsonify(counter=counter)
    except redis.exceptions.RedisError:
        app.logger.exception("Redis request failed")
        return jsonify(error="database unavailable"), 503

@app.get("/test")
def test():
    try:
        redis_client.ping()
        return jsonify(status="ok")
    except redis.exceptions.RedisError:
        return jsonify(error="database unavailable"), 503
