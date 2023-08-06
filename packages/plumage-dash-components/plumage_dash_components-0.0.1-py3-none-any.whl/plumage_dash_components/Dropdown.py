# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dropdown(Component):
    """A Dropdown component.


Keyword arguments:

- id (string; required):
    The ID used to identify this component in Dash callbacks.

- allowSelectAll (boolean; default True):
    enable selection of all components in list, default True.

- className (string; default ""):
    Append a class to the div of dropdown component.

- closeMenuOnSelect (boolean; default False):
    close menu when selecting. if False keep menu open. default False.

- hideSelectedOptions (boolean; default True):
    hide the selection made or keep in list if False. default True.

- isClearable (boolean; default True):
    clear selection default True.

- isDisabled (boolean; default False):
    disable dropdown default False.

- isMulti (boolean; default True):
    isMulti Selection bool.

- label (string; default ""):
    Label above the dropdown.

- options (list of dicts; optional):
    An array of options {label: [string|number], value:
    [string|number]},.

    `options` is a list of string | numbers | list of dicts with keys:

    - label (string | number; required)

    - value (string | number; required)

- style (dict; optional):
    append style to the div of dropdown component.

- value (dict; optional):
    The value of the input. If `multi` is False then value is just a
    string that corresponds to the values provided in the `options`
    property. If `multi` is True, then multiple values can be selected
    at once, and `value` is an array of items with values
    corresponding to those in the `options` prop.

    `value` is a string | number | list of string | numbers | list of
    dicts with keys:

    - label (string | number; required)

    - value (string | number; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'plumage_dash_components'
    _type = 'Dropdown'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, value=Component.UNDEFINED, options=Component.UNDEFINED, isMulti=Component.UNDEFINED, closeMenuOnSelect=Component.UNDEFINED, hideSelectedOptions=Component.UNDEFINED, allowSelectAll=Component.UNDEFINED, isClearable=Component.UNDEFINED, isDisabled=Component.UNDEFINED, style=Component.UNDEFINED, className=Component.UNDEFINED, label=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'allowSelectAll', 'className', 'closeMenuOnSelect', 'hideSelectedOptions', 'isClearable', 'isDisabled', 'isMulti', 'label', 'options', 'style', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'allowSelectAll', 'className', 'closeMenuOnSelect', 'hideSelectedOptions', 'isClearable', 'isDisabled', 'isMulti', 'label', 'options', 'style', 'value']
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
