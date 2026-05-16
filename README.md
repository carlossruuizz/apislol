<div align="center">
<img src="https://i.imgur.com/Ytw0dW6.png" />

| <a href="https://github.com/carlossruuizz/apislol"><img src="https://img.shields.io/badge/version-1.1.1-f2c94c?style=flat-square" alt="Version" /></a> <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-f2c94c?style=flat-square" alt="Python" /></a> <a href="./LICENSE"><img src="https://img.shields.io/badge/license-bsd3 clause-f2c94c?style=flat-square" alt="License" /></a> <a href="https://github.com/carlossruuizz/apislol/stargazers"><img src="https://img.shields.io/github/stars/carlossruuizz/apislol?style=flat-square&color=f2c94c" alt="Stars" /></a> |
|---|

[Spanish/Español](./docs/README.es.md) — [Chinese/中文](./docs/README.zh.md) ⁞ [Brainfuck/BF](./docs/README.bf.md)

</div>

<img align="right" src="https://i.imgur.com/H0Ta4fj.png" height="250px" alt="apislol logo">

**Build HTTP APIs in pure Python** with zero dependencies and minimal boilerplate. A lightweight framework with a built-in security middleware stack, flexible routing, and multi-format response transforms.

**apislol provides:** *Rate limiting*, *Bot blocking*, *CORS*, *Honeypot traps*, *IP/UA blocklists*, *API key auth*, *Cooldown*, *Response transforms (JSON, YAML, XML, CSV, TOML, HTML)*, and more.

> [!NOTE]
> Requires Python 3.10+. No external dependencies — built entirely on the Python standard library.

## Quick Start

```bash
pip install git+https://github.com/carlossruuizz/apislol.git
```

```python
import apis as alol

api = alol.engine()

api.start(config={
    "host": "localhost",
    "port": 8080,
    "rate_limit": 60,
    "block_bots": True,
    "honeypots": ["/.env", "/admin", "/wp-login.php"],
    "cors": {"enabled": True, "origins": ["*"]},
    "routing": {
        "/users": "./handlers/users.py",
    },
})
```

<details>
<summary><b><code>Development</code></b></summary>

### Setup

```bash
git clone https://github.com/carlossruuizz/apislol.git
cd apislol
```

### Handler example

```python
from apislol.router import Router
from apislol.request import Request
from apislol.response import Response

router = Router()

@router.get("/{id}")
def get_user(request: Request) -> Response:
    return Response.json({"id": request.path_params["id"]})
```

</details>

> [!TIP]
> Return a plain *`dict`* from any handler — apislol auto-serializes it based on the *`Accept`* header or URL suffix (e.g. *`/users/1.yaml`*).

---

### Middleware

<div>

| Component | Behavior |
|-----------|----------|
| *`RateLimiter`* | Sliding-window per-IP request cap |
| *`BotBlocker`* | Block known bots, AI crawlers, headless browsers |
| *`IPFilter`* | Block/allow IPs and CIDR ranges |
| *`UaBlocklist`* | Custom User-Agent regex patterns |
| *`CorsMiddleware`* | Inject CORS headers per config |
| *`HoneypotMiddleware`* | Ban IPs that hit trap paths |
| *`ApiKeyMiddleware`* | Header or query-param key validation |
| *`CooldownMiddleware`* | Per-IP delay after repeated errors |
| *`AllowedHosts`* | Validate the *`Host`* header |

### Response Transforms

| Format | Content-Type |
|--------|-------------|
| *`json`* | *`application/json`* |
| *`yaml`* | *`application/x-yaml`* |
| *`toml`* | *`application/toml`* |
| *`xml`* | *`application/xml`* |
| *`csv`* | *`text/csv`* |
| *`html`* | *`text/html`* |

> Resolved automatically via *`Accept`* header or URL suffix. <br>
> Register custom formats with *`engine.transforms.register()`*.

--- 

### Routing

```python
api.start(config={
    "routing": {
        "/users":    "./handlers/users.py",
        "/products": "./handlers/products.py",
    }
})
```

> Dynamic path parameters use *`{param}`* syntax:

```python
@router.get("/{id}")
def get_item(request: Request) -> dict:
    return {"id": request.path_params["id"]}
```

---

<div align="center">

**Built by <a href="https://github.com/carlossruuizz">Carlos Ruiz</a>**

</div>
