import json
from mudpi.exceptions import MudPiError
from mudpi.constants import FONT_YELLOW, FONT_RESET
from mudpi.logger.Logger import Logger, LOG_LEVEL

class Registry:
    """ Key-Value database for managing object instances """
    def __init__(self, mudpi, name):
        self.mudpi = mudpi
        self.name = name
        self._registry = {}

    def all(self):
        """ Return all items in the registry """
        return self._registry

    def items(self):
        """ Dict items() helper for iteration """
        return self.all().items()

    def keys(self):
        """ Dict keys() helper for iteration """
        return self.all().keys()

    def get(self, key):
        """ Get an item for the specified key """
        return self._registry[key]

    def exists(self, key):
        """ Return if key exists in the registry """
        return key in self._registry

    def register(self, key, value):
        """ Registers the value into the registry """
        if key not in self._registry:
            self.mudpi.events.publish(self.name, {'event': 'Registered', 'action': key})
        self._registry[key] = value
        return value

    @property
    def length(self):
        return len(self.all())


class ComponentRegistry(Registry):
    """ Comopnent Database
        Stores components per namespace for MudPi
    """
    def get(self, component_id):
        """ Get an item for the specified key """
        try:
            component = [ component 
            for components in self._registry.values()
            for _id, component in components.items() 
            if _id in component_id ][0]
        except Exception as error:
            component = None
        return component

    def for_namespace(self, namespace=None):
        """ Get all the components for a given namespace """
        return self._registry.setdefault(namespace, {})

    def for_interface(self, interface=None):
        """ Get all the components for a given interface """
        try:
            components = [ component 
            for components in self._registry.values()
            for _id, component in components.items() 
            if component.interface in interface ]
        except Exception as error:
            components = []
        return components

    def exists(self, component_ids):
        """ Return if key exists in the registry """
        return any([ exists for components in self._registry.values()
            for exists in components 
            if exists in component_ids ])

    def register(self, component_id, component, namespace=None):
        """ Registers the component into the registry """
        namespace_registry = self._registry.setdefault(namespace, {})
        if component_id not in namespace_registry:
            self.mudpi.events.publish('core', {'event': 'ComponentRegistered', 'component': component_id, 'namespace': namespace})
        namespace_registry[component_id] = component
        return component

    def ids(self):
        """ Return all the registered component ids """
        return [ component.id 
            for components in self._registry.values()
            for component in components.values() ]


class ActionRegistry(Registry):
    """ Database of actions available to MudPi from 
        user configs or components. 
        None = global
    """
    def register(self, action_key, func, namespace=None, validator=None):
        """ Register the action under the specified namespace. """
        namespace_registry = self._registry.setdefault(namespace, {})
        if action_key not in namespace_registry:
            self.mudpi.events.publish('core', {'event': 'ActionRegistered', 'action': action_key, 'namespace': namespace})
        namespace_registry[action_key] = Action(func, validator)

    def for_namespace(self, namespace=None):
        """ Get all the actions for a given namespace """
        return self._registry.setdefault(namespace, {})

    def exists(self, action_key):
        """ Return if action exists for given action command """
        action = self.parse_call(action_key)
        registry = self._registry.setdefault(action['namespace'], {})
        return action['action'] in registry

    def parse_call(self, action_call):
        """ Parse a command string and extract the namespace and action """
        parsed_action = {}
        if action_call.startswith('.'):
            # Empty Namespace
            parsed_action['namespace'] = None
            action_call = action_call.replace('.', '', 1)
            parsed_action['action'] = action_call
        elif '.' in action_call:
            parts = action_call.split('.')
            if len(parts) > 2:
                parsed_action['namespace'] = f'{parts[0]}.{parts[1]}'
                parsed_action['action'] = parts[2]
            else:
                parts = action_call.split('.', 1)
                parsed_action['namespace'] = parts[0]
                parsed_action['action'] = parts[1]
        else:
            parsed_action['namespace'] = None
            parsed_action['action'] = action_call
        return parsed_action

    def call(self, action_call, action_data={}):
        """ Call an action from the registry 
            Format: {namespace}.{action} or 
                    {namespace}.{component}.{action}
        """
        command = self.parse_call(action_call)
        action = self._registry.get(command['namespace'], {}).get(command['action'])
        if not action:
            # raise MudPiError("Call to action that doesn't exists!")
            Logger.log(
                LOG_LEVEL["error"],
                f'{FONT_YELLOW}Call to action {action_call} that doesn\'t exists!.{FONT_RESET}'
            )
        validated_data = action.validate(action_data)
        if not validated_data and action_data:
            # raise MudPiError("Action data was not valid!")
            Logger.log(
                LOG_LEVEL["error"],
                f'{FONT_YELLOW}Action data was not valid for {action_call}{FONT_RESET}'
            )
        self.mudpi.events.publish('core', {'event': 'ActionCall', 'action': action_call, 'data': action_data, 'namespace': command['namespace']})
        action(data=validated_data)


    def handle_call(self, event_data={}):
        """ Handle an Action call from event bus """
        if event_data:
            try:
                _data = json.loads(event_data.get('data', {}))
            except Exception:
                _data = event_data
            action = _data.get('action')
            if action:
                return self.call(action, _data.get('data', {}))

class Action:
    """ A callback associated with a string """

    def __init__(self, func, validator):
        self.func = func
        self.validator = None

    def validate(self, data):
        if not self.validator:
            return data

        if callable(self.validator):
            return self.validator(data)

        return False

    def __call__(self, data=None, **kwargs):
        if self.func:
            if callable(self.func):
                if data:
                    return self.func(data)
                else:
                    return self.func()