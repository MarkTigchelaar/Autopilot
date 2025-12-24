MODULE_NOT_FOUND = "module not found"

IMPORT_PATH_NOT_FOUND = "import path not found"

IMPORT_PATH_AMBIGUOUS = "import path is ambiguous, multiple paths found"

ENUM_HAS_UDT = "enum type cannot be a user defined type"

ENUM_DUP_FIELD_NAME = "duplicate enum field name"

ENUM_DUP_VALUE = "duplicate enum value"

ENUM_MISMATCHED_TYPE = "enum field has mismatched type"

ENUM_AND_FIELD_TYPE_MISMATCH = "enum field type does not match enum type"

ENUM_AND_FIELD_NAME_COLLISION = "enum field name matches enum name"

ENUM_VALUE_IS_UDT = "enum field type cannot be a user defined type"

BOOL_ENUM_TOO_MANY_FIELDS = "bool enum has too many fields, max 2 fields allowed"

CHAR_ENUM_TOO_MANY_FIELDS = "char enum has too many fields, max 256 fields allowed"

ENUM_HAS_NO_TYPE = "enum has no explicit or inferred type"

DUPLICATE_ERROR_FIELD_NAME = "duplicate error field name"

ERROR_AND_FIELD_NAME_COLLISION = "error field matches error name"

INVALID_FIELD_TYPE = "error field is not a identifier"

DUPLICATE_UNION_FIELD_NAME = "duplicate union field name"

DUPLICATE_UNION_FIELD_TYPE = "duplicate union field type"

UNION_AND_FIELD_NAME_COLLISION = "union field name matches union name"

UNION_AND_FIELD_TYPE_COLLISION = "union field type matches union name"

FUNCTION_NAME_COLLISION = "function name matches previous function name"

ARGUMENT_NAME_COLLISION = (
    "function argument name matches previous function argument name"
)

FN_AND_INTERFACE_NAME_COLLISION = "function name matches interface name"

ARGUMENT_AND_FN_NAME_COLLISION = "function argument name matches function name"

ARGUMENT_AND_PREV_FN_NAME_COLLISION = (
    "function argument name matches previous function name"
)

ARGUMENT_AND_INTERFACE_NAME_COLLISION = "function argument name matches interface name"

DUPLICATE_IMPORT = "duplicate import item name"

IMPORT_NAME_ALIAS_COLLISION = "import item alias matches import item name"

DUPLICATE_IMPORT_ALIAS = "import item alias matches previous import item alias"

PATH_BACKTRACKING = "import path cannot backtrack up directory paths"

DEFINED_NAME_COLLISION_WITH_COMPONENT = (
    "defined types cannot have the name of any of their components"
)

DUPLICATE_CASE_VALUE = "duplicate case value"

UNWRAPPED_OPTION_SHADOWS_OPTION = (
    "unwrapped option variable name mathes option variable name"
)

INVALID_BREAK = "break not found in loop"

UNDEFINED_LOOP_NAME = "undefined loop name"

INVALID_CONTINUE = "continue not found in loop"

START_IDX_SHADOWS_INDEX_VAR = (
    "start index variables name matches iteration index variable name"
)

STOP_IDX_SHADOWS_INDEX_VAR = (
    "stop index variables name matches iteration index variable name"
)

ITER_SIZE_SHADOWS_INDEX_VAR = (
    "iteration step variable name matches iteration index variable name"
)

LOOP_NAME_SHADOWS_INDEX_VAR = "loop name matches iteration index variable name"

STOP_IDX_SHADOWS_START_IDX = (
    "stop index variable name matches start index variable name"
)

ITER_SIZE_SHADOWS_START_IDX = (
    "iteration step variable name matches stop index variable name"
)

LOOP_NAME_SHADOWS_START_IDX = "loop name matches start index variable name"

ITER_SIZE_SHADOWS_STOP_IDX = (
    "iteration step variable name matches stop index variable name"
)

LOOP_NAME_SHADOWS_STOP_IDX = "loop name matches stop index variable name"

