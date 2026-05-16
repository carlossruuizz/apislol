"""
Recommend handler — returns an Arduino board recommendation based on experience level.
Data is self-contained; no external API key required.
"""

from apislol.router import Router
from apislol.request import Request
from apislol.response import Response

router = Router()

BOARDS: list[dict] = [
    {
        "id": "uno",
        "name": "Arduino Uno R3",
        "level": "beginner",
        "price_usd": 27,
        "image": "https://store.arduino.cc/cdn/shop/files/A000066_03.front_1000x750.jpg",
        "store": "https://store.arduino.cc/products/arduino-uno-rev3",
        "description": "The classic starting point. Huge community, endless tutorials, and forgiving to mistakes.",
        "specs": {"flash_kb": 32, "ram_kb": 2, "clock_mhz": 16, "pins": 14},
        "tags": ["beginner", "education", "prototyping"],
    },
    {
        "id": "nano",
        "name": "Arduino Nano",
        "level": "beginner",
        "price_usd": 24,
        "image": "https://store.arduino.cc/cdn/shop/files/A000005_03.front_1000x750.jpg",
        "store": "https://store.arduino.cc/products/arduino-nano",
        "description": "Compact Uno-compatible board. Great for breadboard projects where space matters.",
        "specs": {"flash_kb": 32, "ram_kb": 2, "clock_mhz": 16, "pins": 22},
        "tags": ["beginner", "compact", "breadboard"],
    },
    {
        "id": "mega",
        "name": "Arduino Mega 2560",
        "level": "intermediate",
        "price_usd": 48,
        "image": "https://store.arduino.cc/cdn/shop/files/A000067_03.front_1000x750.jpg",
        "store": "https://store.arduino.cc/products/arduino-mega-2560-rev3",
        "description": "More pins, more memory. Ideal for complex projects like 3D printers or large sensor arrays.",
        "specs": {"flash_kb": 256, "ram_kb": 8, "clock_mhz": 16, "pins": 54},
        "tags": ["intermediate", "robotics", "3d-printing"],
    },
    {
        "id": "mkr_wifi",
        "name": "Arduino MKR WiFi 1010",
        "level": "intermediate",
        "price_usd": 38,
        "image": "https://store.arduino.cc/cdn/shop/files/ABX00023_03.front_1000x750.jpg",
        "store": "https://store.arduino.cc/products/arduino-mkr-wifi-1010",
        "description": "Built-in WiFi and low power design. Perfect for IoT projects and connected devices.",
        "specs": {"flash_kb": 256, "ram_kb": 32, "clock_mhz": 48, "pins": 22},
        "tags": ["intermediate", "iot", "wifi", "low-power"],
    },
    {
        "id": "portenta",
        "name": "Arduino Portenta H7",
        "level": "advanced",
        "price_usd": 103,
        "image": "https://store.arduino.cc/cdn/shop/files/ABX00042_03.front_1000x750.jpg",
        "store": "https://store.arduino.cc/products/portenta-h7",
        "description": "Dual-core ARM Cortex-M7/M4. Industrial-grade for machine learning, vision, and edge computing.",
        "specs": {"flash_kb": 2048, "ram_kb": 1024, "clock_mhz": 480, "pins": 80},
        "tags": ["advanced", "ml", "vision", "industrial"],
    },
    {
        "id": "giga",
        "name": "Arduino GIGA R1 WiFi",
        "level": "advanced",
        "price_usd": 65,
        "image": "https://store.arduino.cc/cdn/shop/files/ABX00063_03.front_1000x750.jpg",
        "store": "https://store.arduino.cc/products/giga-r1-wifi",
        "description": "High-performance dual-core with WiFi, audio, and display support. The Mega for the modern era.",
        "specs": {"flash_kb": 2048, "ram_kb": 1024, "clock_mhz": 480, "pins": 76},
        "tags": ["advanced", "wifi", "audio", "display"],
    },
]

LEVEL_MAP = {
    "0": "beginner", "1": "beginner",
    "2": "intermediate", "3": "intermediate",
    "4": "advanced", "5": "advanced",
    "beginner": "beginner",
    "intermediate": "intermediate",
    "advanced": "advanced",
}


@router.get("/")
def recommend(request: Request) -> Response:
    """
    Query params:
        level   — 0-5 numeric or beginner/intermediate/advanced
        tag     — optional filter tag (e.g. iot, wifi, robotics)
    """
    raw_level = str(request.query.get("level", "0")).lower().strip()
    tag_filter = str(request.query.get("tag", "")).lower().strip()

    level = LEVEL_MAP.get(raw_level, "beginner")

    results = [b for b in BOARDS if b["level"] == level]

    if tag_filter:
        results = [b for b in results if tag_filter in b["tags"]]

    if not results:
        results = [b for b in BOARDS if b["level"] == level]

    return Response.json({
        "level": level,
        "tag": tag_filter or None,
        "count": len(results),
        "boards": results,
    })


@router.get("/levels")
def levels(request: Request) -> Response:
    """Returns available experience levels and tags."""
    all_tags = sorted({tag for b in BOARDS for tag in b["tags"]})
    return Response.json({
        "levels": ["beginner", "intermediate", "advanced"],
        "tags": all_tags,
    })
