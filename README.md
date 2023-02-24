# Assisted Power-On-LAN

To set up a computer power management scenario (including shutdown) via the standard Wake-On-LAN integration takes a lot of effort.

Assisted WoL offers an option where you additionally run a small application on the computer that listens for requests from the integration and puts it to sleep if a request comes in.

## Configuration 

Example

```yaml
switch:
  - platform: assisted_pol
    name: gaming_station
    host: Gaming-Station.local
    mac: !secret gaming_station_mac
```
