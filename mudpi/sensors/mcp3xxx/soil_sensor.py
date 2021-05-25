import sys

from adafruit_mcp3xxx.analog_in import AnalogIn

from logger.Logger import Logger, LOG_LEVEL
from sensors.mcp3xxx.sensor import Sensor



#  Tested using Sun3Drucker Model SX239
# Wet Water = 287
# Dry Air = 584
AirBounds = 43700
WaterBounds = 13000
intervals = int((AirBounds - WaterBounds) / 3)


class SoilSensor(Sensor):

    def __init__(self, pin, mcp, name=None, key=None, redis_conn=None):
        super().__init__(pin, name=name, key=key, mcp=mcp,
                         redis_conn=redis_conn)
        return

    def init_sensor(self):
        self.topic = AnalogIn(self.mcp, Sensor.PINS[self.pin])

    def read(self):
        resistance = self.read_pin()
        moistpercent = (
                               (resistance - WaterBounds) / (
                               AirBounds - WaterBounds)
                       ) * 100
        if moistpercent > 80:
            moisture = 'Very Dry - ' + str(int(moistpercent))
        elif 80 >= moistpercent > 45:
            moisture = 'Dry - ' + str(int(moistpercent))
        elif 45 >= moistpercent > 25:
            moisture = 'Wet - ' + str(int(moistpercent))
        else:
            moisture = 'Very Wet - ' + str(int(moistpercent))
        # print("Resistance: %d" % resistance)
        # TODO: Put redis store into sensor worker
        self.r.set(self.key,
                   resistance)
        # TODO: CHANGE BACK TO 'moistpercent' (PERSONAL CONFIG)

        Logger.log(LOG_LEVEL["debug"], "moisture: {0}".format(moisture))
        return resistance
