""" 
    FFMpeg Camera Interface
    Connects to any supported camera
    via FFMpeg.
"""
import os
import subprocess
from mudpi.exceptions import ConfigError
from mudpi.extensions import BaseInterface
from mudpi.extensions.camera import Camera
from mudpi.logger.Logger import Logger, LOG_LEVEL

class Interface(BaseInterface):

    def load(self, config):
        camera = FFMpegCamera(self.mudpi, config)
        if camera:
            self.add_component(camera)
        return True

    def validate(self, config):
        """ Validate the camera config """
        if not isinstance(config, list):
            config = [config]

        for conf in config:
            if not conf.get('path'):
                raise ConfigError('FFMpegcamera needs a `path` to save files to.')
            if not conf.get('video_device'):
                raise ConfigError('FFMpegcamera needs a `video_device` to capture images from.')
            if (conf.get('rotate_output') and not conf.get('rotate_filter_string')):
                raise ConfigError("FFMpegcamera needs a value for rotate_filter_string when rotate_output is set")
            
        return config


class FFMpegCamera(Camera):

    """ Properties """
    @property
    def record_video(self):
        """ Set to True to record video instead of photos """
        return self.config.get('record_video', False)

    @property
    def embed_timestamp(self):
        """ Set to True to add a timestamp to the video"""
        return self.config.get('embed_timestamp', False)

    @property
    def timestamp_offset_x(self):
        """ Return timestamp offset x component in pixels, measured from the top left corner of the frame"""
        return self.config.get('timestamp_offset', {}).get('x',0)

    @property
    def timestamp_offset_y(self):
        """ Return timestamp offset y component in pixels, measured from the top left corner of the frame"""
        return self.config.get('timestamp_offset', {}).get('y',0)

    @property
    def rotate_output(self):
        """ Set to True to rotate the video according to the rotation settings provided"""
        return self.config.get('rotate_output', False)

    @property
    def rotate_filter_string(self):
        """ This string is passed directly to ffmpeg's transpose video filter when rotate_output is true"""
        return self.config.get('rotate_filter_string', "")

    """ Methods """        
    def init(self):
        self.video_device = self.config.get("video_device", "/dev/video0")

    def update(self):
        """ Main update loop to check when to capture images """
        if self.mudpi.is_prepared:
            if self.duration > self.delay.total_seconds():
                if self.record_video:
                    self.capture_recording()
                else:
                    self.capture_image()
                self.reset_duration()

    """ Actions """
    def capture_image(self, data={}):
        """ Capture a single image from the camera
            it should use the file name and increment 
            counter for sequenetial images """
        image_name = f'{os.path.join(self.path, self.filename)}.jpg'
        _initialSettings = f"-hide_banner -loglevel error -stats -f v4l2 -use_wallclock_as_timestamps 1 -framerate {self.framerate}"
        _videoSize = f"-video_size {str(self.width)}x{str(self.height)}"
        _videoFilters = []
        _filterString = ""
        _endString = f"-q:v 1 -frames 1 -y {image_name}"
        
        #calculate vf filter string
        if(self.rotate_output):
            _videoFilters.append(self.rotate_filter_string)
        if(self.embed_timestamp):
            _videoFilters.append(f"drawtext=text='%{{localtime}}':fontcolor=White:box=1:boxcolor=0x00000088:x={self.timestamp_offset_x}:y={self.timestamp_offset_y}:fix_bounds=true")
        if(len(_videoFilters)>0):
            _filterString = f"-vf '{','.join(_videoFilters)}'"

        #command = f"ffmpeg -hide_banner -loglevel error -stats -f v4l2 -video_size {str(self.width)}x{str(self.height)} -i {self.video_device} -vf 'transpose=2' -q:v 1 -frames 1 -y {image_name}"
        command = f"ffmpeg {_initialSettings} {_videoSize} -i {self.video_device} {_filterString} {_endString}"
        completed_process = subprocess.run(command, shell=True)

        if completed_process.returncode == 0:
            self.last_image = os.path.abspath(image_name)
            self.increment_count()
            self.fire({'event': 'ImageCaptured', 'image': image_name})
        else:
            Logger.log_formatted(LOG_LEVEL["error"],f'FFMpeg Camera: Unable to capture using ffmpeg.')
        
        
    def capture_recording(self, data={}):
        """ Record a video from the camera """
        _file_name = f'{os.path.join(self.path, self.filename)}.mp4'
        
        _initialSettings = "-hide_banner -loglevel error -stats -f v4l2 -use_wallclock_as_timestamps 1"
        _videoSize = f"-video_size {str(self.width)}x{str(self.height)}"
        _videoFilters = []
        _filterString = ""
        _endString = f"-c:v h264_omx -b:v 8M -q:v 1 -t {self.record_duration} -y {_file_name}"
        
        #calculate vf filter string
        if(self.rotate_output):
            _videoFilters.append(self.rotate_filter_string)
        if(self.embed_timestamp):
            _videoFilters.append(f"drawtext=text='%{{localtime}}':fontcolor=White:box=1:boxcolor=0x00000088:x={self.timestamp_offset_x}:y={self.timestamp_offset_y}:fix_bounds=true")
        if(len(_videoFilters)>0):
            _filterString = f"-vf '{','.join(_videoFilters)}'"
        
        #_timestampCommand = ""
        # if(self.embed_timestamp): _timestampCommand = f"-vf 'drawtext=text='%{{localtime}}':fontcolor=white:x={self.timestamp_offset_x}:y={self.timestamp_offset_y}'"
        #command = f'ffmpeg -hide_banner -loglevel error -stats -use_wallclock_as_timestamps 1 -f v4l2 -video_size {str(self.width)}x{str(self.height)} -i {self.video_device} {_timestampCommand} -c:v h264_omx -b:v 8M -q:v 1 -t {self.record_duration} -y {_file_name}'
        
        command = f'ffmpeg {_initialSettings} {_videoSize} -i {self.video_device} {_filterString} {_endString}'
        completed_process = subprocess.run(command, shell=True)
        if completed_process.returncode == 0:
            self.last_image = os.path.abspath(_file_name)
            self.increment_count()
            self.fire({'event': 'RecordingCaptured', 'file': _file_name})
        else:
            Logger.log_formatted(LOG_LEVEL["error"],f'FFMpeg Camera: Unable to capture using ffmpeg.')