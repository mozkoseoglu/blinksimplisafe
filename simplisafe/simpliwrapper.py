import config
import logging
# Simplisafe
import asyncio
from aiohttp import ClientSession
from simplipy import API


class SimpliSafeWrapper:
    def __init__(self):
        self.system = self.__get_ss()

    async def __get_ss_connection(self):
        """Create the aiohttp session and run."""
        async with ClientSession() as websession:
            self.websession = websession
            try:
                self.simplisafe = await API.login_via_credentials(config.simplisafe['username'], config.simplisafe['password'], websession)
                return await self.simplisafe.get_systems()
            except Exception as e:
                logging.error('Error in getting simplisafe ')
                raise e

    def __get_ss(self):
        systems = asyncio.get_event_loop().run_until_complete(self.__get_ss_connection())
        return self.__filter_system(systems)

    def __filter_system(self, systems):
        """Filter relevant system"""
        _systems = list(filter(lambda x: x.address ==
                               config.simplisafe['address'], systems))
        if len(_systems) != 1:
            raise AttributeError(
                'Cannot find address, make sure your configuration is set up correctly')
        else:
            system = _systems[0]
        return system

    async def refresh_ss(self):
        """Refresh simplisafe's settings"""
        async with ClientSession() as websession:
            # TODO: remove continous login
            self.simplisafe = await API.login_via_credentials(config.simplisafe['username'], config.simplisafe['password'], websession)
            systems = await self.simplisafe.get_systems()
            self.system = self.__filter_system(systems)
            await self.system.update(refresh_location=False, cached=True)

    def get_simplisafe_status(self):
        """Get simplisafe's status"""
        return self.system.state.name

    def get(self):
        return self.system
