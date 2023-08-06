# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Badge(Component):
    """A Badge component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- appearance (a value equal to: 'filled', 'ghost', 'outline', 'tint'; optional):
    A button can have its content and borders styled for greater
    emphasis or to be subtle.   - 'secondary' (default): Gives
    emphasis to the button in such a way that it indicates a secondary
    action.  - 'primary': Emphasizes the button as a primary action.
    - 'outline': Removes background styling.  - 'subtle': Minimizes
    emphasis to blend into the background until hovered or focused.  -
    'transparent': Removes background and border styling.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- color (a value equal to: 'brand', 'danger', 'important', 'informative', 'severe', 'subtle', 'success', 'warning'; optional):
    Disabled state of button.

- icon_position (a value equal to: 'before', 'after'; optional):
    A Badge can position the icon before or after the content.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- shape (a value equal to: 'circular', 'square', 'rounded'; optional):
    A Badge can be square, circular or rounded.

- size (a value equal to: 'small', 'tiny', 'extra-small', 'medium', 'large', 'extra-large'; optional):
    A Badge can be of several preset sizes.

- style (dict; optional):
    Defines CSS styles which will override styles previously set."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_fluentui_components'
    _type = 'Badge'
    @_explicitize_args
    def __init__(self, children=None, appearance=Component.UNDEFINED, color=Component.UNDEFINED, shape=Component.UNDEFINED, size=Component.UNDEFINED, icon_position=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'appearance', 'class_name', 'color', 'icon_position', 'key', 'shape', 'size', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'appearance', 'class_name', 'color', 'icon_position', 'key', 'shape', 'size', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(Badge, self).__init__(children=children, **args)
