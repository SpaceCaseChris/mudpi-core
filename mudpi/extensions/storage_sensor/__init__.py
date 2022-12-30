""" 
    RPi Storage Sensor 
    Displays the used and total storage as well as a percentage representation of the same.
"""
from mudpi.extensions import BaseExtension


class Extension(BaseExtension):
    namespace = 'storage_sensor'
    update_interval = 60
    
