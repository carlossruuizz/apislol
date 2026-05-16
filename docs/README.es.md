<div align="center">
<img src="https://i.imgur.com/Ytw0dW6.png" />

| <a href="https://github.com/carlossruuizz/apislol"><img src="https://img.shields.io/badge/version-1.0.0-f2c94c?style=flat-square" alt="Versión" /></a> <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-f2c94c?style=flat-square" alt="Python" /></a> <a href="../LICENSE"><img src="https://img.shields.io/badge/licencia-MIT-f2c94c?style=flat-square" alt="Licencia" /></a> <a href="https://github.com/carlossruuizz/apislol/stargazers"><img src="https://img.shields.io/github/stars/carlossruuizz/apislol?style=flat-square&color=f2c94c" alt="Estrellas" /></a> |
|---|

</div>

<img align="right" src="https://i.imgur.com/H0Ta4fj.png" height="250px" alt="apislol logo">

**Construye APIs HTTP en Python puro** sin dependencias externas y con el mínimo código posible. Un framework ligero con un stack de middleware de seguridad integrado, enrutamiento flexible y transformaciones de respuesta en múltiples formatos.

**apislol incluye:** Rate limiting, Bloqueo de bots, CORS, Trampas honeypot, Listas negras de IP/UA, Autenticación por API key, Cooldown, Transformaciones de respuesta (JSON, YAML, XML, CSV, TOML, HTML), y más.

> [!NOTE]
> Requiere Python 3.10+. Sin dependencias externas — construido íntegramente sobre la biblioteca estándar de Python.

## Inicio rápido

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
<summary><b><code>Desarrollo</code></b></summary>

### Configuración

```bash
git clone https://github.com/carlossruuizz/apislol.git
cd apislol
```

### Ejemplo de handler

```python
from apislol.router import Router
from apislol.request import Request
from apislol.response import Response

router = Router()

@router.get("/{id}")
def obtener_usuario(request: Request) -> Response:
    return Response.json({"id": request.path_params["id"]})
```

</details>

> [!TIP]
> Devuelve un `dict` simple desde cualquier handler — apislol lo serializa automáticamente según la cabecera `Accept` o el sufijo de la URL (p. ej. `/users/1.yaml`).

---

<table width="100%">
<tr>
<td valign="top" width="50%">

### Middleware

<div align="center">

| Componente | Comportamiento |
|-----------|----------------|
| `RateLimiter` | Límite de peticiones por IP con ventana deslizante |
| `BotBlocker` | Bloquea bots conocidos, crawlers de IA y navegadores headless |
| `IPFilter` | Bloquea/permite IPs y rangos CIDR |
| `UaBlocklist` | Patrones regex personalizados de User-Agent |
| `CorsMiddleware` | Inyecta cabeceras CORS según la configuración |
| `HoneypotMiddleware` | Banea IPs que acceden a rutas trampa |
| `ApiKeyMiddleware` | Validación de clave por cabecera o parámetro de consulta |
| `CooldownMiddleware` | Retraso por IP tras errores repetidos |
| `AllowedHosts` | Valida la cabecera `Host` |

</div>
</td>
<td valign="top" width="50%">

### Transformaciones de respuesta

| Formato | Content-Type |
|---------|-------------|
| `json` | `application/json` |
| `yaml` | `application/x-yaml` |
| `toml` | `application/toml` |
| `xml` | `application/xml` |
| `csv` | `text/csv` |
| `html` | `text/html` |

Se resuelven automáticamente mediante la cabecera `Accept` o el sufijo de la URL.
Registra formatos personalizados con `engine.transforms.register()`.

</td>
</tr>
<tr>
<td valign="top" colspan="2">

### Enrutamiento

Las rutas asocian un prefijo de ruta a un archivo `.py` de handler. Cada archivo expone un `router` (una instancia de `Router`) con funciones handler decoradas.

```python
api.start(config={
    "routing": {
        "/users":    "./handlers/users.py",
        "/products": "./handlers/products.py",
    }
})
```

Los parámetros dinámicos de ruta usan la sintaxis `{param}`:

```python
@router.get("/{id}")
def obtener_elemento(request: Request) -> dict:
    return {"id": request.path_params["id"]}
```

</td>
</tr>
</table>

---

<div align="center">

**Creado por <a href="https://github.com/carlossruuizz">carlossruuizz</a>** · [README.md](../README.md) · [README.zh.md](./README.zh.md)

</div>
