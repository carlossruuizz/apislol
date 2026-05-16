<div align="center">
<img src="https://i.imgur.com/Ytw0dW6.png" />

| <a href="https://github.com/carlossruuizz/apislol"><img src="https://img.shields.io/badge/版本-1.0.0-f2c94c?style=flat-square" alt="版本" /></a> <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-f2c94c?style=flat-square" alt="Python" /></a> <a href="../LICENSE"><img src="https://img.shields.io/badge/许可证-MIT-f2c94c?style=flat-square" alt="许可证" /></a> <a href="https://github.com/carlossruuizz/apislol/stargazers"><img src="https://img.shields.io/github/stars/carlossruuizz/apislol?style=flat-square&color=f2c94c" alt="星标" /></a> |
|---|

</div>

<img align="right" src="https://i.imgur.com/H0Ta4fj.png" height="250px" alt="apislol logo">

**用纯 Python 构建 HTTP API**，零外部依赖，极简样板代码。一个轻量级框架，内置安全中间件栈、灵活路由和多格式响应转换。

**apislol 提供：** 速率限制、机器人拦截、CORS、蜜罐陷阱、IP/UA 黑名单、API 密钥认证、冷却机制、响应转换（JSON、YAML、XML、CSV、TOML、HTML）等。

> [!NOTE]
> 需要 Python 3.10+。无外部依赖 — 完全基于 Python 标准库构建。

## 快速开始

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
<summary><b><code>开发</code></b></summary>

### 环境配置

```bash
git clone https://github.com/carlossruuizz/apislol.git
cd apislol
```

### 处理器示例

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
> 从任意处理器返回普通 `dict` — apislol 会根据 `Accept` 请求头或 URL 后缀自动序列化（例如 `/users/1.yaml`）。

---

<table width="100%">
<tr>
<td valign="top" width="50%">

### 中间件

<div align="center">

| 组件 | 行为 |
|------|------|
| `RateLimiter` | 基于滑动窗口的每 IP 请求限制 |
| `BotBlocker` | 拦截已知机器人、AI 爬虫和无头浏览器 |
| `IPFilter` | 封锁/允许 IP 地址和 CIDR 范围 |
| `UaBlocklist` | 自定义 User-Agent 正则表达式模式 |
| `CorsMiddleware` | 按配置注入 CORS 响应头 |
| `HoneypotMiddleware` | 封禁访问陷阱路径的 IP |
| `ApiKeyMiddleware` | 通过请求头或查询参数验证密钥 |
| `CooldownMiddleware` | 重复错误后对 IP 施加延迟 |
| `AllowedHosts` | 验证 `Host` 请求头 |

</div>
</td>
<td valign="top" width="50%">

### 响应转换

| 格式 | Content-Type |
|------|-------------|
| `json` | `application/json` |
| `yaml` | `application/x-yaml` |
| `toml` | `application/toml` |
| `xml` | `application/xml` |
| `csv` | `text/csv` |
| `html` | `text/html` |

通过 `Accept` 请求头或 URL 后缀自动解析。
使用 `engine.transforms.register()` 注册自定义格式。

</td>
</tr>
<tr>
<td valign="top" colspan="2">

### 路由

路由将路径前缀映射到处理器 `.py` 文件。每个文件暴露一个 `router`（`Router` 实例），其中包含带装饰器的处理函数。

```python
api.start(config={
    "routing": {
        "/users":    "./handlers/users.py",
        "/products": "./handlers/products.py",
    }
})
```

动态路径参数使用 `{param}` 语法：

```python
@router.get("/{id}")
def get_item(request: Request) -> dict:
    return {"id": request.path_params["id"]}
```

</td>
</tr>
</table>

---

<div align="center">

**由 <a href="https://github.com/carlossruuizz">carlossruuizz</a> 构建** · [README.md](../README.md) · [README.es.md](./README.es.md)

</div>
