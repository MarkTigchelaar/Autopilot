import os
import sys

from Tokenization.tokenizer import Tokenizer
from ErrorHandling.error_manager import ErrorManager
from driver import Driver
from Parsing.parse import parse_src
from Parsing.ExternalStatementParsing.module_parsing import parse_module
from SemanticAnalysis.semantic_analyzer import SemanticAnalyzer
from SemanticAnalysis.AnalysisComponents.module_path_matcher import ModulePathMatcher
import ErrorHandling.semantic_error_messages as ErrMsgs
from ErrorHandling.parsing_error_messages import MODULE_EXPECTED
import symbols

FIRST_MODULE_NAME = "main"


class Parser:
    def __init__(self, current_dir):
        self.current_dir = current_dir
        self.error_manager = ErrorManager()
        self.analyzer = SemanticAnalyzer(self.error_manager)
        self.tokenizer = Tokenizer(self.error_manager)
        self.driver = Driver(self.tokenizer, self.error_manager, self.analyzer)
        self.raw_modules = []
        self.module_location_lookup = dict()
        self.unparsed_source_paths = []

    def get_errors(self):
        return self.error_manager.get_errors()

    def get_raw_modules(self):
        return RawModuleCollection(self.raw_modules, self.error_manager)

    def parse_source(self, source_code_module_path):
        normalized_path = os.path.normpath(self.current_dir + source_code_module_path)
        self.parse_main(normalized_path)
        if len(self.raw_modules) == 0 and self.error_manager.has_errors():
            return
        self.aqquire_latest_module_import_paths()
        while self.has_modules_to_parse():
            self.parse_next_module()

    def parse_main(self, source_code_module_path):
        module_count = len(self.raw_modules)
        self.parse_module(source_code_module_path, FIRST_MODULE_NAME)
        if (
            len(self.raw_modules) == module_count
            and not self.error_manager.has_errors()
        ):
            # no parsing -> no tokens, so just exit
            sys.exit(
                f"No {FIRST_MODULE_NAME} module found in the source code directory {source_code_module_path}"
            )

    def parse_module(self, source_code_module_path, module_name):
        list_1 = os.listdir(path=source_code_module_path)
        #print(list_1)
        check_list = []
        parse_list = []
        skip_list = []
        for file in list_1:
            if file.endswith(".ap"):
                check_list.append(file)
        for file in check_list:
            full_path = source_code_module_path + "/" + file
            normalized_path = os.path.normpath(full_path)
            mod_name = self.find_module_name(normalized_path)
            if mod_name is None:
                continue
            if mod_name == module_name:
                parse_list.append(normalized_path)
            else:
                skip_list.append(normalized_path)

        if len(parse_list) == 0:
            # No module with the given name found
            self.log_missing_imported_module(module_name)
            return
        ast_list = []
        for file in parse_list:
            print(f"Parsing file: {file}")
            self.tokenizer.load_src(file)
            file_ast_list = parse_src(self.driver)
            self.reset_tokenizer()
            
            if file_ast_list is not None and len(file_ast_list) > 0:
                ast_list.extend(file_ast_list)
                #print(f"length of file_ast_list: {len(file_ast_list)}")
            #print(f"length of ast_list: {len(ast_list)}")

        self.convert_to_raw_module(
            ast_list, module_name, parse_list, skip_list, source_code_module_path
        )
        if source_code_module_path not in self.module_location_lookup:
            self.module_location_lookup[source_code_module_path] = []
        self.module_location_lookup[source_code_module_path].append(module_name)

    def log_missing_imported_module(self, module_name):
        previous_module = self.raw_modules[-1]
        imports = previous_module.imports
        for import_statement in imports:
            import_path = import_statement.get_path_list()
            if import_path[-1].node_token.literal == module_name:
                self.error_manager.add_semantic_error(
                    import_path[-1].node_token, ErrMsgs.MODULE_NOT_FOUND
                )
                return

    def has_modules_to_parse(self):
        return len(self.unparsed_source_paths) > 0

    def parse_next_module(self):
        unparsed_module = self.unparsed_source_paths.pop(0)
        current_count_of_raw_modules = len(self.raw_modules)
        self.parse_module(
            unparsed_module.source_code_module_path, unparsed_module.module_name
        )
        if len(self.raw_modules) == current_count_of_raw_modules:
            return
        self.aqquire_latest_module_import_paths()

    def aqquire_latest_module_import_paths(self):
        last_module = self.raw_modules[-1]
        normalized_path = os.path.normpath(last_module.directory_path)
        temp_path_module_lookup = dict()
        for import_statement in last_module.imports:
            if import_statement.import_type == "library":
                continue
            import_path = import_statement.get_path_list()
            module_name = import_path[-1].node_token.literal
            matcher = ModulePathMatcher(
                last_module.id, import_path, normalized_path, self.error_manager
            )
            matcher.collect_valid_paths()
            matching_directories = matcher.get_matching_directories()
            if len(matching_directories) == 0:
                print("path not found!!!")
                self.error_manager.add_semantic_error(
                    import_path[-1].node_token, ErrMsgs.IMPORT_PATH_NOT_FOUND
                )
                return
            if len(matching_directories) > 1:
                self.error_manager.add_semantic_error(
                    import_path[-1].node_token, ErrMsgs.IMPORT_PATH_AMBIGUOUS
                )
                return

            if list(matching_directories)[0] not in temp_path_module_lookup:
                unparsed_module = UnparsedModule(
                    list(matching_directories)[0], module_name, import_statement
                )
                self.unparsed_source_paths.append(unparsed_module)
                temp_path_module_lookup[list(matching_directories)[0]] = [module_name]
            elif module_name in temp_path_module_lookup[list(matching_directories)[0]]:
                continue
            else:
                temp_path_module_lookup[list(matching_directories)[0]].append(
                    module_name
                )
                unparsed_module = UnparsedModule(
                    list(matching_directories)[0], module_name, import_statement
                )
                self.unparsed_source_paths.append(unparsed_module)

    def find_module_name(self, source_code_file_path):
        self.tokenizer.load_src(source_code_file_path)
        module_ast = self.find_module_name_in_file(self.driver)
        self.reset_tokenizer()
        if module_ast is None:
            return None
        return module_ast.get_name().literal

    # This is used by the main parser when looking for files to parse
    # for a given module, in the same directory.
    # This is skipped
    def find_module_name_in_file(self, driver):
        peek_token = driver.peek_token()
        if peek_token.type_symbol == symbols.MODULE:
            return parse_module(driver)
        else:
            driver.add_error(peek_token, MODULE_EXPECTED)
            return None

    def convert_to_raw_module(
        self, ast_list, module_name, parse_list, skip_list, source_code_module_path
    ):
        raw_module = RawModule(module_name, len(self.raw_modules))
        raw_module.directory_path = source_code_module_path
        raw_module.included_files = parse_list
        raw_module.excluded_files = skip_list
        for ast_node in ast_list:
            count = raw_module.item_count()
            self.add_if_module(raw_module, ast_node)
            self.add_if_import(raw_module, ast_node)
            self.add_if_define(raw_module, ast_node)
            self.add_if_enum(raw_module, ast_node)
            self.add_if_error(raw_module, ast_node)
            self.add_if_interface(raw_module, ast_node)
            self.add_if_union(raw_module, ast_node)
            self.add_if_struct(raw_module, ast_node)
            self.add_if_function(raw_module, ast_node)
            self.add_if_unittest(raw_module, ast_node)

            new_count = raw_module.item_count()
            assert new_count > count
        self.raw_modules.append(raw_module)

    def add_if_module(self, raw_module, ast_node):
        if str(ast_node.__class__.__name__) != "ModuleStatement":
            return
        raw_module.module_statements.append(ast_node)

    def add_if_import(self, raw_module, ast_node):
        if str(ast_node.__class__.__name__) != "ImportStatement":
            return
        raw_module.imports.append(ast_node)

    def add_if_define(self, raw_module, ast_node):
        if str(ast_node.__class__.__name__) != "DefineStatement":
            return
        if str(ast_node.sub_type.__class__.__name__) == "KeyValueType":
            raw_module.key_value_defines.append(ast_node)
        elif str(ast_node.sub_type.__class__.__name__) == "LinearType":
            raw_module.linear_type_defines.append(ast_node)
        elif str(ast_node.sub_type.__class__.__name__) == "FailableType":
            raw_module.failable_type_defines.append(ast_node)
        elif str(ast_node.sub_type.__class__.__name__) == "FunctionType":
            raw_module.function_type_defines.append(ast_node)
        else:
            raise Exception("Unknown define type")

    def add_if_enum(self, raw_module, ast_node):
        if str(ast_node.__class__.__name__) != "EnumStatement":
            return
        raw_module.enums.append(ast_node)

    def add_if_error(self, raw_module, ast_node):
        if str(ast_node.__class__.__name__) != "ErrorStatement":
            return
        raw_module.errors.append(ast_node)

    def add_if_interface(self, raw_module, ast_node):
        if str(ast_node.__class__.__name__) != "InterfaceStatement":
            return
        raw_module.interfaces.append(ast_node)

    def add_if_union(self, raw_module, ast_node):
        if str(ast_node.__class__.__name__) != "UnionStatement":
            return
        raw_module.unions.append(ast_node)

    def add_if_struct(self, raw_module, ast_node):
        if str(ast_node.__class__.__name__) != "StructStatement":
            return
        raw_module.structs.append(ast_node)

    def add_if_function(self, raw_module, ast_node):
        if str(ast_node.__class__.__name__) != "FunctionStatement":
            return
        raw_module.functions.append(ast_node)

    def add_if_unittest(self, raw_module, ast_node):
        if str(ast_node.__class__.__name__) != "UnittestStatement":
            return
        raw_module.unit_tests.append(ast_node)

    def reset_tokenizer(self):
        self.tokenizer.close_src()
        self.tokenizer = Tokenizer(self.error_manager)
        self.driver.tokenizer = self.tokenizer

    def has_errors(self):
        return self.error_manager.has_errors(True)

    def report_errors(self):
        self.error_manager.report_errors()


