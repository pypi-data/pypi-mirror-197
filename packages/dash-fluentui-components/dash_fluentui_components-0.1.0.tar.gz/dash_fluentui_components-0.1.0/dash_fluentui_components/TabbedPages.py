# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TabbedPages(Component):
    """A TabbedPages component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional)

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- header (a list of or a singular dash component, string or number; optional)

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- selected_key (string; optional):
    Key of the currently selected page item in navigation controls."""
    _children_props = ['header']
    _base_nodes = ['header', 'children']
    _namespace = 'dash_fluentui_components'
    _type = 'TabbedPages'
    @_explicitize_args
    def __init__(self, children=None, header=Component.UNDEFINED, selected_key=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'header', 'key', 'selected_key']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'header', 'key', 'selected_key']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(TabbedPages, self).__init__(children=children, **args)
