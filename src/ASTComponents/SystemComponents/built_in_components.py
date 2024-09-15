from ASTComponents.SystemComponents.python_definitions import get_python_builtin_definitions

"""
This module contains the built-in library catalog for the system.
It is represented as json.
"""
def get_built_in_library_catalog(language_name: str) -> dict:
    if language_name == "python":
        return get_python_builtin_definitions()
    else:
        raise Exception("Language not supported: " + language_name)