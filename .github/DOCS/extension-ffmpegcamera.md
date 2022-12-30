# ffmpegcamera
The `ffmpeg` extension provides an interface built on top of the [camera]({{url('docs/cameras')}}) component which uses [ffmpeg](https://ffmpeg.org/) to capture stills and videos from `v4l2` compatible devices, including USB cameras. It also provides options for timestamping and rotating video output. Connect a camera to your raspberry pi and make sure you enabled camera support through `raspi-config` for your pi if you have not done so.

This extension does not take an extension level configs and is focused on [interfaces.]({{url('docs/developers-interfaces')}})

---
<div class="mb-2"></div>

## Camera Interface
Provides a [camera]({{url('docs/cameras')}}) to take photos or record videos from a raspberry pi, using [ffmpeg](https://ffmpeg.org/)

<table class="mt-2 mb-4">
  <thead>
    <tr>
      <td width="15%">Option</td>
      <td width="15%">Type</td>
      <td width="15%">Required</td>
      <td width="55%">Description</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="font-600">path</td>
      <td class="text-italic text-sm">[String]</td>
      <td>Yes</td>
      <td class="text-xs">Full path where MudPi should save the images. <i>Make sure proper write permissions are set.</i>
      </td>
    </tr>
    <tr>
      <td class="font-600">video_device</td>
      <td class="text-italic text-sm">[String]</td>
      <td>Yes</td>
      <td class="text-xs">The v4l2 device identifier for the video device in question, i.e. <code>/dev/video0</code>
      </td>
    </tr>
    <tr>
      <td class="font-600">filename</td>
      <td class="text-italic text-sm">[String]</td>
      <td>No</td>
      <td class="text-xs">Name to save file as with either timestamp or photo count attached. i.e. <code>{filename}-00001.jpg</code>
      </td>
    </tr>
    <tr>
      <td class="font-600">record_video</td>
      <td class="text-italic text-sm">[Boolean]</td>
      <td>No</td>
      <td class="text-xs">Set to true to put camera in video mode. Default: <code>False</code> i.e. photo mode. </td>
    </tr>
    <tr>
      <td class="font-600">delay</td>
      <td class="text-italic text-sm">[Object]</td>
      <td>No</td>
      <td class="text-xs">The interval for the camera to take photos. Photo taken every X hours, X minutes, X Seconds. Default: <code>5 seconds</code>
      </td>
    </tr>
    <tr>
      <td class="font-600">delay.hours</td>
      <td class="text-italic text-sm">[Integer]</td>
      <td>No</td>
      <td class="text-xs">Interval in hours for camera to wait between photos. <span class="font-600">Default 0</span>
      </td>
    </tr>
    <tr>
      <td class="font-600">delay.minutes</td>
      <td class="text-italic text-sm">[Integer]</td>
      <td>No</td>
      <td class="text-xs">Interval in minutes for camera to wait between photos. <span class="font-600">Default 0</span>
      </td>
    </tr>
    <tr>
      <td class="font-600">delay.seconds</td>
      <td class="text-italic text-sm">[Integer]</td>
      <td>No</td>
      <td class="text-xs">Interval in seconds for camera to wait between photos. <span class="font-600">Default 0</span>
      </td>
    </tr>
    <tr>
      <td class="font-600">resolution</td>
      <td class="text-italic text-sm">[Object]</td>
      <td>No</td>
      <td class="text-xs">The resolution to take photos at. Larger resolution = larger filesize. Can only support max resolution of camera.</td>
    </tr>
    <tr>
      <td class="font-600">resolution.x</td>
      <td class="text-italic text-sm">[Integer]</td>
      <td>No</td>
      <td class="text-xs">Width to save image at in pixels. <span class="font-600">Default 1920</span>
      </td>
    </tr>
    <tr>
      <td class="font-600">resolution.y</td>
      <td class="text-italic text-sm">[Integer]</td>
      <td>No</td>
      <td class="text-xs">Height to save image at in pixels. <span class="font-600">Default 1080</span>
      </td>
    </tr>
    <tr>
      <td class="font-600">record_duration</td>
      <td class="text-italic text-sm">[Integer]</td>
      <td>No</td>
      <td class="text-xs">Time in seconds to record videos for when in record mode. Default: <code>5</code>
      </td>
    </tr>
    <tr>
      <td class="font-600">framerate</td>
      <td class="text-italic text-sm">[Integer]</td>
      <td>No</td>
      <td class="text-xs">Framerate to set camera at. Default: <code>15</code>
      </td>
    </tr>
    <tr>
      <td class="font-600">topic</td>
      <td class="text-italic text-sm">[String]</td>
      <td>No</td>
      <td class="text-xs">Channel that MudPi broadcasts new images events on. Default: <code>camera/{key}</code>
      </td>
    </tr>
    <tr>
      <td class="font-600">sequential_naming</td>
      <td class="text-italic text-sm">[Boolean]</td>
      <td>No</td>
      <td class="text-xs">Set to true to save photos with a counter instead of timetamp. Default: <code>False</code>
      </td>
    </tr>
    <tr>
      <td class="font-600">count_start</td>
      <td class="text-italic text-sm">[Integer]</td>
      <td>No</td>
      <td class="text-xs">Number to start count at if using <code>sequential_naming</code>
      </td>
    </tr>
    <tr>
      <td class="font-600">max_count</td>
      <td class="text-italic text-sm">[Integer]</td>
      <td>No</td>
      <td class="text-xs">Max number of photos before overwriting if using <code>sequential_naming</code>
      </td>
    </tr>
    <tr>
      <td class="font-600">embed_timestamp</td>
      <td class="text-italic text-sm">[Boolean]</td>
      <td>No</td>
      <td class="text-xs">Whether or not to embed a timestamp in each captured still or frame of video
      </td>
    </tr>
    <tr>
      <td class="font-600">timestamp_offset</td>
      <td class="text-italic text-sm">[Object]</td>
      <td>No</td>
      <td class="text-xs">Contains the values used to offset the timestamp, inset from the top left of the frame
      </td>
    </tr>
    <tr>
      <td class="font-600">timestamp_offset.x</td>
      <td class="text-italic text-sm">[Integer]</td>
      <td>No</td>
      <td class="text-xs">The x offset of the timestamp from the left of the frame, in pixels. Default: <code>0</code>
      </td>
    </tr>
    <tr>
      <td class="font-600">timestamp_offset.y</td>
      <td class="text-italic text-sm">[Integer]</td>
      <td>No</td>
      <td class="text-xs">The y offset of the timestamp from the top of the frame, in pixels.  Default: <code>0</code>
      </td>
    </tr>
    <tr>
      <td class="font-600">rotate_output</td>
      <td class="text-italic text-sm">[Boolean]</td>
      <td>No</td>
      <td class="text-xs">Whether or not to rotate the video using ffmpeg's transpose video filter
      </td>
    </tr>
    <tr>
      <td class="font-600">rotate_filter_string</td>
      <td class="text-italic text-sm">[String]</td>
      <td>No</td>
      <td class="text-xs">The string defining the transposition(s) applied to the video. Written in the format <code>transpose={filterValue}</code> where filterValue falls between 0-3 (inclusive), with special meanings denoted below:<br/>
      <code>0</code> = 90° counter-clockwise and vertical flip (default)<br/>
      <code>1</code> = 90° clockwise<br/>
      <code>2</code> = 90° counter-clockwise<br/>
      <code>3</code> = 90° clockwise and vertical flip<br/>
      </td>
    </tr>
  </tbody>
</table>

### Config Examples
#### Minimal ffmpegcamera configuration:
```json
"camera":[
    {
        "key":"ffmpeg_cam_1",
        "interface":"ffmpegcamera",
        "path":"/home/mudpi/img/ffmpeg_cam_1/img",
        "video_device":"/dev/video0",
    }
]
```
#### ffmpegcamera configuration to record a 10 second video every 10 minutes and add a timestamp with a 10 px vertical and horizontal offset:
```json
"camera":[
    {
        "key":"ffmpeg_cam_1",
        "interface":"ffmpegcamera",
        "path":"/home/mudpi/img/ffmpeg_cam_1/img",
        "video_device":"/dev/video0",
        "record_video":true,
        "record_duration":10,
        "delay":{
            "hours":0,
            "minutes":10,
            "seconds":0
        },
        "embed_timestamp":true,
        "timestamp_offset":{
            "x":10,
            "y":10
        }
    }
]
```
#### Complete ffmpegcamera configuration (with video recording), including timestamps and 90 CCW rotation:

```json
"camera":[
    {
        "key":"ffmpeg_cam_1",
        "name":"Cam 1",
        "interface":"ffmpegcamera",
        "path":"/home/mudpi/img/ffmpeg_cam_1/img",
        "filename":"ffmpeg_cam_1_capture",
        "video_device":"/dev/video0",
        "topic":"camera/ffmpeg_cam_1",
        "framerate":30,
        "record_video":true,
        "record_duration":10,
        "sequential_naming":true,
        "count_start":0,
        "max_count":100,
        "delay":{
            "hours":0,
            "minutes":10,
            "seconds":0
        },
        "resolution":{
            "x":1280,
            "y":960
        },
        "embed_timestamp":true,
        "timestamp_offset":{
            "x":10,
            "y":10
        },
        "rotate_output":true,
        "rotate_filter_string":"transpose=2"
    }
]
```

---
<div class="mb-2"></div>

## WIP
Note, this interface is currently a work in progress. There are many features of ffmpeg not being exposed / leveraged, others left too exposed, and some of the operations performed may not be as performant as they could be given more attention. That said, it is stable on an RPI 3B+ at time of writing for both stills and video.

### Todo
This is a wishlist of features and revisions I'd like to make for `ffmpegcamera`
- [ ] Refactor: Remove boolean flags for `embed_timestamp` and `rotate_output` in favour of simply checking for object existence for their respective options objects
- [ ] Consider moving to `-display_rotation`+`autorotate` instead of `-vf transpose` via to allow for a numerical degree input in config
- [ ] Expose `--vf (video filter)` options for:
  - [ ] `-display_hflip`
  - [ ] `-display_vflip`
- [ ] Expose more timestamp styling options
- [ ] Allow for `vfl2-ctl` options to be sent for camera initialization, noting the complexity of matching cameras to options in `v4l2-ctl` in the docs
- [ ] Consider additional `-vf (video filter)` input using a dict that is simply joined using appropriate separators, being cognisant of potential for injection

