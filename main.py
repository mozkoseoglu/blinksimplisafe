import config
# Blink
from blinkpy import blinkpy
# Simplisafe
import asyncio
from aiohttp import ClientSession
from simplipy import API
from enum import Enum

__author__ = "Christian Hollinger (otter-in-a-suit)"
__version__ = "0.1.0"
__license__ = "MIT"


def get_blink():
    """Get the Blink object"""
    blink = blinkpy.Blink(
        username=config.blink['username'], password=config.blink['password'], refresh_rate=config.blink['refresh_rate'])
    blink.start()
    return blink


def get_armed_status(blink):
    """Get the status of the Blink (XT) system (armed/disarmed)"""
    status = blink.sync[config.blink['system_name']].arm
    print('Blink is armed: {status}'.format(status=status))
    return status


def set_armed_status(blink, status):
    """Set the status of the Blink (XT) system (armed/disarmed)"""
    if get_armed_status(blink) != status:
        blink.sync[config.blink['system_name']].arm = status
        print('Blink\'s is now armed: {status}'.format(status=status))
    else:
        print('Status will be unchanged, doing nothing')


def get_battery_alerts(blink):
    """Get battery alerts"""
    for name, camera in blink.cameras.items():
        # print(name)
        # print(camera.attributes)
        if camera.attributes['battery'] <= config.blink['battery_threshold']:
            print('Battery in camera {id} is at {battery}, below threshold of {threshold}!'
                  .format(id=camera.attributes['name'],
                          battery=camera.attributes['battery'],
                          threshold=config.blink['battery_threshold'])
                  )
        else:
            print('Camera {id}\'s battery status is OK at {battery}'.format(id=camera.attributes['name'],
                                                                            battery=camera.attributes['battery']))


def get_simplisafe_status(system):
    """Get simplisafe's status"""
    return system.state.name


def arm_blink_if_ss(system, blink):
    """Arm the blink system if SS is away or home"""
    ss_status = get_simplisafe_status(system)
    if ss_status == 'away' or ss_status == 'home':
        print('System is armed')
        set_armed_status(blink, True)
    elif ss_status == 'off':
        print('System is off')
        set_armed_status(blink, False)
    else:
        raise ValueError('System state is undefined')


async def init():
    """Create the aiohttp session and run."""
    async with ClientSession() as websession:
        try:
            simplisafe = await API.login_via_credentials(config.simplisafe['username'], config.simplisafe['password'], websession)
            return (await simplisafe.get_systems(), get_blink())
        except Exception as e:
            print('Error in getting simplisafe ')
            raise e


def main():
    print('Synchronizing the system...')
    # Get Simplisafe, Blink
    loop = asyncio.get_event_loop()
    systems, blink = loop.run_until_complete(init())
    # Filter relevant system
    _systems = list(filter(lambda x: x.address ==
                           config.simplisafe['address'], systems))
    if len(_systems) != 1:
        raise AttributeError(
            'Cannot find address, make sure your configuration is set up correctly')
    else:
        system = _systems[0]
    # Get battery
    get_battery_alerts(blink)
    # Arm Blink if SS is armed
    arm_blink_if_ss(system, blink)


if __name__ == "__main__":
    main()
