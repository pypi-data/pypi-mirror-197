# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dropdown(Component):
    """A Dropdown component.
A Dropdown is a selection component composed of a button and a list of options.
The button displays the current selected item or a placeholder, and the list is
visible on demand by clicking the button. Dropdowns are typically used in forms.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- appearance (a value equal to: 'outline', 'underline', 'filled-darker', 'filled-lighter'; default 'outline'):
    Controls the colors and borders of the combobox trigger.

- disabled (boolean; default False):
    If True, the dropdown is disabled and can't be clicked on.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; optional):
    The label associated with the field.

- label_size (a value equal to: 'small', 'medium', 'large'; optional):
    The size of the Field's label.

- multiselect (boolean; default False):
    If True, the user can select multiple values.

- options (list of dicts; optional):
    Choices to be displayed in the dropdown control.

    `options` is a list of dicts with keys:

    - disabled (boolean; optional):
        denotes if radio is disabled.

    - label (string; required):
        The Radio's label.

    - value (string; required):
        The Radio's value.

- orientation (a value equal to: 'horizontal', 'vertical'; optional):
    The orientation of the label relative to the field component. This
    only affects the label, and not the validationMessage or hint
    (which always appear below the field component).

- placeholder (string; optional):
    A string value to be displayed if no item is selected.

- required (boolean; optional):
    Marks the Field as required. If True, an asterisk will be appended
    to the label, and aria-required will be set on the Field's child.

- size (a value equal to: 'small', 'medium', 'large'; default 'medium'):
    Controls the size of the combobox faceplate.

- validation_message (string; optional):
    A message about the validation state. By default, this is an error
    message, but it can be a success, warning, or custom message by
    setting validationState.

- validation_state (a value equal to: 'none', 'success', 'warning', 'error'; optional):
    The validationState affects the display of the validationMessage
    and validationMessageIcon.

- value (list of strings; optional):
    The value of the input."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Dropdown'
    @_explicitize_args
    def __init__(self, value=Component.UNDEFINED, multiselect=Component.UNDEFINED, options=Component.UNDEFINED, placeholder=Component.UNDEFINED, disabled=Component.UNDEFINED, size=Component.UNDEFINED, appearance=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, label=Component.UNDEFINED, validation_message=Component.UNDEFINED, orientation=Component.UNDEFINED, validation_state=Component.UNDEFINED, required=Component.UNDEFINED, label_size=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'appearance', 'disabled', 'key', 'label', 'label_size', 'multiselect', 'options', 'orientation', 'placeholder', 'required', 'size', 'validation_message', 'validation_state', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'appearance', 'disabled', 'key', 'label', 'label_size', 'multiselect', 'options', 'orientation', 'placeholder', 'required', 'size', 'validation_message', 'validation_state', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Dropdown, self).__init__(**args)
