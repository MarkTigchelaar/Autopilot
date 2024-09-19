from ErrorHandling.error_manager import ErrorManager
import ErrorHandling.semantic_error_messages as ErrMsg
from ASTComponents.raw_modules import RawModuleCollection
from SemanticAnalysis.AnalysisComponents.module_path_matcher import ModulePathMatcher
from symbols import OPTION, RESULT
import symbols
from keywords import is_primitive_type


class DefineAnalyzer:
    def __init__(
        self, error_manager: ErrorManager, collected_modules: RawModuleCollection
    ):
        self.error_manager = error_manager
        self.collected_modules = collected_modules

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)

    def analyze(self):
        raw_modules = self.collected_modules.get_raw_modules()
        for i, raw_module in enumerate(raw_modules):
            self.analyze_individual_module(i, raw_module, raw_modules)

    def analyze_individual_module(self, index, raw_module, raw_modules):
        self.check_other_defines_for_same_components(raw_module)
        self.check_for_function_type_with_no_args_no_return_type(raw_module)
        self.check_elements_in_define_are_defined_and_permitted(raw_module)

    def check_other_defines_for_same_components(self, raw_module):
        self.analyze_kv_pair_defines_for_same_components(raw_module)
        self.analyze_linear_defines_for_same_components(raw_module)
        self.analyze_optional_or_result_type_for_same_components(raw_module)
        self.function_defines_for_same_components(raw_module)

    def analyze_kv_pair_defines_for_same_components(self, raw_module):
        def kv_define_component_compare(comparer, comparee) -> bool:
            if comparer.key_type.literal == comparee.key_type.literal:
                if comparer.value_type.literal == comparee.value_type.literal:
                    return True
            return False

        kv_defines = raw_module.key_value_defines
        self.compare_components(kv_defines, kv_define_component_compare)

    def analyze_linear_defines_for_same_components(self, raw_module):
        def linear_define_component_compare(comparer, comparee) -> bool:
            return comparer.value_type.literal == comparee.value_type.literal

        linear_types = raw_module.linear_type_defines
        self.compare_components(linear_types, linear_define_component_compare)

    def analyze_optional_or_result_type_for_same_components(self, raw_module):
        def optional_define_component_compare(comparer, comparee) -> bool:
            return comparer.value_type.literal == comparee.value_type.literal

        def result_define_component_compare(comparer, comparee) -> bool:
            return (
                comparer.value_type.literal == comparee.value_type.literal
                and comparer.get_error_token().literal
                == comparee.get_error_token().literal
            )

        failable_types = raw_module.failable_type_defines
        option_types = [
            define
            for define in failable_types
            if define.get_type().type_symbol == OPTION
        ]
        result_types = [
            define
            for define in failable_types
            if define.get_type().type_symbol == RESULT
        ]

        self.compare_components(option_types, optional_define_component_compare)
        self.compare_components(result_types, result_define_component_compare)

    def function_defines_for_same_components(self, raw_module):
        def function_define_component_compare(comparer, comparee) -> bool:
            arg_literals = [arg.literal for arg in comparer.arg_list]
            other_arg_literals = [arg.literal for arg in comparee.arg_list]
            arg_literals.sort()
            other_arg_literals.sort()
            same = all(a == b for a, b in zip(arg_literals, other_arg_literals))
            if not same:
                return False
            if same and not comparer.value_type and not comparee.value_type:
                return True
            if comparer.value_type.literal == comparee.value_type.literal:
                return True
            return False

        function_types = raw_module.functions
        self.compare_components(function_types, function_define_component_compare)

    def compare_components(self, defined_types, compare_fn):
        for i in range(len(defined_types) - 1):
            comparer = defined_types[i]
            for j in range(i + 1, len(defined_types)):
                comparee = defined_types[j]
                if comparer.get_type().literal != comparee.get_type().literal:
                    continue
                if compare_fn(comparer, comparee):
                    self.add_error(
                        comparer.get_name(),
                        ErrMsg.DEFINE_USES_SAME_COMPONENTS,
                        comparee.get_name(),
                    )

    def check_for_function_type_with_no_args_no_return_type(self, raw_module):
        function_types = raw_module.functions
        for function_define in function_types:
            if (
                len(function_define.arg_list) == 0
                and function_define.value_type is None
            ):
                continue
            self.add_error(
                function_define.get_name(), ErrMsg.FUNCTION_TYPE_HAS_NO_EFFECT
            )

    def check_elements_in_define_are_defined_and_permitted(self, raw_module):
        self.check_kv_elements(raw_module)
        self.check_linear_elements(raw_module)
        self.check_failable_elements(raw_module)
        self.check_function_elements(raw_module)

    def check_kv_elements(self, raw_module):
        kv_defines = raw_module.key_value_defines
        for kv_def in kv_defines:
            self.find_define_element(kv_def.key_token, raw_module)
            self.find_define_element(kv_def.value_token, raw_module)
            self.validate_nested_kv_define_rules(kv_def, raw_module)

    def check_linear_elements(self, raw_module):
        linear_defines = raw_module.linear_type_defines
        for linear_define in linear_defines:
            self.find_define_element(linear_define.value_token, raw_module)
            self.validate_nested_linear_define_rules(linear_define, raw_module)

    def check_failable_elements(self, raw_module):
        failable_defines = raw_module.failable_type_defines
        for failable_define in failable_defines:
            if failable_define.built_in_type_token.type_symbol == symbols.OPTION:
                self.find_define_element(failable_define.value_token, raw_module)
                self.analyze_define_elements_for_option_types(
                    failable_define, raw_module
                )
            elif failable_define.built_in_type_token.type_symbol == symbols.RESULT:
                self.find_define_element(failable_define.value_token, raw_module)
                self.find_define_element(failable_define.error_token, raw_module)
                self.analyze_define_elements_for_result_types(
                    failable_define, raw_module
                )

    def check_function_elements(self, raw_module):
        function_defines = raw_module.function_type_defines
        for function_define in function_defines:
            for arg in function_define.arg_list:
                self.find_define_element(arg, raw_module)
            if function_define.value_type:
                self.find_define_element(function_define.value_type, raw_module)
            self.analyze_define_elements_for_function_types(function_define, raw_module)

    def find_define_element(self, define_element, raw_module):
        all_types_in_module = raw_module.get_module_item_name_tokens()
        all_imported_item_names = raw_module.get_all_imported_item_names()
        found = False
        for mod_item in all_types_in_module:
            if define_element.literal == mod_item.literal:
                found = True
                break
        if found:
            return
        for import_item in all_imported_item_names:
            if define_element.literal == import_item.literal:
                found = True
                break
        if found:
            return
        self.add_error(define_element, ErrMsg.UNDEFINED_ITEM_IN_DEFINE_STMT)

    def validate_nested_kv_define_rules(self, kv_def, raw_module):
        key_err_msg = None
        value_err_msg = None
        match kv_def.built_in_type_token.type_symbol:
            case symbols.MAP:
                key_err_msg = ErrMsg.MAP_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES
                value_err_msg = ErrMsg.MAP_TYPE_VALUE_DEFINE_NESTING_INVALID_DEFINES
            case symbols.HASHMAP:
                key_err_msg = ErrMsg.HASHMAP_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES
                value_err_msg = ErrMsg.HASHMAP_TYPE_DEFINE_NESTING_INVALID_DEFINES
            case symbols.DICTIONARY:
                key_err_msg = ErrMsg.DICT_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES
                value_err_msg = ErrMsg.DICT_TYPE_DEFINE_NESTING_INVALID_DEFINES

        if key_err_msg == None or value_err_msg == None:
            raise Exception("kv types not fidentified")
        # for the values in kv pair:
        self.analyze_define_elements_for_linear_collection_types_default(
            kv_def, ErrMsg.MAP_TYPE_VALUE_DEFINE_NESTING_INVALID_DEFINES, raw_module
        )
        # for keys in kv pair:
        self.analyze_define_elements_for_hash_key_collection_types(
            kv_def, ErrMsg.MAP_TYPE_KEY_DEFINE_NESTING_INVALID_DEFINES, raw_module
        )

    def validate_nested_linear_define_rules(self, linear_define, raw_module):
        value_err_msg = None
        match linear_define.built_in_type_token.type_symbol:
            case symbols.LIST:
                value_err_msg = ErrMsg.LIST_TYPE_DEFINE_NESTING_INVALID_DEFINES
            case symbols.LINKEDLIST:
                value_err_msg = ErrMsg.LINKED_LIST_TYPE_DEFINE_NESTING_INVALID_DEFINES
            case symbols.VECTOR:
                value_err_msg = ErrMsg.VECTOR_TYPE_DEFINE_NESTING_INVALID_DEFINES
            case symbols.QUEUE:
                value_err_msg = ErrMsg.QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
            case symbols.FIFOQUEUE:
                value_err_msg = ErrMsg.FIFO_QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
            case symbols.DEQUE:
                value_err_msg = ErrMsg.DEQUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
            case symbols.PRIORITYQUEUE:
                value_err_msg = (
                    ErrMsg.PRIORITY_QUEUE_TYPE_DEFINE_NESTING_INVALID_DEFINES
                )
            case symbols.STACK:
                value_err_msg = ErrMsg.STACK_TYPE_DEFINE_NESTING_INVALID_DEFINES
        self.analyze_define_elements_for_linear_collection_types_default(
            linear_define, value_err_msg, raw_module
        )

    # def check_failable_elements(self, raw_module):
    #     value_err_msg = None
    #     match linear_define.built_in_type_token.type_symbol:

    def analyze_define_elements_for_linear_collection_types_default(
        self, define_row, error_message, raw_module
    ):
        types_to_check = {
            "acceptable_user_def_types": [
                "StructStatement",
                "UnionStatement",
                "EnumStatement",
                "ErrorStatement",
                "InterfaceStatement",
            ],
            "acceptable_define_stmt_types": [
                symbols.FUN,
                symbols.OPTION,
                symbols.RESULT,
            ],
        }
        self.analyze_define_elements_for_generic_collection_types(
            define_row.value_type,
            raw_module,
            error_message,
            types_to_check,
        )

    def analyze_define_elements_for_hash_key_collection_types(
        self, define_row, error_message, raw_module
    ):
        types_to_check = {
            "acceptable_user_def_types": ["StructStatement", "interface"],
            "acceptable_define_stmt_types": [],
        }
        self.analyze_define_elements_for_generic_collection_types(
            define_row.key_type,
            raw_module,
            error_message,
            types_to_check,
        )

    def analyze_define_elements_for_option_types(self, define_row, raw_module):
        types_to_check = {
            "acceptable_user_def_types": [
                "StructStatement",
                "UnionStatement",
                "EnumStatement",
                "interface",
            ],
            "acceptable_define_stmt_types": [  # everything except options
                symbols.FUN,
                symbols.RESULT,
                symbols.LIST,
                symbols.LINKEDLIST,
                symbols.VECTOR,
                symbols.SET,
                symbols.HASHSET,
                symbols.TREESET,
                symbols.MAP,
                symbols.HASHMAP,
                symbols.DICTIONARY,
                symbols.QUEUE,
                symbols.FIFOQUEUE,
                symbols.DEQUE,
                symbols.PRIORITYQUEUE,
                symbols.STACK,
            ],
        }
        self.analyze_define_elements_for_generic_collection_types(
            define_row.value_type,
            raw_module,
            ErrMsg.OPTION_TYPE_DEFINE_NESTING_INVALID_DEFINES,
            types_to_check,
        )

    def analyze_define_elements_for_result_types(self, define_row, raw_module):
        types_to_check = {
            "acceptable_user_def_types": [
                "StructStatement",
                "UnionStatement",
                "EnumStatement",
                "interface",
            ],
            "acceptable_define_stmt_types": [  # everything except results
                symbols.FUN,
                symbols.OPTION,
                symbols.LIST,
                symbols.LINKEDLIST,
                symbols.VECTOR,
                symbols.SET,
                symbols.HASHSET,
                symbols.TREESET,
                symbols.MAP,
                symbols.HASHMAP,
                symbols.DICTIONARY,
                symbols.QUEUE,
                symbols.FIFOQUEUE,
                symbols.DEQUE,
                symbols.PRIORITYQUEUE,
                symbols.STACK,
            ],
        }
        self.analyze_define_elements_for_generic_collection_types(
            define_row.value_type,
            raw_module,
            ErrMsg.RESULT_TYPE_DEFINE_NESTING_INVALID_DEFINES,
            types_to_check,
        )

        types_to_check = {
            "acceptable_user_def_types": ["error"],
            "acceptable_define_stmt_types": [],
        }
        self.analyze_define_elements_for_generic_collection_types(
            define_row.result_type,
            raw_module,
            ErrMsg.RESULT_TYPE_ERROR_DEFINE_NESTING_INVALID_DEFINES,
            types_to_check,
        )

    def analyze_define_elements_for_function_types(self, define_row, raw_module):
        types_to_check = {
            "acceptable_user_def_types": [
                "StructStatement",
                "UnionStatement",
                "EnumStatement",
                "ErrorStatement",
                "InterfaceStatement",
            ],
            "acceptable_define_stmt_types": [
                symbols.FUN,
                symbols.OPTION,
                symbols.RESULT,
                symbols.LIST,
                symbols.LINKEDLIST,
                symbols.VECTOR,
                symbols.SET,
                symbols.HASHSET,
                symbols.TREESET,
                symbols.MAP,
                symbols.HASHMAP,
                symbols.DICTIONARY,
                symbols.QUEUE,
                symbols.FIFOQUEUE,
                symbols.DEQUE,
                symbols.PRIORITYQUEUE,
                symbols.STACK,
            ],
        }
        for arg in define_row.arg_list:
            self.analyze_define_elements_for_generic_collection_types(
                arg,
                raw_module,
                ErrMsg.FUNCTION_TYPE_ARG_DEFINE_NESTING_INVALID_DEFINES,
                types_to_check,
            )

        # If function has return type
        if define_row.value_type:
            self.analyze_define_elements_for_generic_collection_types(
                define_row.value_type,  # function return type
                raw_module,
                ErrMsg.FUNCTION_TYPE_RETURN_VAL_DEFINE_NESTING_INVALID_DEFINES,
                types_to_check,
            )

    def analyze_define_elements_for_generic_collection_types(
        self, contained_type_token, current_module, error_message, types_to_check
    ):
        if contained_type_token is None:
            raise Exception("INTERNAL ERROR: contained type token is None")
        if is_primitive_type(contained_type_token):
            return
        self.check_type_validity_in_module(
            contained_type_token, current_module, error_message, types_to_check
        )

        # raw_modules = self.collected_modules.get_raw_modules()
        self.check_type_validity_in_imports(
            contained_type_token, current_module, error_message, types_to_check
        )

    def check_type_validity_in_module(
        self, contained_type_token, current_module, error_message, types_to_check
    ):
        all_in_module_items = current_module.get_all_non_import_items()
        for in_module_item in all_in_module_items:
            if in_module_item.get_name().literal != contained_type_token.literal:
                continue
            # replace this with token of language construct, from parser.
            # do it dirty for now:
            # if below in ok lists, the good, else add error
            if (
                str(in_module_item.__class__.__name__)
                in types_to_check["acceptable_user_def_types"]
            ):
                continue
            if str(in_module_item.__class__.__name__) == "DefineStatement":
                if (
                    in_module_item.get_descriptor_token().get_type()
                    in types_to_check["acceptable_define_stmt_types"]
                ):
                    continue
                self.add_error(contained_type_token, error_message)

    def check_type_validity_in_imports(
        self, contained_type_token, current_module, error_message, types_to_check
    ):

        for import_statement in current_module.imports:
            for import_item in import_statement.get_import_list():
                if (
                    import_item.get_visible_item_name().literal
                    == contained_type_token.literal
                ):
                    possible_modules = []
                    for raw_module in self.collected_modules.get_raw_modules():
                        if raw_module == current_module:
                            continue
                        if (
                            raw_module.get_module_name_token().literal
                            == import_statement.get_path_list()[-1].node_token.literal
                        ):
                            possible_modules.append(raw_module)

                    import_path_to_module = import_statement.get_path_list()[0:-1]
                    module_id = -8888
                    path_matcher = ModulePathMatcher(
                        module_id,
                        import_path_to_module,
                        raw_module.directory_path,
                        self.error_manager,
                    )
                    path_matcher.collect_valid_paths()
                    modules_that_match = path_matcher.collect_matching_modules(
                        possible_modules
                    )
                    if len(modules_that_match) > 0:
                        for matching_module in modules_that_match:
                            self.check_type_validity_in_module(
                                contained_type_token,
                                matching_module,
                                error_message,
                                types_to_check,
                            )
