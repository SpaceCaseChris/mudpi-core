# Example
The `storage-sensor` extension provides a simple sensor interface that displays used and total storage space and a percentage represenation of the same.

This extension does not take an extension level configs and is focused on [interfaces.]({{url('docs/developers-interfaces')}})

---
<div class="mb-2"></div>

## Sensor Interface
Provides a [sensor]({{url('docs/sensors')}}) that returns used and total storage space and a percentage represenation of the same.

<table class="mt-2 mb-4">
<thead><tr><td width="15%">Option</td><td width="15%">Type</td><td width="15%">Required</td><td width="55%">Description</td></tr></thead>
<tbody>
    <tr><td class="font-600">key</td><td class="text-italic text-sm">[String]</td><td>Yes</td><td class="text-xs">Unique slug id for the component</td></tr>
    <tr><td class="font-600">name</td><td class="text-italic text-sm">[String]</td><td>No</td><td class="text-xs">Friendly display name of component. Useful for UI.</td></tr>
</tbody>
</table>

### Config Examples
Here is a config of a complete storage-sensor.

```json
"sensor": [{
    "key": "storage_sensor",
    "name": "Storage Sensor",
    "interface": "storage_sensor"
}]
```
