__author__ = "Carlos Ruiz"

import os
from typing import Any

DEFAULT_CONFIG: dict[str, Any] = {
    "host": "localhost",
    "port": 8080,
    "debug": False,
    "ssl": None,
    "workers": 1,
    "auto_reload": False,
    "auto_reload_interval": 2,
    "secret_key": "change_me",
    "allowed_hosts": ["localhost", "127.0.0.1"],
    "rate_limit": 60,
    "rate_limit_window": 60,
    "block_bots": True,
    "honeypots": ["/admin", "/wp-login"],
    "ip_blacklist": [],
    "ip_whitelist": [],
    "ua_blocklist": [],
    "cors": {
        "enabled": True,
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        "headers": ["Content-Type", "Authorization", "X-API-Key"],
        "allow_credentials": False,
        "max_age": 600,
    },
    "api_key": {
        "enabled": False,
        "header": "X-API-Key",
        "query_param": "api_key",
        "keys": [],
    },
    "cooldown": {
        "enabled": False,
        "window": 10,
        "trigger_on_status": [429, 500],
    },
    "routing": {},
}

class ConfigError(Exception):
    """Raised when the provided configuration is invalid."""

def merge_config(user_config: dict[str, Any]) -> dict[str, Any]:
    """
    Deep-merges user_config on top of DEFAULT_CONFIG.
    Nested dicts are merged recursively; all other values are overwritten.
    """
    result = _deep_copy(DEFAULT_CONFIG)
    _deep_merge(result, user_config)
    return result

def validate_config(config: dict[str, Any]) -> None:
    """
    Validates the merged configuration dictionary.
    Raises ConfigError with a descriptive message on the first violation found.
    """
    if not isinstance(config.get("port"), int) or not (1 <= config["port"] <= 65535):
        raise ConfigError("'port' must be an integer between 1 and 65535.")

    if not isinstance(config.get("host"), str) or not config["host"]:
        raise ConfigError("'host' must be a non-empty string.")

    if config.get("ssl") is not None:
        ssl = config["ssl"]
        if not (isinstance(ssl, (list, tuple)) and len(ssl) == 2):
            raise ConfigError("'ssl' must be a (keyfile, certfile) tuple or None.")
        keyfile, certfile = ssl
        if not os.path.isfile(keyfile):
            raise ConfigError(f"SSL keyfile not found: {keyfile}")
        if not os.path.isfile(certfile):
            raise ConfigError(f"SSL certfile not found: {certfile}")

    if not isinstance(config.get("workers"), int) or config["workers"] < 1:
        raise ConfigError("'workers' must be a positive integer.")

    if not isinstance(config.get("rate_limit"), int) or config["rate_limit"] < 0:
        raise ConfigError("'rate_limit' must be a non-negative integer.")

    if not isinstance(config.get("allowed_hosts"), list):
        raise ConfigError("'allowed_hosts' must be a list of strings.")

    if not isinstance(config.get("routing"), dict):
        raise ConfigError("'routing' must be a dict mapping path prefixes to handler paths.")

def _deep_copy(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _deep_copy(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_deep_copy(i) for i in obj]
    return obj

def _deep_merge(base: dict, override: dict) -> None:
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value