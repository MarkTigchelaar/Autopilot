import os
from Testing.utils import open_json
from ASTComponents.AggregatedComponents.libraries import Library

def select_libraries(library_names):
    libraries = dict()
    abs_location_of_this_python_file = os.path.dirname(__file__)
    for library_name in library_names:
        lib_path = os.path.normpath(
            abs_location_of_this_python_file + "/LibraryFiles/" + library_name + ".json"
        )
        # This blows up if "library" json doesnt exist
        libraries[library_name] = Library(open_json(lib_path))
    return libraries
