# Better Wake-On-LAN intergration

The standard Wake-On-LAN integration is very limited in configuration possibilities and has questionable update logic.

This integration simplifies script invocation and adds a delayed status update. This means that the status indicator will not suddenly become off immediately after switching on due to the device taking a long time to start up

## Configuration 

Example

```yaml
switch:
  - platform: better_wol
    name: gaming_station
    host: gaming-station
    mac: !secret gaming_station_mac
    turn_off_script:
      ssh -i /config/.ssh/id_rsa mishamyrt@192.168.1.148 "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
```
