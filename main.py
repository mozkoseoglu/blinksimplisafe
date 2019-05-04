import config
from blinkpy import blinkpy


__author__ = "Christian Hollinger (otter-in-a-suit)"
__version__ = "0.1.0"
__license__ = "GNU GPLv3"


def get_blink():
    blink = blinkpy.Blink(
        username=config.blink['username'], password=config.blink['password'], refresh_rate=config.blink['refresh_rate'])
    blink.start()
    return blink


def get_armed_status(blink):
    return blink.sync[config.blink['system_name']].arm


def get_battery_alerts(blink):
    for name, camera in blink.cameras.items():
        #print(name)
        #print(camera.attributes)
        if camera.attributes['battery'] <= config.blink['battery_threshold']:
            print('Battery in camera {id} is at {battery}, below threshold of {threshold}!'
                  .format(id=camera.attributes['name'],
                          battery=camera.attributes['battery'],
                          threshold=config.blink['battery_threshold'])
                  )
        else:
            print('Camera {id}\'s battery status is OK at {battery}'.format(id=camera.attributes['name'],
                                                                            battery=camera.attributes['battery']))


def main():
    print('Starting main')
    blink = get_blink()
    get_battery_alerts(blink)

if __name__ == "__main__":
    main()
