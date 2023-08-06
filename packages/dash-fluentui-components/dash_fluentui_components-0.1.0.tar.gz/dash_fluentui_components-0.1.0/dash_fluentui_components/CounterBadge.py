# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CounterBadge(Component):
    """A CounterBadge component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- appearance (a value equal to: 'filled', 'ghost'; default 'filled'):
    A button can have its content and borders styled for greater
    emphasis or to be subtle.   - 'secondary' (default): Gives
    emphasis to the button in such a way that it indicates a secondary
    action.  - 'primary': Emphasizes the button as a primary action.
    - 'outline': Removes background styling.  - 'subtle': Minimizes
    emphasis to blend into the background until hovered or focused.  -
    'transparent': Removes background and border styling.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- color (a value equal to: 'brand', 'danger', 'important', 'informative'; default 'brand'):
    Disabled state of button.

- count (number; default 0):
    Value displayed by the Badge.

- dot (boolean; default False):
    If a dot should be displayed without the count.

- icon (a list of or a singular dash component, string or number; optional)

- icon_position (a value equal to: 'before', 'after'; optional):
    A Badge can position the icon before or after the content.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- overflow_count (number; optional):
    Max number to be displayed.

- shape (a value equal to: 'circular', 'rounded'; default 'circular'):
    A Badge can be square, circular or rounded.

- show_zero (boolean; default False):
    Max number to be displayed.

- size (a value equal to: 'small', 'tiny', 'extra-small', 'medium', 'large', 'extra-large'; optional):
    A Badge can be of several preset sizes.

- style (dict; optional):
    Defines CSS styles which will override styles previously set."""
    _children_props = ['icon']
    _base_nodes = ['icon', 'children']
    _namespace = 'dash_fluentui_components'
    _type = 'CounterBadge'
    @_explicitize_args
    def __init__(self, children=None, count=Component.UNDEFINED, icon=Component.UNDEFINED, appearance=Component.UNDEFINED, color=Component.UNDEFINED, shape=Component.UNDEFINED, size=Component.UNDEFINED, icon_position=Component.UNDEFINED, dot=Component.UNDEFINED, overflow_count=Component.UNDEFINED, show_zero=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'appearance', 'class_name', 'color', 'count', 'dot', 'icon', 'icon_position', 'key', 'overflow_count', 'shape', 'show_zero', 'size', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'appearance', 'class_name', 'color', 'count', 'dot', 'icon', 'icon_position', 'key', 'overflow_count', 'shape', 'show_zero', 'size', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(CounterBadge, self).__init__(children=children, **args)
