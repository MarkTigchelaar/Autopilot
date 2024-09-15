def get_python_builtin_definitions():
    return PYTHON_DEFINITIONS.copy()


# This is the built-in library catalog for the Python language.
# It is represented as a dictionary.
# It contains all items, enums, functions, classes etc. that can be imported using import ... from library ...
PYTHON_DEFINITIONS = {
    "io": {
        "import_path_literal": None,
        "sub_modules": 
            {
                "console": {
                    "import_path_literal": None,
                    "sub_modules": {},
                    "functions": {
                        "input": {
                            "import_path_literal": None,
                            "target_name": "input",
                            "return_type": "string",
                            "parameters": [{"prompt": "string", "default": None}],
                        },
                        "write": {
                            "import_path_literal": None,
                            "target_name": "print",
                            "return_type": None,
                            "parameters": ["Any"],
                        },
                    },
                    "classes": {},
                }
            }
        ,
        "functions": {},
        "classes": {},
    }
}
"""
TODO: Implement the rest of the Python built-in library definitions.
Number / string casting, data structure methods, etc.
Files for IO,


Math functions,
String functions,
List functions,
Dictionary functions,
Set functions,
Enum functions,
Class functions,
Add some handy libraries, like smtp, datetime, system directory, and file names,
polars dataframe library, etc.
"""