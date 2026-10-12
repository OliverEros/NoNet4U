# NoNet4U

A command-line tool for shaping traffic on your local network. Scan your LAN, see who is on it, then limit, block or free individual devices using ARP spoofing and a hierarchical token-bucket rate limiter.

Built in Python as a personal project to learn how networks, ARP and rate limiting work in practice.

![NoNet4U screenshot](https://i.imgur.com/Pj9Zdt2.png)

> **Legal and ethical notice:** This tool is for learning and for use **only on networks you own or have explicit permission to test**. ARP spoofing on a network you don't control is illegal in many jurisdictions and disrupts other people's connectivity. You are responsible for how you use it.

## Features

- **Network scan:** discover all devices currently on the LAN
- **Per-device bandwidth limits:** set speeds in familiar units (Mbit, Kbit, etc.)
- **Block and free:** cut a device off, or restore it, individually or for everyone at once
- **Status overview:** list scanned devices with their state (normal, limited, blocked)
- **Interactive CLI:** a continuous input loop, so you can run several commands in one session without restarting

## How it works

1. **Discovery:** the tool scans the local subnet to build a list of devices.
2. **Interception:** ARP spoofing places your machine between the selected devices and the gateway, so their traffic passes through it.
3. **Shaping:** a hierarchical token-bucket algorithm decides how much traffic each device may send at any moment, which enforces the speed limit you set.

## Requirements

- Python 3
- A packet-capable environment (typically Linux, and likely elevated privileges for raw sockets) <!-- confirm the supported OS and privilege requirements -->

Python packages:

| Package | Used for |
| --- | --- |
| [Click](https://click.palletsprojects.com/) | Command-line interface |
| [netaddr](https://netaddr.readthedocs.io/) | Address and subnet handling |
| [tqdm](https://tqdm.github.io/) | Progress bar during scans |
| ipaddress | Standard-library IP address handling |

## Installation

```bash
git clone https://github.com/OliverEros/NoNet4U.git
cd NoNet4U
pip install click netaddr tqdm
```

## Usage

Start the tool:

```bash
python NoNet4U.py
```

This opens an interactive prompt. Available commands:

| Command | Description |
| --- | --- |
| `scan` | Scan the LAN for available devices |
| `users` | Show scanned devices with their status (blocked, limited) |
| `limit -user <id> <speed>` | Limit a device by its ID, e.g. `5Mbit` or `500Kbit` |
| `limit all <speed>` | Limit every scanned device |
| `block -user <id>` | Block a single device |
| `block -all` | Block every scanned device |
| `free -user <id>` | Remove limits or blocks from a device |

<!-- confirm the exact syntax and speed format of each command above -->

### Example session

```text
> scan
> users
> limit -user 3 2Mbit
> block -user 5
> free -user 5
```

## Project structure

```text
NoNet4U/
├── NoNet4U.py      # Entry point; builds the menu and starts the CLI
├── CLI/            # Click-based command-line interface
├── Network/        # Scanning, ARP spoofing and token-bucket shaping
└── utilities.py    # Shared helper functions
```

The CLI uses a customised `@click.group` that supports a continuous input loop. State is held in a `Menu` object, which receives its parameters in the entry-point file (`NoNet4U.py`).

## Possible improvements

- Unit tests for the token-bucket logic
- Clean restoration of ARP tables on exit
- Packaging as an installable module with a `requirements.txt`

## License

<!-- add a licence, e.g. MIT, so others know how they may reuse the code -->
