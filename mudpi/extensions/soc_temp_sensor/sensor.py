""" 
    SOC Sensor Interface
    Returns the SOC temperature
"""
import subprocess
import os
from mudpi.logger.Logger import Logger, LOG_LEVEL
from mudpi.extensions import BaseInterface
from mudpi.extensions.sensor import Sensor


class Interface(BaseInterface):

    def load(self, config):
        """ Load soc sensor component from configs """
        sensor = SOCTempSensor(self.mudpi, config)
        self.add_component(sensor)
        return True


class SOCTempSensor(Sensor):
    """ Properties """
    @property
    def id(self):
        """ Return a unique id for the component """
        return self.config['key']

    @property
    def name(self):
        """ Return the display name of the component """
        return self.config.get('name') or f"{self.id.replace('_', ' ').title()}"
    
    @property
    def state(self):
        """ Return the state of the component (from memory, no IO!) """
        return self._state

    @property
    def classifier(self):
        """ Classification further describing it, effects the data formatting """
        return self.config.get('classifier', "temperature" )

    """ Methods """
    def update(self):
        """ Get SOC Temp """
        completed_process = subprocess.run(["vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'"], shell=True, encoding='utf-8', capture_output=True)
        self._state = float(completed_process.stdout)

        return True