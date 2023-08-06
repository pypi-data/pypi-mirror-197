# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Slider(Component):
    """A Slider component.
A Slider represents an input that allows user to choose a value from within a specific range.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- disabled (boolean; default False):
    Optional flag to render the Slider as disabled.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; optional):
    Description label of the Slider   The label associated with the
    field.

- label_size (a value equal to: 'small', 'medium', 'large'; optional):
    The size of the Field's label.

- max (number; required):
    The max value of the Slider.

- min (number; required):
    The min value of the Slider.

- orientation (a value equal to: 'vertical', 'horizontal'; optional):
    The orientation of the label relative to the field component. This
    only affects the label, and not the validationMessage or hint
    (which always appear below the field component).

- required (boolean; optional):
    Marks the Field as required. If True, an asterisk will be appended
    to the label, and aria-required will be set on the Field's child.

- size (a value equal to: 'small', 'medium'; default 'medium'):
    The size of the Slider.

- step (number; optional):
    The difference between the two adjacent values of the Slider.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- validation_message (string; optional):
    A message about the validation state. By default, this is an error
    message, but it can be a success, warning, or custom message by
    setting validationState.

- validation_state (a value equal to: 'none', 'success', 'warning', 'error'; optional):
    The validationState affects the display of the validationMessage
    and validationMessageIcon.

- value (number; optional):
    The initial value of the Slider.

- vertical (boolean; default False):
    Optional flag to render the slider vertically. Defaults to
    rendering horizontal."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Slider'
    @_explicitize_args
    def __init__(self, label=Component.UNDEFINED, value=Component.UNDEFINED, min=Component.REQUIRED, max=Component.REQUIRED, step=Component.UNDEFINED, vertical=Component.UNDEFINED, size=Component.UNDEFINED, disabled=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, validation_message=Component.UNDEFINED, orientation=Component.UNDEFINED, validation_state=Component.UNDEFINED, required=Component.UNDEFINED, label_size=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'class_name', 'disabled', 'key', 'label', 'label_size', 'max', 'min', 'orientation', 'required', 'size', 'step', 'style', 'validation_message', 'validation_state', 'value', 'vertical']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'class_name', 'disabled', 'key', 'label', 'label_size', 'max', 'min', 'orientation', 'required', 'size', 'step', 'style', 'validation_message', 'validation_state', 'value', 'vertical']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['max', 'min']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Slider, self).__init__(**args)
