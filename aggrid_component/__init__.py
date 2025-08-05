import streamlit.components.v1 as components
import os

_component_func = components.declare_component("aggrid_component", path=os.path.join(os.path.dirname(__file__), "frontend", "build"))

def aggrid_component(data, workers, columns, key=None):
    return _component_func(data=data, workers=workers, columns=columns, key=key)
