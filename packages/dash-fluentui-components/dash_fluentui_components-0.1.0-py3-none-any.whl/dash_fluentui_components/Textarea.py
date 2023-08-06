# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Textarea(Component):
    """A Textarea component.
Textarea allows the user to enter and edit multiline text.
### Do
- Consider using Textarea with outline appearance. When the contrast ratio against
  the immediate surrounding color is less than 3:1, consider using outline styles
  which has a bottom border stroke. But please ensure the color of bottom border stroke
  has a sufficient contrast which is greater than 3 to 1 against the immediate surrounding.
### Don't
- Don’t place Textarea on a surface which doesn't have a sufficient contrast.
  The colors adjacent to the input should have a sufficient contrast. Particularly,
  the color of input with filled darker and lighter styles needs to provide greater
  than 3 to 1 contrast ratio against the immediate surrounding color to pass accessibility
  requirements.

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- appearance (a value equal to: 'outline', 'filled-darker', 'filled-lighter'; default 'outline'):
    Styling the Textarea should use.

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

- required (boolean; optional):
    Marks the Field as required. If True, an asterisk will be appended
    to the label, and aria-required will be set on the Field's child.

- resize (a value equal to: 'none', 'both', 'horizontal', 'vertical'; default 'none'):
    Which direction the Textarea is allowed to be resized.

- size (a value equal to: 'small', 'medium', 'large'; default 'medium'):
    Size of the Textarea.

- validation_message (string; optional):
    A message about the validation state. By default, this is an error
    message, but it can be a success, warning, or custom message by
    setting validationState.

- validation_state (a value equal to: 'none', 'success', 'warning', 'error'; optional):
    The validationState affects the display of the validationMessage
    and validationMessageIcon.

- value (string; optional):
    The value of the Textarea."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Textarea'
    @_explicitize_args
    def __init__(self, appearance=Component.UNDEFINED, resize=Component.UNDEFINED, size=Component.UNDEFINED, value=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, label=Component.UNDEFINED, validation_message=Component.UNDEFINED, orientation=Component.UNDEFINED, validation_state=Component.UNDEFINED, required=Component.UNDEFINED, label_size=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'appearance', 'key', 'label', 'label_size', 'orientation', 'required', 'resize', 'size', 'validation_message', 'validation_state', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'appearance', 'key', 'label', 'label_size', 'orientation', 'required', 'resize', 'size', 'validation_message', 'validation_state', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Textarea, self).__init__(**args)
