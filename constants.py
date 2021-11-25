"""This file contains constants mostly called by utils.py
"""
from os import getenv

# Token file used as cache by ring_doorbell Python library
TOKEN_CACHE_DIR = getenv('HOME') + '/.config/ring_doorbell'
TOKEN_CACHE_FILE = f'{TOKEN_CACHE_DIR}/token_cache.json'

# User agent used by the skill to speak wtih Ring API
USER_AGENT = 'MycroftAI/1.0'

# Interval in seconds to check for alerts
ALERTS_INTERVAL = 5
