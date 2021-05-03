import threading
import logging
import asyncio
import traceback
import queue
from kasa import SmartBulb, Discover

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rather than using the temperature selector which I find has a not-very-useful
# range, I prefer having a constant orange bulb which I oversaturate to white during
# the day.
COLOR_HUE = 20


async def find_device(alias: str):
    logger.info("Searching for device...")
    devices = await Discover.discover()
    for addr, dev in devices.items():
        if type(dev) is SmartBulb and dev.alias == alias:
            logger.info(f"Device found @ {addr}")
            return dev
    
    logger.error(f"No device found for alias {alias}")
    return None


class BulbService(threading.Thread):
    def __init__(self, alias: str):
        super().__init__()
        self.alias = alias
        self.daemon = True
        self.start()
        self.setting_q = queue.Queue()
    
    def run(self):
        asyncio.run(self._runner())

    async def _runner(self):
        retry_time = 1
        while True:
            try:
                bulb = await find_device(self.alias)
                assert bulb is not None

                retry_time = 1
            
                await self._update_loop(bulb)
            except:
                logger.error(traceback.format_exc())
                logger.error(f"An error occured, retrying in {retry_time} seconds")
                await asyncio.sleep(retry_time)
                if retry_time < 16:
                    retry_time *= 2
    
    async def _update_loop(self, bulb):
        while True:
            if self.setting_q.empty():
                await asyncio.sleep(0.5)
                continue

            toggle = False
            saturation = None
            brightness = None
            while not self.setting_q.empty():
                ud = self.setting_q.get()
                if "toggle" in ud:
                    toggle = not toggle
                if "saturation" in ud:
                    saturation = ud["saturation"]
                if "brightness" in ud:
                    brightness = ud["brightness"]

            logger.info(f"Setting ({toggle}, {saturation}, {brightness})")
            await bulb.update()
            
            if saturation is not None:
                await bulb.set_hsv(COLOR_HUE, saturation, bulb.hsv[2])
            if brightness is not None:
                await bulb.set_hsv(COLOR_HUE, bulb.hsv[1], brightness)
            if toggle:
                if bulb.is_on:
                    await bulb.turn_off()
                else:
                    await bulb.turn_on()

    def toggle_power(self):
        self.setting_q.put({"toggle": True})
    
    def set_saturation(self, val: int):
        self.setting_q.put({"saturation": val})
    
    def set_brightness(self, val: int):
        self.setting_q.put({"brightness": val})
