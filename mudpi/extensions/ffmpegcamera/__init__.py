""" 
    Ffmpeg Camera Extension
    Connect to any attached camera
    with ffmpeg. 
"""
from mudpi.extensions import BaseExtension


class Extension(BaseExtension):
    namespace = 'ffmpegcamera'
    update_interval = 1
 