def to_js(o):
    import js
    import pyodide
    return pyodide.to_js(o, dict_converter=js.Object.fromEntries)
