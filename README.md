<div align="center">
<img src="https://i.imgur.com/Ytw0dW6.png" />

| <a href="https://github.com/carlossruuizz/apislol"><img src="https://img.shields.io/badge/version-1.1.1-f2c94c?style=flat-square" alt="Version" /></a> <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-f2c94c?style=flat-square" alt="Python" /></a> <a href="./LICENSE"><img src="https://img.shields.io/badge/license-bsd3%20clause-f2c94c?style=flat-square" alt="License" /></a> <a href="https://github.com/carlossruuizz/apislol/stargazers"><img src="https://img.shields.io/github/stars/carlossruuizz/apislol?style=flat-square&color=f2c94c" alt="Stars" /></a> |
|---|
| <a href="https://github.com/carlossruuizz/apisloL/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22"><img src="https://img.shields.io/github/issues/carlossruuizz/apisloL/good%20first%20issue?style=flat-square&color=7057ff&label=good%20first%20issues" alt="Good First Issues" /></a> <a href="https://github.com/carlossruuizz/apisloL/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22"><img src="https://img.shields.io/github/issues/carlossruuizz/apisloL/help%20wanted?style=flat-square&color=008672&label=help%20wanted" alt="Help Wanted" /></a> <a href="./CONTRIBUTING.md"><img src="https://img.shields.io/badge/contributors-welcome-brightgreen?style=flat-square" alt="Contributors Welcome" /></a> |

[Spanish/Español](./docs/README.es.md) — [Chinese/中文](./docs/README.zh.md) ⁞ [Brainfuck/BF](./docs/README.bf.md)

</div>

<img align="right" src="https://i.imgur.com/H0Ta4fj.png" height="250px" alt="apislol logo">

**Lightweight Python HTTP API framework** with zero external dependencies. Production-ready security middleware stack including rate limiting, bot blocking, CORS, honeypot protection, and multi-format response serialization.

**apislol provides:** *Rate limiting*, *Bot blocking*, *CORS*, *Honeypot traps*, *IP/UA blocklists*, *API key auth*, *Cooldown*, *Response transforms (JSON, YAML, XML, CSV, TOML, HTML)*, and more.

> [!NOTE]
> Requires Python 3.10+. No external dependencies — built entirely on the Python standard library.

## Quick Start

```bash
pip install git+https://github.com/carlossruuizz/apislol.git
```

```python
import apis as alolapi = alol.engine()

api.start( config={
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
from apislol.response import Responserouter = Router()@router.get("/{id}")
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

</div>

---

## Contributing

We welcome contributions from developers of all skill levels. Whether you're fixing a typo, adding documentation, or implementing new features, your help is appreciated.

### Good First Issues

New to open source or the project? Start here:

<div align="center">

[![Good First Issues](https://img.shields.io/github/issues/carlossruuizz/apisloL/good%20first%20issue?style=for-the-badge&color=7057ff&label=GOOD%20FIRST%20ISSUES)](https://github.com/carlossruuizz/apisloL/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

</div>
