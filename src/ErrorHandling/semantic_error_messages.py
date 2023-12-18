

ENUM_HAS_UDT = "enum type cannot be a user defined type"

ENUM_DUP_FIELD_NAME = "duplicate enum field name"

ENUM_DUP_VALUE = "duplicate enum value"

ENUM_MISMATCHED_TYPE = "enum field has mismatched type"

ENUM_AND_FIELD_TYPE_MISMATCH = "enum field type does not match enum type"

ENUM_AND_FIELD_NAME_COLLISION = "enum field name matches enum name"

ENUM_VALUE_IS_UDT = "enum field type cannot be a user defined type"

DUPLICATE_ERROR_FIELD_NAME = "duplicate error field name"

ERROR_AND_FIELD_NAME_COLLISION = "error field matches error name"

INVALID_FIELD_TYPE = "error field is not a identifier"

DUPLICATE_UNION_FIELD_NAME = "duplicate union field name"

DUPLICATE_UNION_FIELD_TYPE = "duplicate union field type"

UNION_AND_FIELD_NAME_COLLISION = "union field name matches union name"

FUNCTION_NAME_COLLISION = "function name matches previous function name"

ARGUMENT_NAME_COLLISION = "function argument name matches previous function argument name"

FN_AND_INTERFACE_NAME_COLLISION = "function name matches interface name"

ARGUMENT_AND_FN_NAME_COLLISION = "function argument name matches function name"

ARGUMENT_AND_PREV_FN_NAME_COLLISION = "function argument name matches previous function name"

ARGUMENT_AND_INTERFACE_NAME_COLLISION = "function argument name matches interface name"

DUPLICATE_IMPORT = "duplicate import item name"

IMPORT_NAME_ALIAS_COLLISION = "import item alias matches import item name"

DUPLICATE_IMPORT_ALIAS = "import item alias matches previous import item alias"

PATH_BACKTRACKING = "import path cannot backtrack up directory paths"

DEFINED_NAME_COLLISION_WITH_COMPONENT = "defined types cannot have the name of any of their components"

DUPLICATE_CASE_VALUE = "duplicate case value"

UNWRAPPED_OPTION_SHADOWS_OPTION = "unwrapped option variable name mathes option variable name"

INVALID_BREAK = "break not found in loop"

UNDEFINED_LOOP_NAME = "undefined loop name"

INVALID_CONTINUE = "continue not found in loop"

START_IDX_SHADOWS_INDEX_VAR = "start index variables name matches iteration index variable name"

STOP_IDX_SHADOWS_INDEX_VAR = "stop index variables name matches iteration index variable name"

ITER_SIZE_SHADOWS_INDEX_VAR = "iteration step variable name matches iteration index variable name"

LOOP_NAME_SHADOWS_INDEX_VAR = "loop name matches iteration index variable name"

STOP_IDX_SHADOWS_START_IDX = "stop index variable name matches start index variable name"

ITER_SIZE_SHADOWS_START_IDX = "iteration step variable name matches stop index variable name"

LOOP_NAME_SHADOWS_START_IDX = "loop name matches start index variable name"

ITER_SIZE_SHADOWS_STOP_IDX = "iteration step variable name matches stop index variable name"

LOOP_NAME_SHADOWS_STOP_IDX = "loop name matches stop index variable name"

LOOP_NAME_SHADOWS_ITER_SIZE = "loop name matches iteration step variable name"

MAP_VALUE_NAME_SHADOWS_KEY_ITEM = "map value variable name matches map key variable name"

COLLECTION_NAME_SHADOWS_ITEM = "collection name matches collection item variable name"

LOOP_NAME_SHADOWS_VALUE_ITEM = "loop name matches map value variable name"

LOOP_NAME_SHADOWS_COLLECTION_NAME = "loop name matches collection variable name"

SECOND_OPT_VAR_SHADOWS_OPT_VAR = "unwrapped optional value variable name matches unwrapped optional key variable name"

LOOP_NAME_SHADOWS_OPTIONAL_VARIABLE = "loop name matches optional variable name"

LOOP_NAME_SHADOWS_OPTIONAL_VALUE_VARIABLE = "loop name matches unwrapped optional map value variable name"

