# Temp & Humidity Monitor (Project 08-001)

## Overview
This project provides a Python script for learning how to read temperature and humidity data from a DHT11 sensor on a Raspberry Pi 5. The project requirements are documented in `08-001_温湿度モニタリングアプリ_要件定義書.md`, and operational rules are defined in `CLAUDE.md` and `AGENTS.md`.

## Hardware & Safety
- Raspberry Pi 5 with Raspberry Pi OS (Bookworm or later)
- DHT11 sensor module wired to GPIO4 (physical pin 7)
- 4.7 kΩ pull-up resistor when required by the sensor module
- Jumper wires and a stable 5 V power supply

**Safety notice:** Always disconnect power before modifying wiring, verify voltage levels before connecting new peripherals, and avoid touching live GPIO pins to prevent short circuits.

## Software Requirements
- Python 3.9+
- Virtual environment (required on Raspberry Pi OS Bookworm)
- Libraries: `adafruit-blinka`, `adafruit-circuitpython-dht`, `lgpio`

### Raspberry Pi 5 Library Constraints
Raspberry Pi 5 uses a new GPIO chip (RP1), which means traditional libraries like `Adafruit_DHT` and `RPi.GPIO` do not work. This project uses `adafruit-circuitpython-dht` with `adafruit-blinka` (CircuitPython compatibility layer) and `lgpio` for GPIO control.

Despite the "CircuitPython" name, these libraries work with standard Python (CPython) on Raspberry Pi.

### Installation

```bash
# Install system packages
sudo apt install -y python3-pip python3-venv libgpiod3 swig liblgpio-dev

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python libraries
pip install adafruit-blinka adafruit-circuitpython-dht lgpio
```

For detailed setup instructions, see `SETUP_GUIDE.md`.

## Usage
Activate the virtual environment before running the script:

```bash
source venv/bin/activate
```

### Console Monitor (`dht11_basic.py`)
Reads the DHT11 sensor every 2 seconds and prints the readings in Celsius, Fahrenheit, and percent humidity.

```bash
python3 dht11_basic.py
```

Use `Ctrl+C` to exit; the script releases the sensor on shutdown.

## Troubleshooting
- **Read errors:** Occasional `RuntimeError` messages (e.g., "Checksum did not validate") are expected; the script continues after the next interval. Persistent failures usually indicate wiring or power issues.
- **Module import errors:** Ensure the virtual environment is activated and libraries are installed.
- **Permission errors:** Add your user to the gpio group: `sudo usermod -aG gpio $USER` and re-login.

## Further Reading
Consult the requirement specification and rule documents for detailed expectations, coding standards, and operational procedures:
- `08-001_温湿度モニタリングアプリ_要件定義書.md`
- `SETUP_GUIDE.md`
- `CLAUDE.md`
- `python_coding_guidelines.md`
- `COMMENT_STYLE_GUIDE.md`
