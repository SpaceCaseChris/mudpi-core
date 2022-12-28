# SOC Temperature Sensor
The `soc_temp_sensor` extension provides an interface used to display the SOC's temperature (returned by `vcgencmd measure_temp`) inline with other sensors in your Mudpi configuration.

This extension does not take an extension level configs and is focused on [interfaces.]({{url('docs/developers-interfaces')}})

---
<div class="mb-2"></div>

## Sensor Interface
Provides a [sensor]({{url('docs/sensors')}}) that returns the temperature reported by `vcgencmd measure_temp`

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
            <td class="font-600">key</td>
            <td class="text-italic text-sm">[String]</td>
            <td>Yes</td><td class="text-xs">Unique slug id for the component</td>
        </tr>
        <tr>
            <td class="font-600">name</td>
            <td class="text-italic text-sm">[String]</td>
            <td>No</td>
            <td class="text-xs">Friendly display name of component. Useful for UI.</td>
        </tr>
        <tr>
            <td class="font-600">classifier</td>
            <td class="text-italic text-sm">[String]</td>
            <td>No</td>
            <td class="text-xs">Classifier override for sensor formatting.</td>
        </tr>
    </tbody>
</table>

### Config Examples
Here is a config of a complete SOC Temperature Sensor.

```json
"sensor": [{
    "key": "soc_temp_sensor_1",
    "interface": "soc_temp_sensor",
    "topic": "sensor/soc",
    "classifier":"temperature"
}]
```



