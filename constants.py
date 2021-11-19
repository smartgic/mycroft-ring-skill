"""This file contains constants mostly called by utils.py
"""
from os import getenv

# Token file used as cache by ring_doorbell Python library
TOKEN_CACHE_DIR = getenv('HOME') + '/.config/ring_doorbell'
TOKEN_CACHE_FILE = f'{TOKEN_CACHE_DIR}/token_cache.json'

# User agent used by the skill to speak wtih Ring API
USER_AGENT = 'MycroftAI/1.0'

# Interval in seconds to check for dings alerts
DING_INTERVAL = 5

# Interval in seconds to wait before the speak dialog
DING_AUDIO_INTERVAL = 3

# Mime type of the doorbell sound files
AUDIO_MIME_TYPE = 'audio/mpeg'
