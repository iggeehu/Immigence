#!/py/bin/env python
from redis import Redis
from rq import Worker

# Preload libraries
from distutils.log import error
from xmlrpc.client import DateTime
import helpers
import numpy
from random import randint as rand, sample as sample
from redis import Redis
from rq import Worker
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
from constants import SAMPLE_SIZE
import redis
from helpers import dbOperations
from redis import Redis
from rq import Queue, Connection


# url = urlparse(os.environ.get("REDIS_URL"))
# conn = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None)
# print(url)


# Provide the worker with the list of queues (str) to listen to.
w = Worker(['default', 'high', 'low'], connection=Redis())
w.work()



