""" 
    Storage Sensor Interface
    Returns the used and total storage and a percentage representation of the same
"""
import subprocess
from mudpi.logger.Logger import Logger, LOG_LEVEL
from mudpi.extensions import BaseInterface
from mudpi.extensions.sensor import Sensor


class Interface(BaseInterface):

    def load(self, config):
        """ Load storage sensor component from configs """
        sensor = StorageSensor(self.mudpi, config)
        self.add_component(sensor)
        return True


class StorageSensor(Sensor):
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

    """ Methods """
    def update(self):
        """ Get Storage Info """
        completed_process = subprocess.run(["df -h | awk '/%/ && NR > 1 && NR < 3 {print $3 \"/\" $2 \" (\" $5 \")\"}'"], shell=True, encoding='utf-8', capture_output=True)
        reading = str(completed_process.stdout)
        self._state = reading

        return True