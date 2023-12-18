from SemanticAnalysis.Database.database import Database

import ErrorHandling.semantic_error_messages as ErrMsg

from SemanticAnalysis.AnalysisComponents.GlobalAnalysis.import_analyzer import ImportAnalyzer
from SemanticAnalysis.AnalysisComponents.GlobalAnalysis.define_analyzer import DefineAnalyzer
from SemanticAnalysis.AnalysisComponents.GlobalAnalysis.enumerable_analyzer import EnumerableAnalyzer
from SemanticAnalysis.AnalysisComponents.GlobalAnalysis.interface_analyzer import InterfaceAnalyzer

# NOTE: Most types of objects check their own names against names of other items in their own
#       module, so multiple name collision errors can occur. This is ok, because the compiler doesn't know which
#       item is copying the name of the other item, so complain about all of them!
class SemanticAnalyzer:
    def __init__(self, error_manager, database=None):
        self.error_manager = error_manager
        if database is None:
            self.database = Database(error_manager)
        else:
            self.database = database

        self.call_graph = dict()
        self.ref_graph = dict()
        self.import_dependency_graph = dict()
        self.import_analyzer = None
        self.define_analyzer = None
        self.enum_analyzer = None

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def save_item_to_data_store(self, ast_node_saver):
        ast_node_saver.save_to_db(self.database)

    def run_global_analysis(self):
        for object_id in range(self.database.object_count()):
            match self.database.get_tablename_for_object(object_id):
                case "modules":
                    self.run_module_checks(object_id)
                case "imports":
                    self.run_import_checks(object_id)
                case "defines":
                    continue
                    # self.run_define_checks(object_id)
                case "enumerables":
                    continue
                    # self.run_enumerable_checks(object_id)
                case "functions":
                    self.run_function_checks(object_id)
                case "interfaces":
                    self.run_interface_checks(object_id)
                case "structs":
                    self.run_struct_checks(object_id)
                # Figure out how to add unittests
                case _:
                    self.identify_type(object_id)
        # Then checkimports, functions, and ref types for cycles

    # NOTE: Semantic Analyzer should not error if some imported module has code that is not referenced
    #       by anything being used in the program.
    def run_module_checks(self, object_id):
        """
        Need to check if same module name is defined in places other than
        a given directory, it's preferable to just have unique module names in general.
        """
        first_module_object = self.database.get_object(object_id)
        module_table = self.database.get_table("modules")
        module_name_and_path = module_table.get_module_for_id(object_id)
        other_modules_with_same_name = module_table.get_modules_data_for_name(
            module_name_and_path.module_name.literal
        )
        # print(f"number of modules: {len(other_modules_with_same_name)}")
        for mod in other_modules_with_same_name:
            if mod.module_id == object_id:
                # print(f"Found same module, skipping {mod.id}")
                continue
            elif object_id > mod.module_id:
                # Collision already recorded
                # print(f"collision reported for {object_id}")
                break  # because first module (lowest id) already found ALL collisions
            if mod.path == module_name_and_path.path:
                raise Exception(
                    "INTERNAL ERROR: Other module found with same path, should be same module"
                )
            module_object = self.database.get_object(mod.module_id)
            # print(f"Recording for {object_id}")
            self.add_error(
                module_object.name, ErrMsg.NON_UNIQUE_MODULE, first_module_object.name
            )
        self.check_items_in_module_for_name_collisions_with_module(object_id)

    
    def check_items_in_module_for_name_collisions_with_module(self, object_id):
        typename_table = self.database.get_table("typenames")
        other_items_in_module = typename_table.get_items_by_module_id(object_id)

        for item in other_items_in_module:
            if item.object_id == object_id:
                continue
            if item.name_token.literal == item.module_name:
                self.add_error(
                    item.name_token,
                    ErrMsg.MODULE_NAME_AND_ITEM_COLLISION,
                    item.module_name,
                )

    def run_import_checks(self, object_id):
        if self.import_analyzer is None:
            self.import_analyzer = ImportAnalyzer(self.database, self.error_manager, self.import_dependency_graph)
        self.import_analyzer.analyze(object_id)

    def run_define_checks(self, object_id):
        if self.define_analyzer is None:
            self.define_analyzer = DefineAnalyzer(self.database, self.error_manager, self.import_dependency_graph)
        self.define_analyzer.analyze(object_id)

    # Unions, enums, and errors
    # unions have types, they must be checked (like defines)
    # enums only have primitive types, this might have been covered by local analysis (check that)
    # enums and errors must have field names not named the same as other items in module



    def run_enumerable_checks(self, object_id):
        """
        Check that the name does not collide with other names in import lists / module
        """
        if self.enum_analyzer is None:
            self.enum_analyzer = EnumerableAnalyzer(self.database, self.error_manager)
        self.enum_analyzer.analyze(object_id)

    def run_interface_checks(self, object_id):
        if self.interface_analyzer is None:
            self.interface_analyzer = InterfaceAnalyzer(self.database, self.error_manager)
        self.interface_analyzer.analyze(object_id)

    def run_function_checks(self, object_id):
        """
        Check that argument types are defined somewhere
        Check that function name has no collisions
        Check the variable names are defined in their scope
        Check types for argument re assignment
        check types of expressions
        Check method and function calls
        Register current function as caller of any called functions to later check inline / acyclic rules
        Check fields and methods of types referenced in function
        Check arguments to other functions and methods
        Enforce enumerable type rules, like with switch statements for unions
        Enforce optional variable rules.
        Enforce that collections return Results or Optionals if guarantee of membership is not present
        Check that Errors in results have valid fields
        Check that break statements that refer to labels have labels that exist
        Check that labels have no name collisions
        Check assignment types, for let, and var
        Check if expressions violate int / float promotion rules
        Check that function / method calls are public
        """
        function_object = self.database.get_object(object_id)

    def run_struct_checks(self, object_id):
        """
        Check for name collisions
        Check functions for references to fields, or make function checks try to get struct fields
        Add fields to reference graph table to later check inline / acyclic rules
        """
        struct_object = self.database.get_object(object_id)

    def identify_type(self, object_id):
        print(f"\nObject not in list: {object_id}, is likely header, or modifier")
        header_table = self.database.get_table("fn_headers")
        modifier_table = self.database.get_table("modifiers")
        if header_table.is_object_defined(object_id):
            print(f"--> Is a function header")
        # BC modifiers use the object ids of the things they modify
        if modifier_table.is_object_defined(object_id):
            print(f"--> Is a modifier")
        else:
            raise Exception("Shit, I don't know what that is. :(")
