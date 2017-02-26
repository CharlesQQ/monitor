#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Charles Chang'

import redis

def redis_conn(settings):
    pool = redis.ConnectionPool(host=settings.REDIS_CONN['HOST'],port=settings.REDIS_CONN['PORT'])
    r = redis.Redis(connection_pool=pool)
    return r