# Temp & Humidity Monitor (Project 08-001)

## Overview
This repository provides two step-by-step Python scripts for learning how to read temperature and humidity data from a DHT11 sensor on a Raspberry Pi. The project requirements are documented in `08-001_温湿度モニタリングアプリ_要件定義書.md`, and operational rules are defined in `CLAUDE.md` and `AGENTS.md`.

## Hardware & Safety
- Raspberry Pi 5 with Raspberry Pi OS
- DHT11 sensor module wired to GPIO4 (physical pin 7)
- 4.7 kΩ pull-up resistor when required by the sensor module
- Jumper wires and a stable 5 V power supply

**Safety notice:** Always disconnect power before modifying wiring, verify voltage levels before connecting new peripherals, and avoid touching live GPIO pins to prevent short circuits.

## Software Requirements
- Python 3.9+
- `adafruit-circuitpython-dht` (installs `adafruit_dht` and `board` modules)

```bash
python3 -m pip install --upgrade pip
python3 -m pip install adafruit-circuitpython-dht
```

## Usage
Run the scripts from the project root so relative paths resolve correctly.

### 1. Console Monitor (`dht11_basic.py`)
Reads the DHT11 sensor every 2 seconds and prints the readings in Celsius, Fahrenheit, and percent humidity.

```bash
python3 dht11_basic.py
```
Use `Ctrl+C` to exit; the script releases the sensor on shutdown.

### 2. CSV Logger (`dht11_logger.py`)
Creates a daily CSV file named `temperature_humidity_YYYY-MM-DD.csv`, then logs a reading every 60 seconds with a timestamp.

```bash
python3 dht11_logger.py
```
Each run appends to the same-day file. Ensure the working directory remains writable and monitor available disk space for long-term logging.

## Troubleshooting
- **Read errors:** Occasional `RuntimeError` messages are expected; the scripts continue after the next interval. Persistent failures usually indicate wiring or power issues.
- **Module import errors:** Re-run the installation command or confirm you are using Python 3.
- **CSV not created:** Confirm the logger script has write permission in the working directory and that the system clock is set correctly.

## Further Reading
Consult the requirement specification and rule documents for detailed expectations, coding standards, and operational procedures:
- `08-001_温湿度モニタリングアプリ_要件定義書.md`
- `CLAUDE.md`
- `AGENTS.md`
- `python_coding_guidelines.md`
- `COMMENT_STYLE_GUIDE.md`
