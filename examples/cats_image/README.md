<div align="center">
<img src="https://i.imgur.com/Ytw0dW6.png" />

| <a href="https://github.com/carlossruuizz/apislol"><img src="https://img.shields.io/badge/example-cats__image-f2c94c?style=flat-square" alt="Example" /></a> <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-f2c94c?style=flat-square" alt="Python" /></a> <a href="https://thecatapi.com"><img src="https://img.shields.io/badge/data-The%20Cat%20API-f2c94c?style=flat-square" alt="Cat API" /></a> |
|---|

</div>

<img align="right" src="https://i.imgur.com/H0Ta4fj.png" height="200px" alt="apislol logo">

**cats_image** — a minimal apislol app that serves a random cat photo on every request.

Hits [The Cat API](https://thecatapi.com) (no API key needed), returns the image URL as JSON, and renders it in a clean dark-mode frontend.

## Run

```bash
cd examples/cats_image
python main.py
```

Open `http://localhost:8081` and click **New cat**.

## Structure

```
cats_image/
├── main.py
├── handlers/
│   ├── cat.py        GET /cat  →  random cat JSON
│   └── static.py     serves HTML, CSS, JS
└── static/
    ├── index.html
    ├── styles/main.css
    └── js/app.js
```

## Endpoint

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/cat` | Returns `{ id, url, width, height }` |

---

<div align="center">

**Built by <a href="https://github.com/carlossruuizz">Carlos Ruiz</a>** · <a href="../../README.md">apislol</a>

</div>
