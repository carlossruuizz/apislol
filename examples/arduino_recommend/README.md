<div align="center">
<img src="https://i.imgur.com/Ytw0dW6.png" />

| <a href="https://github.com/carlossruuizz/apislol"><img src="https://img.shields.io/badge/example-arduino__recommend-f2c94c?style=flat-square" alt="Example" /></a> <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-f2c94c?style=flat-square" alt="Python" /></a> <a href="https://store.arduino.cc"><img src="https://img.shields.io/badge/data-Arduino%20Store-f2c94c?style=flat-square" alt="Arduino" /></a> |
|---|

</div>

<img align="right" src="https://i.imgur.com/H0Ta4fj.png" height="200px" alt="apislol logo">

**arduino_recommend** — recommends an Arduino board based on your experience level (0–5) and optional tag filter.

No external API keys. All board data is self-contained in the handler.

## Run

```bash
cd examples/arduino_recommend
python main.py
```

Open `http://localhost:8082`, drag the slider, and optionally pick a tag.

## Structure

```
arduino_recommend/
├── main.py
├── handlers/
│   ├── recommend.py   GET /recommend?level=&tag=
│   └── static.py      serves HTML, CSS, JS
└── static/
    ├── index.html
    ├── styles/main.css
    └── js/app.js
```

## Endpoints

| Method | Path | Params | Description |
|--------|------|--------|-------------|
| `GET` | `/recommend` | `level=0-5`, `tag=` | Board recommendations |
| `GET` | `/recommend/levels` | — | Available levels and tags |

---

<div align="center">

**Built by <a href="https://github.com/carlossruuizz">Carlos Ruiz</a>** · <a href="../../README.md">apislol</a>

</div>