OPTIONAL_COLLECTION_NAME_SHADOWS_OPTIONAL_VARIABLE = "optional collection variable name matches unwrapped optional variable name"

OPTIONAL_COLLECTION_NAME_SHADOWS_OPTIONAL_VALUE_VARIABLE = "optional collection variable name matches unwrapped map value variable name"

STRUCT_FIELD_NAME_COLLISION = "duplicate struct field name"

STRUCT_INTERFACE_NAME_COLLISION = "duplicate interface name in struct"

METHOD_NAME_COLLISION = "duplicate method name"

FUNCTION_ARG_NAME_COLLISION = "name collision, arguments have same name"

RETURN_NOT_LAST_STATEMENT = "return is not last statement in block"

FUNCTION_MISSING_RETURN_PATH = "function not valid, function returns a value, but not all code paths return a value"

DUPLICATE_LOOP_NAME = "duplicate loop name"

CONTINUE_NOT_IN_LOOP = "continue statement only valid inside loops"

BREAK_NOT_IN_LOOP = "break statement only valid inside loops"

LOOP_LABEL_UNDEFINED = "loop label not defined"


#--------------------------- GLOBAL SEMANTIC ERRORS ---------------------------

NON_UNIQUE_MODULE = "module is not uniquely named"

MODULE_NAME_AND_ITEM_COLLISION = "item in module has name that matches its module name"

INVALID_IMPORTED_MODULE = "imported module is not defined"

INVALID_IMPORTED_MODULE_PATH = "imported module not found in included path"

INVALID_IMPORT_PATH_START = "import path must start with current folder name"

IMPORT_PATH_MISSING_PARENT_FOLDER = "import path must contain parent folder name in directory within 10 levels"

PATH_BACKTRACKING = "import path cannot backtrack up directory paths"

DUPLICATE_IMPORT_IN_MODULE = "import of module of same name detected, other modules are only allowed to be imported once in a module"

IMPORT_ITEM_NAME_COLLISION = "item in import matches name of other item also being imported"

#IMPORT_NAME_COLLIDES_WITH_OTHER_IMPORTED_MOD_NAME = "item in import matches name of other module being imported from"

# Get this error in module check also, but should be kept here too, to show all the lcations where it can occur
IMPORT_ITEM_HAS_SAME_NAME_AS_ITS_MODULE = "item in import matches name of module being imported from"

IMPORT_ITEM_NAME_COLLIDES_WITH_MODULE_ITEM = "item in import matches name of another item in module"

IMPORT_ITEM_COLLIDES_WITH_MOD_NAME = "item in import matches name of current module"

IMPORTED_ITEM_NOT_FOUND = "item in import not defined in imported module"

MULTIPLE_MODULES_FOUND_ON_PATH = "multiple modules found on import path"

DEFINE_NEW_NAME_COLLISION = "type definition name matches other items name"

DEFINE_USES_SAME_COMPONENTS = "define statement uses same exact types in definition"

FUNCTION_TYPE_HAS_NO_EFFECT = "function definition does not have arguments or a return value"

UNDEFINED_ITEM_IN_DEFINE_STMT = "define statement contains a argument that is not defined"

ENUMERABLE_NAME_COLLISION_IN_MODULE = "enumerable name matches name of other item in module"

UNDEFINED_ITEM_IN_UNION_STMT = "union elements type is not defined"

ENUMERABLE_LIST_ITEM_NAME_COLLISION_IN_MODULE = "enumurable element name matches name of item in module"

ENUMERABLE_LIST_ITEM_NAME_COLLISION_IN_IMPORT = "enumurable element name matches name of item in import"

INTERFACE_NAME_COLLIDES_WITH_MODULE_ITEM = "interface name matches name of item in module"

INTERFACE_FN_ARG_COLLIDES_WITH_MODULE_ITEM = "interface function argument matches name of item in module"

INTERFACE_FN_NAME_COLLIDES_WITH_IMPORT_ITEM = "interface name matches name of item in import"

INTERFACE_FN_ARG_COLLIDES_WITH_IMPORT_ITEM = "interface function argument matches name of item in import"

INVALID_FUNCTION_ARG_TYPE = "invalid function argument type"

UNDEFINED_TYPE = "Undefined argument type"