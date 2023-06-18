from SemanticAnalysis.Database.table import Table

def make_all_tables():
    tables = dict()
    tables["Objects"] = make_objects_table()
    tables["TypeNames"] = make_type_defs_table()
    tables["Structs"] = make_structs_table()
    tables["StructFields"] = make_struct_fields_table()
    tables["Functions"] = make_functions_table()
    tables["FunctionSignatures"] = make_function_signatures_table()
    tables["Defines"] = make_defines_table()
    tables["StatementLists"] = make_statement_lists_table()
    tables["Statements"] = make_statements_table()
    tables["Modules"] = make_modules_table()
    tables["ModuleSrcFiles"] = make_module_source_files_table()
    tables["ModuleItems"] = make_module_items_table()
    tables["ModuleImports"] = make_module_imports_table()
    tables["ImportPaths"] = make_import_paths_table()
    tables["ImportItems"] = make_import_items_table()
    tables["Errors"] = make_errors_table()
    tables["ErrorFields"] = make_error_fields_table()
    tables["Enums"] = make_enums_table()
    tables["EnumFields"] = make_enum_fields_table()
    tables["BinaryExpressions"] = make_binary_expressions_table()
    tables["OptResultAssignExpressions"] = make_opt_result_assign_expressions_table()
    tables["RangeExpressions"] = make_range_expressions_table()
    tables["CollectionExpressions"] = make_collection_expressions_table()
    tables["FunctionCallExpressions"] = make_function_call_expressions_table()
    return tables

def make_objects_table():
    # main table that connects back to the AST
    columns = ["object_id", "type_id", "status_code", "name", "access_modifier", "object_reference"]
    objects = Table("Objects", columns)
    objects.make_index("object_id")
    return objects

def make_type_defs_table():
    columns = ["type_id", "type_def_name"]
    type_defs = Table("TypeDefNames", columns)
    type_defs.make_index("type_id")
    return type_defs

def make_structs_table():
    columns = ["object_id", "interface_id_list"]
    structs = Table("Structs", columns)
    structs.make_index("object_id")
    return structs

def make_struct_fields_table():
    columns = ["object_id", "struct_id", "mutation_type", "default_value"]
    structs = Table("StructFields", columns)
    structs.make_index("object_id")
    return structs

def make_functions_table():
    columns = ["object_id", "signature_id", "owner_id"]
    functions = Table("Functions", columns)
    functions.make_index("object_id")
    return functions

def make_function_signatures_table():
    columns = ["object_id", "return_type_object_id"]
    signatures = Table("FunctionSignatures", columns)
    signatures.make_index("object_id")
    return signatures

def make_defines_table():
    columns = ["object_id", "owner_id", "container_type_id", "lhs_type_id", "rhs_type_id"]
    defines = Table("Defines", columns)
    defines.make_index("object_id")
    return defines

def make_statement_lists_table():
    columns = ["object_id", "owner_id", "scope_level"]
    statement_lists = Table("StatementLists", columns)
    statement_lists.make_index("object_id")
    return statement_lists

def make_statements_table():
    columns = ["object_id", "owner_id", "position_number", "type"]
    statements = Table("Statements", columns)
    statements.make_index("object_id")
    return statements

def make_modules_table():
    columns = ["object_id", "directory_path"]
    modules = Table("Modules", columns)
    modules.make_index("object_id")
    return modules

def make_module_source_files_table():
    columns = ["object_id", "owner_id", "file_name"]
    source_files = Table("ModuleSrcFiles", columns)
    source_files.make_index("object_id")
    return source_files

def make_module_items_table():
    columns = ["object_id", "module_id"]
    module_items = Table("ModuleItems", columns)
    module_items.make_index("object_id")
    return module_items

def make_module_imports_table():
    columns = ["object_id", "module_id", "import_type", "import_name"]
    module_imports = Table("ModuleImports", columns)
    module_imports.make_index("object_id")
    return module_imports

def make_import_paths_table():
    columns = ["object_id", "import_id"]
    import_paths = Table("ImportPaths", columns)
    import_paths.make_index("object_id")
    return import_paths

def make_import_items_table():
    columns = ["object_id", "import_id"]
    import_items = Table("ImportItems", columns)
    import_items.make_index("object_id")
    return import_items

def make_errors_table():
    columns = ["object_id", "owner_id", "type_id"]
    errors = Table("Errors", columns)
    errors.make_index("object_id")
    return errors

def make_error_fields_table():
    columns = ["object_id", "error_id"]
    error_fields = Table("ErrorFields", columns)
    error_fields.make_index("object_id")
    return error_fields

def make_enums_table():
    columns = ["object_id", "owner_id", "type_id"]
    enums = Table("Enums", columns)
    enums.make_index("object_id")
    return enums

def make_enum_fields_table():
    columns = ["object_id", "enum_id", "default_value"]
    enum_fields = Table("EnumFields", columns)
    enum_fields.make_index("object_id")
    return enum_fields

def make_binary_expressions_table():
    columns = ["object_id", "lhs_exp_id", "rhs_exp_id", "owner_id"]
    binary_expressions = Table("BinaryExpressions", columns)
    binary_expressions.make_index("object_id")
    return binary_expressions

def make_opt_result_assign_expressions_table():
    columns = ["object_id", "owner_id", "unwrapped_var_id", "wrapped_var_id"]
    opt_result_assign_expressions = Table("OptResultAssignExpressions", columns)
    opt_result_assign_expressions.make_index("object_id")
    return opt_result_assign_expressions

def make_range_expressions_table():
    columns = ["object_id", "owner_id", "index_variable_object_id", "idx_start_object_id", "idx_stop_object_id", "iter_step_object_id"]
    range_expressions = Table("RangeExpressions", columns)
    range_expressions.make_index("object_id")
    return range_expressions

def make_collection_expressions_table():
    columns = ["object_id", "owner_id", "item_or_key_object_id", "value_item_object_id", "collection_id"]
    collection_expressions = Table("CollectionExpressions", columns)
    collection_expressions.make_index("object_id")
    return collection_expressions

def make_function_call_expressions_table():
    columns = ["object_id", "owner_id", "argument_id_list"]
    function_call_expressions = Table("FunctionCallExpressions", columns)
    function_call_expressions.make_index("object_id")
    return function_call_expressions
