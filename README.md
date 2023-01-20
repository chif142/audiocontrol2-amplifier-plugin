# hifiberry-os-amplifier-plugin
Plugin for HiFiBerryOS to control an external amplifier. 
It sets a Pin of the Raspberry Pi to high if music is played and set it low if the music is paused. 
A delay can be configured, so that the pin is only set to low after the music is paused for some time.

## Prerequisites
- Raspberry Pi 4 with HifiBerryOs

## Installation and usage
Save `apmlyfier.py` under `/data/ac2plugins/` and add the lines
```
[controller:amplifier.Amplifier]
out=<GPIO>
t=<delay>
```
to the file `/etc/audiocontrol2.conf`. 
GPIP is the Broadcom SOC channel of the controled pin (default is 16)
and delay is the time in seconds the music has been paused untill the pin is set to low (default is 60 seconds).
For the changes to take effect, the raspberry pi must be restarted

For more info about Hifiberry os and plugin in audiocontrol2 (the backend of the HifiBerryOs) see:

[HifiBerryOs](https://github.com/hifiberry/hifiberry-os)

[audiocontrol2](https://github.com/hifiberry/audiocontrol2)
