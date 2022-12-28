""" 
    SOC Temp Sensor 
    Displays the SOC temperature
"""
from mudpi.extensions import BaseExtension


class Extension(BaseExtension):
    namespace = 'soc_temp_sensor'
    update_interval = 30
    
