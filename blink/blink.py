import config
import logging
# Blink
from blinkpy import blinkpy


class BlinkWrapper:
    def __init__(self):
        self.blink = blinkpy.Blink(
            username=config.blink['username'], password=config.blink['password'], refresh_rate=config.blink['refresh_rate'])
        self.blink.start()

    def refresh(self):
        self.blink.refresh(force_cache=False)

    def get_armed_status(self):
        """Get the status of the Blink (XT) system (armed/disarmed)"""
        status = self.blink.sync[config.blink['system_name']].arm
        logging.info('Blink is armed: {status}'.format(status=status))
        return status

    def set_armed_status(self, status):
        """Set the status of the Blink (XT) system (armed/disarmed)"""
        if self.get_armed_status() != status:
            self.blink.sync[config.blink['system_name']].arm = status
            logging.info(
                'Blink\'s is now armed: {status}'.format(status=status))
        else:
            logging.info('Blink\s status will be unchanged, doing nothing')

    def get_battery_alerts(self):
        """Get battery alerts"""
        logging.info('Blink camera status:')
        for name, camera in self.blink.cameras.items():
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

    def get(self):
        return self.blink
