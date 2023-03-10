#!/py/bin/env python


# Preload libraries
from distutils.log import error
from xmlrpc.client import DateTime
import helpers
import numpy
from random import randint as rand, sample as sample

from time import sleep
from secret import dbPwd, agentList
import mysql.connector
from mysql.connector import errorcode
import requests
import time
from bs4 import BeautifulSoup as bs
import random
from MySQLdb import _mysql
import datetime
import os
from rq.timeouts import BaseDeathPenalty
from constants import SAMPLE_SIZE


from rq import Queue, Connection

import redis
from redis import Redis
from rq.worker import HerokuWorker as Worker
# from rq import Worker



listen = ['high', 'default', 'low']
redis_url = os.getenv('REDIS_URL','redis://localhost:6379')
conn = redis.from_url(redis_url)


# url = urlparse(os.environ.get("REDIS_URL"))
# conn = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None)
# print(url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()