LOOP_NAME_SHADOWS_ITER_SIZE = "loop name matches iteration step variable name"

MAP_VALUE_NAME_SHADOWS_KEY_ITEM = (
    "map value variable name matches map key variable name"
)

COLLECTION_NAME_SHADOWS_ITEM = "collection name matches collection item variable name"

LOOP_NAME_SHADOWS_VALUE_ITEM = "loop name matches map value variable name"

LOOP_NAME_SHADOWS_COLLECTION_NAME = "loop name matches collection variable name"

SECOND_OPT_VAR_SHADOWS_OPT_VAR = "unwrapped optional value variable name matches unwrapped optional key variable name"

LOOP_NAME_SHADOWS_OPTIONAL_VARIABLE = "loop name matches optional variable name"

LOOP_NAME_SHADOWS_OPTIONAL_VALUE_VARIABLE = (
    "loop name matches unwrapped optional map value variable name"
)

OPTIONAL_COLLECTION_NAME_SHADOWS_OPTIONAL_VARIABLE = (
    "optional collection variable name matches unwrapped optional variable name"
)

OPTIONAL_COLLECTION_NAME_SHADOWS_OPTIONAL_VALUE_VARIABLE = (
    "optional collection variable name matches unwrapped map value variable name"
)

STRUCT_FIELD_NAME_COLLISION = "duplicate struct field name"

#STRUCT_HAS_NO_FIELDS = "struct does not have any fields"

METHOD_NAME_COLLIDES_WITH_STRUCT_NAME = "method name is the same as struct type name"

STRUCT_FIELD_COLLIDES_WITH_STRUCT_NAME = "field name is the same as struct type name"

INTERFACE_NAME_COLLIDES_WITH_STRUCT_NAME = "interface name is the same as struct type name"

STRUCT_INTERFACE_NAME_COLLISION = "duplicate interface name in struct"

METHOD_NAME_COLLISION = "duplicate method name"

STRUCT_FIELD_NAME_COLLIDES_WITH_MODULE_ITEM = "field name collides with module item"

STRUCT_METHOD_NAME_COLLIDES_WITH_MODULE_ITEM = "method name collides with module item"

STRUCT_FIELD_NAME_COLLIDES_WITH_IMPORT_ITEM = "field name collides with import item"

STRUCT_METHOD_NAME_COLLIDES_WITH_IMPORT_ITEM = "method name collides with import item"

FUNCTION_ARG_NAME_COLLISION = "name collision, arguments have same name"

RETURN_NOT_LAST_STATEMENT = "return is not last statement in block"

FUNCTION_MISSING_RETURN_PATH = "function not valid, function returns a value, but not all code paths return a value"

VOID_FUNCTION_RETURNS_VALUE = "function expected to return nothing, but return value found"

FUNCTION_DOES_NOT_RETURN_VALUE = "function expected to return value, but no return value found"

DUPLICATE_LOOP_NAME = "duplicate loop name"

CONTINUE_NOT_IN_LOOP = "continue statement only valid inside loops"

BREAK_NOT_IN_LOOP = "break statement only valid inside loops"

LOOP_LABEL_UNDEFINED = "loop label not defined"


# --------------------------- GLOBAL SEMANTIC ERRORS ---------------------------

NON_UNIQUE_MODULE = "module is not uniquely named"

MODULE_NAME_AND_ITEM_COLLISION = "item in module has name that matches its module name"

INVALID_IMPORTED_MODULE = "imported module is not defined"

INVALID_IMPORTED_MODULE_PATH = "imported module not found in included path"

INVALID_IMPORT_PATH_START = "import path must start with current folder name"

IMPORT_PATH_MISSING_PARENT_FOLDER = (
    "import path must contain parent folder name in directory within 10 levels"
)

PATH_BACKTRACKING = "import path cannot backtrack up directory paths"

DUPLICATE_IMPORT_IN_MODULE = "import of module of same name detected, other modules are only allowed to be imported once in a module"

IMPORT_ITEM_NAME_COLLISION = (
    "item in import matches name of other item also being imported"
)