class UnparsedModule:
    def __init__(self, source_code_module_path, module_name, import_statement):
        self.source_code_module_path = source_code_module_path
        self.module_name = module_name
        self.import_statement = import_statement


# After parsing is done, as well as local analysis, a list of these objects
# is what is produced. This is the raw data that is then used to generate
# the IL for autopilot, called APIL.
class RawModule:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.directory_path = None
        self.included_files = []
        self.excluded_files = []
        self.module_statements = []
        # self.defines = []
        self.key_value_defines = []
        self.linear_type_defines = []
        self.failable_type_defines = []
        self.function_type_defines = []
        self.enums = []
        self.errors = []
        self.interfaces = []
        self.unions = []
        self.structs = []
        self.functions = []
        self.imports = []
        self.unit_tests = []
        self.built_in_libs = dict()
    
    def get_built_in_libs(self):
        return self.built_in_libs

    def item_count(self):
        count = len(self.module_statements)
        count += len(self.key_value_defines)
        count += len(self.linear_type_defines)
        count += len(self.failable_type_defines)
        count += len(self.function_type_defines)
        count += len(self.enums)
        count += len(self.errors)
        count += len(self.interfaces)
        count += len(self.unions)
        count += len(self.structs)
        count += len(self.functions)
        count += len(self.imports)
        count += len(self.unit_tests)
        return count
    




class RawModuleCollection:
    def __init__(self, raw_modules, error_manager):
        self.raw_modules = raw_modules
        self.error_manager = error_manager
        self.built_in_libs = dict()

    def get_error_manager(self):
        return self.error_manager

    def has_errors(self):
        return self.error_manager.has_errors(True)
    
    def report_errors(self):
        self.error_manager.report_errors()
        
    def get_raw_modules(self):
        return self.raw_modules

    def add_built_in_libs(self, built_in_libs):
        self.built_in_libs.update(built_in_libs)
        for module in self.raw_modules:
            module.built_in_libs.update(built_in_libs)
    
    def get_built_in_libs(self):
        return self.built_in_libs