# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Switch(Component):
    """A Switch component.
A switch represents a physical switch that allows someone to choose between two mutually exclusive options.
For example, "On/Off" and "Show/Hide". Choosing an option should produce an immediate result.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- checked (boolean; default False):
    Checked state of the toggle.

- disabled (boolean; default False):
    If True, the switch is disabled and can't be clicked on.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; default ''):
    A label to be displayed along with the toggle component.   The
    label associated with the field.

- label_postion (a value equal to: 'before', 'after', 'above'; optional):
    The position of the label relative to the Switch.

- label_size (a value equal to: 'small', 'medium', 'large'; optional):
    The size of the Field's label.

- orientation (a value equal to: 'horizontal', 'vertical'; optional):
    The orientation of the label relative to the field component. This
    only affects the label, and not the validationMessage or hint
    (which always appear below the field component).

- required (boolean; optional):
    Marks the Field as required. If True, an asterisk will be appended
    to the label, and aria-required will be set on the Field's child.

- validation_message (string; optional):
    A message about the validation state. By default, this is an error
    message, but it can be a success, warning, or custom message by
    setting validationState.

- validation_state (a value equal to: 'none', 'success', 'warning', 'error'; optional):
    The validationState affects the display of the validationMessage
    and validationMessageIcon."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Switch'
    @_explicitize_args
    def __init__(self, label=Component.UNDEFINED, checked=Component.UNDEFINED, label_postion=Component.UNDEFINED, disabled=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, validation_message=Component.UNDEFINED, orientation=Component.UNDEFINED, validation_state=Component.UNDEFINED, required=Component.UNDEFINED, label_size=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'checked', 'disabled', 'key', 'label', 'label_postion', 'label_size', 'orientation', 'required', 'validation_message', 'validation_state']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'checked', 'disabled', 'key', 'label', 'label_postion', 'label_size', 'orientation', 'required', 'validation_message', 'validation_state']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Switch, self).__init__(**args)
