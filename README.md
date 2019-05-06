# Simplisafe™ & Blink (XT) Camera System Integration & Monitoring
This repository connects the **SimpliSafe** Home Monitoring System with Amazon's wireless indoor and outdoor camera system, **Blink**.

This project is based on [simplisafe-python](https://github.com/bachya/simplisafe-python) by *William Scanlon & Aaron Bach* and [blinkpy](https://github.com/fronzbot/blinkpy) by *Kevin Fronczak*.

## Disclaimer
"Blink Wire-Free HS Home Monitoring & Alert Systems" is a trademark owned by Immedia Inc., see www.blinkforhome.com for more information. I am in no way affiliated with Blink, nor Immedia Inc.

SimpliSafe and SimpliCam is a trademark owned by SimpliSafe, Inc., see www.simplisafe.com for more information. I am in no way affiliated with SimpliSafe, nor  SimpliSafe, Inc.

**USE THIS PROJECT AT YOUR OWN RISK - IT REQUIRES YOUR LOGIN FOR BOTH BLINK AND SIMPLISAFE - I TAKE NO RESPONSIBILITY FOR ANY DAMAGES**

## Goal of the project
It aims to solve these common problems I have with running 2 disparate systens:
* The SimpliSafe alarm and Blink XT cameras need to be indepedently activated; Disarming/arming one system does not affect the other - this allows to sync both up automatically. If your SimpliSafe System is in `home` or `away` mode, it will activate the `Blink` cameras.
* Blink cameras running low on battery is only shown as a simple **OK** indicator on the iOS App - this allows for closer monitoring, custom alarms, and to extract more details (*no automatic alerts implemented*)
* Recorded videos are only available by manually downloading them via the iOS app - this solves the problem by downloading videos automatically (*not implemented*)

## Requirements
You will need
* A SimpliSafe account (this *should* work with a basic plan - please feel free to test this)
* A Blink (XT) Account
* Python 3.7

## Configuration
Configure the `config.py` file by running
```
cp config.py_example config.py
vim config.py
```

And enter your SimpliSafe and Blink username and password.

The `blink.system_name` configuration can be found at the top of your Blink App. The `simplisafe.address` configuration can be taken from your SimpliSafe account page. 

These configurations ensure that only one system is in sync at the time. If you run multiple systems, you can run multiple instances of this tool.

## Start
`python main.py`

The script can be run periodically via a cronjob. The tool itself does not run an internal loop on purpose, so it allows for more granular scheduling.

## ToDo
* Add unit tests
* Add monitoring for camera battery status
* Add automatic downloads for Blink

## License
[MIT](./LICENSE.md)