import config
# Simplisafe
import asyncio
from aiohttp import ClientSession
# Python
from enum import Enum
import logging
import time
import threading
# Modules
from simplisafe.simpliwrapper import SimpliSafeWrapper
from blink.blink import BlinkWrapper

__author__ = "Christian Hollinger (otter-in-a-suit)"
__version__ = "0.1.0"
__license__ = "MIT"


def arm_blink_if_ss(system, blink):
    """Arm the blink system if SS is away or home"""
    ss_status = system.get_simplisafe_status()
    if ss_status == 'away' or ss_status == 'home':
        logging.info('Simplisafe system is armed')
        blink.set_armed_status(True)
    elif ss_status == 'off':
        logging.info('Simplisafe system is off')
        blink.set_armed_status(False)
    else:
        logging.error('Error in checking simplisafe status')
        raise ValueError('Simplisafe system state is undefined')


def scheduled_run(system, blink):
    """Re-runs this every check_interval_in_s seconds"""
    # Refresh
    blink.refresh()
    asyncio.new_event_loop().run_until_complete(system.refresh_ss())
    # Run
    logging.info('Running loop at {thyme}'.format(thyme=time.ctime()))
    run_main_loop(system, blink)
    # Repeat
    threading.Timer(config.schedule['check_interval_in_s'], scheduled_run, [
                    system, blink]).start()


def run_main_loop(system, blink):
    """Runs all functions, depending on the configurations"""
    if config.modes['use_arm_sync'] == True:
        # Arm Blink if SS is armed
        arm_blink_if_ss(system, blink)
    if config.modes['use_battery_check'] == True:
        # Get battery
        blink.get_battery_alerts()

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
    # Get Blink
    blink = BlinkWrapper()
    # Get Simplisafe
    system = SimpliSafeWrapper()

    # Scheduling
    if config.schedule['use_schedule'] is True:
        # Run in schedule
        logging.info('Running in schedule...')
        scheduled_run(system, blink)
    else:
        # Run once
        logging.info('Running once...')
        run_main_loop(system, blink)


if __name__ == "__main__":
    main()
