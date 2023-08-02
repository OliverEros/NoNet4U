# NoNet4U
<img src =https://i.imgur.com/Pj9Zdt2.png align='center'>

Personal project I have created for learning purposes. The tool is intended to limit network traffic on your LAN using ARP spoofing and
Token-Bucket hierarchy. 
With it, you can scan the network for all the users on it. Speed can be allocated in different formats (Mbit, KBit, etc)

## Requirements:
- Python3

## Packages used:
- Click for implementing command-line interface
- ipaddress 
- tqdm (status bar)
- netaddr

## Arguments for CLI :
The CLI component is implemented using Click. The commands are grouped together using a tweaked version of @click.group that allows continous input loop.
In the group where all state data is held in the form of a 'Menu' object which receives its parameters in the entry-point file (NoNet4U.py)
| Argument | Comment |
| -------- | ------- |
| scan     | Scans LAN for available users |
| limit -user    | Limit a given user (derived by ID or all user (limit all) |
| block -user / block -all | Block a given or all user |
| free -user | Free user|
| users | Displays scanned users with status information (blocked, limited) |

