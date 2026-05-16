"""
arduino_recommend — recommends an Arduino board based on experience level.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import apis as alol

api = alol.engine()

api.start(config={
    "host": "localhost",
    "port": 8082,
    "debug": True,
    "block_bots": False,
    "allowed_hosts": ["localhost", "127.0.0.1"],
    "rate_limit": 120,
    "cors": {"enabled": True, "origins": ["*"]},
    "honeypots": ["/.env", "/wp-login.php"],
    "routing": {
        "/": "./handlers/static.py",
        "/recommend": "./handlers/recommend.py",
    },
})
