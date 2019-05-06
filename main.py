import config
# Blink
from blinkpy import blinkpy
# Simplisafe
import asyncio
from aiohttp import ClientSession
from simplipy import API
# Python
from enum import Enum
import logging

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
    logging.info('Blink is armed: {status}'.format(status=status))
    return status


def set_armed_status(blink, status):
    """Set the status of the Blink (XT) system (armed/disarmed)"""
    if get_armed_status(blink) != status:
        blink.sync[config.blink['system_name']].arm = status
        logging.info('Blink\'s is now armed: {status}'.format(status=status))
    else:
        logging.info('Blink\s status will be unchanged, doing nothing')


def get_battery_alerts(blink):
    """Get battery alerts"""
    logging.info('Blink camera status:')
    for name, camera in blink.cameras.items():
        # logging.info(name)
        # logging.info(camera.attributes)
        if camera.attributes['battery'] <= config.blink['battery_threshold']:
            logging.warn('Battery in camera {id} is at {battery}, below threshold of {threshold}!'
                         .format(id=camera.attributes['name'],
                                 battery=camera.attributes['battery'],
                                 threshold=config.blink['battery_threshold'])
                         )
        else:
            logging.info('Camera {id}\'s battery status is OK at {battery}'.format(id=camera.attributes['name'],
                                                                                   battery=camera.attributes['battery']))


def get_simplisafe_status(system):
    """Get simplisafe's status"""
    return system.state.name


def arm_blink_if_ss(system, blink):
    """Arm the blink system if SS is away or home"""
    ss_status = get_simplisafe_status(system)
    if ss_status == 'away' or ss_status == 'home':
        logging.info('Simplisafe system is armed')
        set_armed_status(blink, True)
    elif ss_status == 'off':
        logging.info('Simplisafe system is off')
        set_armed_status(blink, False)
    else:
        logging.error('Error in checking simplisafe status')
        raise ValueError('Simplisafe system state is undefined')


async def init():
    """Create the aiohttp session and run."""
    async with ClientSession() as websession:
        try:
            simplisafe = await API.login_via_credentials(config.simplisafe['username'], config.simplisafe['password'], websession)
            return (await simplisafe.get_systems(), get_blink())
        except Exception as e:
            logging.error('Error in getting simplisafe ')
            raise e


def main():
    # Configure logger
    logging.basicConfig(level=logging.INFO, 
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler(
            "{0}/{1}.log".format(config.logs['log_path'], 'blinksimplisafe')),
        logging.StreamHandler()
    ])

    logging.info('Synchronizing the systems...')
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