# IMPORT_NAME_COLLIDES_WITH_OTHER_IMPORTED_MOD_NAME = "item in import matches name of other module being imported from"

# Get this error in module check also, but should be kept here too, to show all the locations where it can occur
IMPORT_STATEMENT_HAS_SAME_NAME_AS_ITS_MODULE = (
    "imported module name matches name of current module"
)

IMPORT_ITEM_NAME_COLLIDES_WITH_MODULE_ITEM = (
    "item in import matches name of another item in module"
)

IMPORT_ITEM_HAS_SAME_NAME_AS_ITS_MODULE  = "item in import matches name of current module"

MODULE_ITEM_NAME_COLLISION = "item in module collides with another item in same module"

IMPORTED_ITEM_NOT_FOUND = "item in import not defined in imported module"

DUPLICATE_IMPORTED_ITEM = "item in import has duplicate definition in imported module"

MULTIPLE_MODULES_FOUND_ON_PATH = "multiple modules found on import path"

DEFINE_NEW_NAME_COLLISION = "define statement names new type the same as another type"

TYPE_NOT_DEFINED = "type is not defined"

# DEFINE_NEW_NAME_COLLISION_W_IMPORT = (
#     "define statement names new type the same as an imported type"
# )

DEFINE_USES_SAME_COMPONENTS = (
    "define statement uses same exact types in definition as other define statement"
)

FUNCTION_TYPE_HAS_NO_EFFECT = (
    "function definition does not have arguments or a return value"
)

UNDEFINED_ITEM_IN_DEFINE_STMT = (
    "define statement contains a argument that is not defined"
)

ENUMERABLE_NAME_COLLISION_IN_MODULE = (
    "enumerable name matches name of other item in module"
)

UNION_MEMBER_NAME_ALREADY_MATCHED_TO_TYPE = "union member name already matched to type"

UNION_MEMBER_INVALID_TYPE = "union member type is not valid"

UNDEFINED_ITEM_IN_UNION_STMT = "union element type is not defined"

UNDEFINED_IMPORT_ITEM_IN_IMPORT_STMT = "union member type not found in imported module"

ENUMERABLE_LIST_ITEM_NAME_COLLISION_IN_MODULE = (
    "enumurable element name matches name of item in module"
)

ENUMERABLE_LIST_ITEM_NAME_COLLISION_IN_IMPORT = (
    "enumurable element name matches name of item in import"
)

INTERFACE_NAME_COLLIDES_WITH_MODULE_ITEM = (
    "interface name matches name of item in module"
)

INTERFACE_NAME_COLLIDES_WITH_IMPORT = "interface name matches name of item in import"

INTERFACE_FN_ARG_COLLIDES_WITH_MODULE_ITEM = (
    "interface function argument matches name of item in module"
)

INTERFACE_FN_NAME_COLLIDES_WITH_IMPORT_ITEM = (
    "interface name matches name of item in import"
)

INTERFACE_FN_ARG_COLLIDES_WITH_IMPORT_ITEM = (
    "interface function argument matches name of item in import"
)

INVALID_FUNCTION_ARG_TYPE = "invalid function argument type"

INVALID_FUNCTION_RETURN_TYPE = "invalid function return type"

UNDEFINED_TYPE = "Undefined argument type"

CYCLE_IN_DEFINE_DEPENDANCIES = "cycle in define statement dependancies"

NON_ERROR_TYPE_IN_RESULT = "non error type for alternative value in result definition"

UNIONS_NOT_HASHABLE = "union type is not hashable"

ENUMS_NOT_HASHABLE = "enum type is not hashable"

ERRORS_NOT_HASHABLE = "error type is not hashable"

FUNCTIONS_NOT_HASHABLE = "function types are not hashable"

STRUCT_HASH_FUNCTION_WRONG_RETURN_TYPE = (
    "struct hash function does not return a int value"
)

STRUCT_HASH_FUNCTION_WRONG_ARG_COUNT = (
    "struct hash function does not have the correct number of arguments, should be 0"
)

UNDEFINED_STRUCT_FIELD = "undefined struct field type"

