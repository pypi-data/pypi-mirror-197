from collections.abc import Iterable

DEFAULT_ACTIONS = ['required', 'default', 'convert', 'type', 'valid', 'rename', ]
NONE_VALUES = [None, '', [], (), {}]
TYPE_MAP = {
    'int': int,
    'float': float,
    'number': (int, float),
    'str': str,
    'bool': bool,
    'list': (tuple, list, set),
    'dict': dict,
}


def purify(data, schema, many=False):
    return Puty(schema).purify(data, many=many)


class PutyException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class PutyActionException(Exception):
    def __init__(self, key, value, action=None, param=None, message=None):
        self.action = action
        self.key = key
        self.value = value
        self.param = param
        self.message = message

    def __str__(self):
        return self.message


class skip:
    """
    When null is this class, that will remove in value dict.
    """
    pass


class Puty:
    """
    example of inspector map

    ALLOWED_ACTIONS: required, type, default, convert, valid, rename

    {
        key: {
            'required': True or False,
            'type': ['int', 'float', 'number', 'str', 'list', 'dict', 'bool'],
            'default': {DEFAULT_VALUE},
            'convert': [int, float, str, list, convert_function, ...],
            'valid': {Validation Function},
            'rename': string
        },
        another_key: {
            ...actions
        }
    }

    # valid function example
    def valid_func(value, key, schema):
        return True or False

    # rename function example
    def rename_func(value, original):
        # original: original key of data
        return 'new_name'
    """
    type_maps = TYPE_MAP
    none_values = NONE_VALUES
    allow_actions = DEFAULT_ACTIONS

    def __init__(self, schema=None):
        self.schema = schema
        self._current_schema = None

    def action_unknown(self, key, value, param=None):
        """
        When data not exists in inspect_map
        """
        return skip

    def action_required(self, key, value, param):
        """
        When field has required.
        """
        required = param
        if required and value in self.none_values:
            raise PutyActionException(
                key, value, action='required', param=param,
                message='required field {} is not exists'.format(key)
            )
        return value

    def action_convert(self, key, value, param):
        """
        When field has convert, convert value
        """
        if not callable(param):
            raise PutyException(
                message='{} convert param is not callable'.format(key)
            )
        return param(value)

    def action_type(self, key, value, param):
        """
        When field has type, check type.
        """
        if param not in self.type_maps:
            raise PutyActionException(
                key, value, action='type', param=param,
                message='type: {} is not allowed'.format(param)
            )
        if value is None:
            return value

        standard = self.type_maps[param]
        value_type = type(value)

        if value_type is standard:
            return value
        if isinstance(standard, Iterable) and value_type in standard:
            return value
        raise PutyActionException(
            key, value, action='type', param=param,
            message='value type: {} is not {}'.format(value_type, param)
        )

    def action_default(self, key, value, param):
        """
        When field has default and value in none_values, return default
        """
        default = param
        if value in self.none_values:
            if param is skip:
                return skip
            if callable(default):
                return default()
            return default
        return value

    def action_valid(self, key, value, param):
        if not callable(param):
            raise PutyActionException(
                key, value, action='valid', param=param,
                message='valid function: {} is not callable'.format(param)
            )

        if param(value, key=key):
            return value
        raise PutyActionException(
            key, value, action='valid', param=param,
            message='validation error: {} is invalid value {}'.format(key, value)
        )

    def action_rename(self, key, value, param):
        if callable(param):
            return param(value, original=key)
        return param

    def get_clear_field(self, field):
        if 'required' in field and 'default' in field:
            raise PutyException(
                'Purify failed: required action cannot be used with default.'
            )
        if 'convert' in field and 'type' in field:
            raise PutyException(
                'Purify failed: convert action cannot be used with type.'
            )

        result = {}
        for action in self.allow_actions:
            if action in field:
                result[action] = field[action]
        return result

    def action(self, action, key, value, param):
        if action == 'unknown':
            return self.action_unknown(key, value, param)
        if action not in self.allow_actions:
            raise PutyException('invalid action: {}'.format(action))
        method = getattr(self, 'action_{}'.format(action))
        return method(key, value, param)

    def purify_field(self, key, value, field):
        cleared_field = self.get_clear_field(field)
        # rename action always run first
        if 'rename' in field:
            key = self.action_rename(key, value, cleared_field.pop('rename'))

        for action, param in cleared_field.items():
            value = self.action(action, key, value, param)
            if value is skip:
                break
        return key, value

    def _purify_data(self, data):
        result = {}
        # field in schema
        for key, field in self._current_schema.items():
            value = data.get(key)
            key, value = self.purify_field(key, value, field)
            if value is skip:
                continue
            result[key] = value

        # data not in schema
        unknown_data = {key: value for key, value in data.items() if key not in self._current_schema}
        for key, value in unknown_data.items():
            value = self.action('unknown', key, value, None)
            if value is skip:
                continue
            result[key] = value

        return result

    def purify(self, data, schema=None, many=False):
        schema = schema or self.schema
        if schema is None:
            raise PutyException('Purifying failed: no schema')
        self._current_schema = schema

        if not many:
            result = self._purify_data(data)
            self._current_schema = None
            return result

        results = []
        for item in data:
            purified_item = self._purify_data(item)
            results.append(purified_item)
        self._current_schema = None
        return results
