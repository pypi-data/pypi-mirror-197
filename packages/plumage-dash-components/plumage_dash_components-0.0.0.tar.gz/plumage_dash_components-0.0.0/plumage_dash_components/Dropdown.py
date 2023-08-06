# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dropdown(Component):
    """A Dropdown component.


Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- allowSelectAll (boolean; default True)

- closeMenuOnSelect (boolean; default False)

- hideSelectedOptions (boolean; default True)

- isClearable (boolean; default True)

- isDisabled (boolean; default False)

- isMulti (boolean; default True)

- options (list of dicts; optional)

    `options` is a list of dicts with keys:

    - label (string | number; required)

    - value (string | number; required)

- style (dict; optional)

- value (string | number | list of string | numbers; optional):
    The value of the input. If `multi` is False then value is just a
    string that corresponds to the values provided in the `options`
    property. If `multi` is True, then multiple values can be selected
    at once, and `value` is an array of items with values
    corresponding to those in the `options` prop."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'plumage_dash_components'
    _type = 'Dropdown'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, value=Component.UNDEFINED, options=Component.UNDEFINED, isMulti=Component.UNDEFINED, closeMenuOnSelect=Component.UNDEFINED, hideSelectedOptions=Component.UNDEFINED, allowSelectAll=Component.UNDEFINED, isClearable=Component.UNDEFINED, isDisabled=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'allowSelectAll', 'closeMenuOnSelect', 'hideSelectedOptions', 'isClearable', 'isDisabled', 'isMulti', 'options', 'style', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'allowSelectAll', 'closeMenuOnSelect', 'hideSelectedOptions', 'isClearable', 'isDisabled', 'isMulti', 'options', 'style', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Dropdown, self).__init__(**args)