INVALID_STRUCT_FIELD_TYPE = "invalid struct field type"

UNDEFINED_STRUCT_INTERFACE = "undefined struct interface"

INVALID_STRUCT_INTERFACE = "invalid struct interface"

INTERFACES_NOT_HASHABLE = "interface types are not hashable"

GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES = "type define statement can only contain primitives, unions, enums, structs, interfaces, function, options and results"

LIST_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "general list " + GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

LINKED_LIST_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "linked list " + GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

VECTOR_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "vector " + GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "queue " + GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

FIFO_QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "fifo queue " + GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

DEQUE_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "deque " + GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

PRIORITY_QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "priority queue " + GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

STACK_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "stack " + GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

GENERIC_SET_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "type define statement can only contain primitives, structs and interfaces"
)

SET_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "general set " + GENERIC_SET_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

HASHSET_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "hash set " + GENERIC_SET_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

TREESET_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "tree set " + GENERIC_SET_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

MAP_TYPE_VALUE_DEFINE_NESTING_INVALID_DEFINES = (
    "map value " + GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

HASHMAP_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "hashmap value " + GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

DICT_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "dictionary value" + GENERIC_LINEAR_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

GENERIC_MAP_KEY_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "type can only be primitives, structs or interfaces"
)

MAP_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES = (
    "map key " + GENERIC_MAP_KEY_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

HASHMAP_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES = (
    "hashmap key " + GENERIC_MAP_KEY_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

DICT_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES = (
    "dictionary key " + GENERIC_MAP_KEY_TYPE_DEFINE_NESTING_INVALID_DEFINES
)

OPTION_TYPE_DEFINE_NESTING_INVALID_DEFINES = (
    "optional value type cannot be a result type"
)

RESULT_TYPE_DEFINE_NESTING_INVALID_DEFINES = "result value type cannot be a option type"

RESULT_TYPE_ERROR_DEFINE_NESTING_INVALID_DEFINES = "result error type must be an error"

FUNCTION_TYPE_ARG_DEFINE_NESTING_INVALID_DEFINES = (
    "function argument type cannot be a error type"
)

FUNCTION_TYPE_RETURN_VAL_DEFINE_NESTING_INVALID_DEFINES = (
    "function return value type cannot be a error type"
)

STRUCT_NAME_COLLIDES_WITH_MODULE_ITEM = "struct name matches name of item in module"

STRUCT_NAME_COLLIDES_WITH_IMPORT = "struct name matches name of item in import"

STRUCT_INTERFACE_MATCHES_TO_MULTIPLE_INTERFACES = (
    "struct interface matches to multiple interfaces"
)

FUNCTION_NAME_COLLIDES_WITH_MODULE_ITEM = "function name matches name of item in module"

FUNCTION_NAME_COLLIDES_WITH_IMPORT = "function name matches name of item in import"


DUPLICATE_DECLARATION = "variable declaration shadows previous declaration"


UNDEFINED_VARIABLE = "undefined variable"

UNDECLARED_EXP_VAR = "undeclared expression variable"

RE_ASSIGNMENT_OF_LET_VARIABLE = "variables declared with let keyword are not re assignable"

EXP_VAR_TYPE_MISMATCH = (
    "expression variable type does not match declared type of variable"
)

INVALID_PREFIX_EXP = "expression not compatible with prefix"

INVALID_BINARY_EXP = "expression not compatible with binary operator"

INCOMPATIBLE_EXPRESSION_TYPES = "incompatible expression types"


FUNCTION_NOT_DEFINED = "function is not defined"

REFERENCED_ITEM_IS_NOT_A_FUNCTION = "referenced item is not a function or initializer"

FUNCTION_CALLED_HAS_NO_RETURN_TYPE = "function being called has no return type"

FUNCTION_CALL_ARG_NUMBER_MISMATCH = (
    "function being called has different number of arguments"
)

MULTIPLE_MAIN_FUNCTIONS = "multiple main functions found"

NO_MAIN_FUNCTION = "no main function found in main module"

MAIN_FUNCTION_IN_NON_MAIN_MODULE = "main function found in non main module"

FUNCTION_CALL_ARG_TYPE_MISMATCH = "function argument is incorrect type"

CONSTRUCTOR_IS_NOT_ONLY_EXP_AST_ELEMENT = "constructors must be the only element in an expression"

MULTIPLE_MAP_DELIMITERS_FOUND = "multiple map delimiters found for map key value pair"

MISSING_MAP_DELIMITER = "missing map delimiter for map key value pair"

INCONSISTANT_MAP_KEY_TYPES = "inconsistant map key types"

INCONSISTANT_MAP_VALUE_TYPES = "inconsistant map value types"

INCONSISTANT_HASH_ELEMENT_TYPES = "inconsistant set element types"

UNHASHABLE_HASH_ELEMENT_TYPES = "unhashable set element types"

UNHASHABLE_MAP_KEY_TYPES = "unhashable map key types"

INCONSISTANT_LIST_ELEMENT_TYPES = "inconsistant list element types"

COLLECTION_ACCESS_WITH_WRONG_NUMBER_OF_ARGUMENTS = "collection access requires exactly one argument"


VARIABLE_NAME_MATCHES_UNITTEST = "variable name matches unittest name"


EXP_DOES_NOT_RESOLVE_TO_BOOL = "expression does not resolve to a boolean"

CASE_TYPE_MISMATCH = "case type does not match switch test expression type"


VARIABLE_NOT_DEFINED = "variable is not defined"



UNDEFINED_ENUM_FIELD = "enum field is not defined"

UNDEFINED_UNION_FIELD = "union field is not defined"

UNDEFINED_STRUCT_FIELD = "struct field is not defined"

UNION_FIELD_TYPE_UNDEFINED = "union fields type is not defined"

ACCESS_OF_PREVIOUSLY_DECLARED_ENUMS_FIELD = "direct access of previously declared enums field is illegal"

ENUM_HAS_NO_FIELDS_OR_METHODS = "enum fields cannot have fields or methods"

ENUM_FIELD_HAS_FIELDS_OR_METHODS = "enum field cannot have fields or methods"

STRUCT_FIELD_TYPE_UNDEFINED = "struct fields type is not defined"

CONSTRUCTOR_CALL_ARG_NUMBER_MISMATCH = "constructor being called has different number of arguments"


UNION_CONSTRUCTOR_HAS_MORE_THAN_ONE_ARG = "union constructor has more than one argument"

ILLEGAL_UNION_ACCESS = "illegal access of union field"

ILLEGAL_UNION_METHOD_CALL = "illegal method call on union"

STRUCT_CONSTRUCTOR_ARG_TYPE_MISMATCH = "union constructor argument type does not match any union type"

STRUCT_CONSTRUCTOR_ARG_TYPE_MISMATCH = "struct constructor argument type does not match struct type"

PRIMITIVE_TYPE_HAS_NO_FIELDS_OR_METHODS = "primitive type has no fields or methods"

DIRECT_ACCESS_OF_ERROR_FIELD = "direct access of error field is illegal, errors must be handled with result types"

INTERFACE_METHOD_RETURN_TYPE_UNDEFINED = "interface method return type is not defined"

UNDEFINED_INTERFACE_METHOD = "interface method is not defined"

KEY_VALUE_METHOD_RETURN_TYPE_UNDEFINED = "key value method return type is not defined"

LIST_FIELD_TYPE_UNDEFINED = "list field type is not defined"

UNDEFINED_LIST_METHOD = "list method is not defined"

STACK_FIELD_TYPE_UNDEFINED = "stack field type is not defined"

DEQUEUE_FIELD_TYPE_UNDEFINED = "dequeue field type is not defined"

UNDEFINED_DEQUEUE_METHOD = "dequeue method is not defined"

SET_FIELD_TYPE_UNDEFINED = "set field type is not defined"

UNDEFINED_SET_METHOD = "set method is not defined"

FAILABLE_TYPE_HAS_NO_FIELDS_OR_METHODS = "Options and Results do not have methods or fields"
