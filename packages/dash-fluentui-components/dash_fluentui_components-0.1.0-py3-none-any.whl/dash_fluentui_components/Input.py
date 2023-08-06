# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Input(Component):
    """An Input component.
Input allows the user to enter and edit text.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- appearance (a value equal to: 'outline', 'underline', 'filled-darker', 'filled-lighter', 'filled-darker-shadow', 'filled-lighter-shadow'; optional):
    Controls the colors and borders of the input.

- content_after (a list of or a singular dash component, string or number; optional):
    Element after the input text, within the input border.

- content_before (a list of or a singular dash component, string or number; optional):
    Element before the input text, within the input border.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; optional):
    The label associated with the field.

- label_size (a value equal to: 'small', 'medium', 'large'; optional):
    The size of the Field's label.

- orientation (a value equal to: 'horizontal', 'vertical'; optional):
    The orientation of the label relative to the field component. This
    only affects the label, and not the validationMessage or hint
    (which always appear below the field component).

- placeholder (string; optional):
    Placeholder text for the input.

- required (boolean; optional):
    Marks the Field as required. If True, an asterisk will be appended
    to the label, and aria-required will be set on the Field's child.

- size (a value equal to: 'small', 'medium', 'large'; optional):
    Size of the input (changes the font size and spacing).

- type (a value equal to: 'number', 'time', 'text', 'search', 'tel', 'url', 'email', 'date', 'datetime-local', 'month', 'password'; optional):
    An input can have different text-based types based on the type of
    value the user will enter.

- validation_message (string; optional):
    A message about the validation state. By default, this is an error
    message, but it can be a success, warning, or custom message by
    setting validationState.

- validation_state (a value equal to: 'none', 'success', 'warning', 'error'; optional):
    The validationState affects the display of the validationMessage
    and validationMessageIcon.

- value (string; optional):
    Current value of the input."""
    _children_props = ['content_before', 'content_after']
    _base_nodes = ['content_before', 'content_after', 'children']
    _namespace = 'dash_fluentui_components'
    _type = 'Input'
    @_explicitize_args
    def __init__(self, appearance=Component.UNDEFINED, type=Component.UNDEFINED, size=Component.UNDEFINED, value=Component.UNDEFINED, placeholder=Component.UNDEFINED, content_before=Component.UNDEFINED, content_after=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, label=Component.UNDEFINED, validation_message=Component.UNDEFINED, orientation=Component.UNDEFINED, validation_state=Component.UNDEFINED, required=Component.UNDEFINED, label_size=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'appearance', 'content_after', 'content_before', 'key', 'label', 'label_size', 'orientation', 'placeholder', 'required', 'size', 'type', 'validation_message', 'validation_state', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'appearance', 'content_after', 'content_before', 'key', 'label', 'label_size', 'orientation', 'placeholder', 'required', 'size', 'type', 'validation_message', 'validation_state', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Input, self).__init__(**args)
