# Simplisafe & Blink (XT) Integration & Monitoring
This repository connects the **SimpliSafe** Home Monitoring System with Amazon's wireless indoor and outdoor camera system, **Blink**.

This project is based on [simplisafe-python](https://github.com/bachya/simplisafe-python) by *baya* and [blinkpy](https://github.com/fronzbot/blinkpy) by *froznbot*.

## Disclaimer
"Blink Wire-Free HS Home Monitoring & Alert Systems" is a trademark owned by Immedia Inc., see www.blinkforhome.com for more information. I am in no way affiliated with Blink, nor Immedia Inc.

SimpliSafe and SimpliCam is a trademark owned by SimpliSafe, Inc., see www.simplisafe.com for more information. I am in no way affiliated with SimpliSafe, nor  SimpliSafe, Inc.

## Goal of the project
It aims to solve these common problems I have with running 2 disparate systens:
* The SimpliSafe alarm and Blink XT cameras need to be indepedently activated; Disarming/arming one system does not affect the other - this allows to sync both up
* Blink cameras running low on battery is only shown as a simple **OK** indicator on the iOS App - this allows for closer monitoring, custom alarms, and to extract more details
* Recorded videos are only available by manually downloading them via the iOS app - this solves the problem by downloading videos automatically

