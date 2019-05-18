#!/usr/bin/env python3
"""
This is a set of common functions used by each naumachia VPN script
"""

from db import DB
from redis import Redis
import os
import yaml

ENVFILE = '/env.yaml'

def get_env():
    env = {}
    yamlenv = {}
    with open(ENVFILE, 'r') as f:
        yamlenv = yaml.safe_load(f)

    env['REDIS_HOSTNAME'] = yamlenv.get('redis_hostname', 'redis')
    env['REDIS_DB'] = int(yamlenv.get('redis_db', '0'))
    env['REDIS_PORT'] = int(yamlenv.get('redis_port', '6379'))
    env['REDIS_PASSWORD'] = yamlenv.get('redis_password', None)
    env['HOSTNAME'] = yamlenv.get('hostname')
    env['NAUM_VETHHOST'] = yamlenv.get('naum_vethhost')
    env['NAUM_FILES'] = yamlenv.get('naum_files')
    env['NAUM_CHAL'] = yamlenv.get('naum_chal')
    env['PUSH_ADDR'] = yamlenv.get('push_addr', None)
    env['PUSH_MASK'] = yamlenv.get('push_mask', None)

    env['COMMON_NAME'] = os.getenv('common_name')
    env['TRUSTED_IP'] = os.getenv('trusted_ip', None)
    env['TRUSTED_PORT'] = os.getenv('trusted_port', None)

    if DB.redis is None:
        set_redis(env)

    return env

def set_redis(env):
    DB.redis = Redis(host=env['REDIS_HOSTNAME'], port=env['REDIS_PORT'], db=env['REDIS_DB'], password=env['REDIS_PASSWORD'])
