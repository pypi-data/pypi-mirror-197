# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Checkbox(Component):
    """A Checkbox component.
Checkboxes give people a way to select one or more items from a group,
or switch between two mutually exclusive options (checked or unchecked).

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- checked (boolean | number | string | dict | list; default False):
    Checked state.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- disabled (boolean; default False):
    Disabled state of button.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- label (string; default 'Checkbox'):
    Label to display next to the checkbox.   The label associated with
    the field.

- label_position (a value equal to: 'before', 'after'; default 'after'):
    The position of the label relative to the checkbox indicator.

- label_size (a value equal to: 'medium', 'large', 'small'; optional):
    The size of the Field's label.

- orientation (a value equal to: 'horizontal', 'vertical'; optional):
    The orientation of the label relative to the field component. This
    only affects the label, and not the validationMessage or hint
    (which always appear below the field component).

- required (boolean; optional):
    Marks the Field as required. If True, an asterisk will be appended
    to the label, and aria-required will be set on the Field's child.

- shape (a value equal to: 'circular', 'square'; default 'square'):
    The shape of the checkbox indicator.  The circular variant is only
    recommended to be used in a tasks-style UI (checklist), since it
    otherwise could be confused for a RadioItem.

- size (a value equal to: 'medium', 'large'; default 'medium'):
    The size of the checkbox indicator.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

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
    _type = 'Checkbox'
    @_explicitize_args
    def __init__(self, checked=Component.UNDEFINED, disabled=Component.UNDEFINED, label=Component.UNDEFINED, label_position=Component.UNDEFINED, shape=Component.UNDEFINED, size=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, validation_message=Component.UNDEFINED, orientation=Component.UNDEFINED, validation_state=Component.UNDEFINED, required=Component.UNDEFINED, label_size=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'checked', 'class_name', 'disabled', 'key', 'label', 'label_position', 'label_size', 'orientation', 'required', 'shape', 'size', 'style', 'validation_message', 'validation_state']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'checked', 'class_name', 'disabled', 'key', 'label', 'label_position', 'label_size', 'orientation', 'required', 'shape', 'size', 'style', 'validation_message', 'validation_state']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Checkbox, self).__init__(**args)
