from keywords import is_primitive_type
import ErrorHandling.semantic_error_messages as ErrMsg


class DefineStatementDependencyChecker:
    def __init__(
        self, undefined_items, structs, unions, enums, errors, defines, error_manager
    ):
        self.undefined_items = undefined_items
        self.structs = structs
        self.unions = unions
        self.enums = enums
        self.errors = errors
        self.defines = defines
        self.error_manager = error_manager

        self.visited = set()
        self.defined_type = None

    def check_dag(self, define_row):
        self.defined_type = define_row.new_type_name_token
        self.visited.add(define_row.new_type_name_token.literal)
        self.visit_define(define_row)

    def find_type(self, type):
        for undefined_item in self.undefined_items:
            if type.literal == undefined_item.literal:
                return
        for struct_row in self.structs:
            if type.literal == struct_row.name_token.literal:
                self.visit_item_with_fields(struct_row)
                return

        for union_row in self.unions:
            if type.literal == union_row.name_token.literal:
                self.visit_item_with_fields(union_row)
                return

        for enum_row in self.enums:
            if type.literal == enum_row.name_token.literal:
                return

        for error_row in self.errors:
            if type.literal == error_row.name_token.literal:
                return

        for define_row in self.defines:
            if type.literal == define_row.new_type_name_token.literal:
                self.visit_define(define_row)
                return

    def visit_item_with_fields(self, struct_row):
        for field in struct_row.fields:
            if is_primitive_type(field.type_token):
                continue
            if field.type_token.literal in self.visited:
                if field.type_token.literal == self.defined_type.literal:
                    self.error_manager.add_semantic_error(
                        self.defined_type,
                        ErrMsg.CYCLE_IN_DEFINE_DEPENDANCIES,
                        field.type_token,
                    )
            else:
                self.visited.add(field.type_token.literal)
                self.find_type(field.type_token)

    def visit_define(self, define_row):
        key_type = define_row.key_type
        value_type = define_row.value_type
        arg_list = define_row.arg_list
        result_type = define_row.result_type

        if key_type and not is_primitive_type(key_type):
            self.find_type(key_type)

        if value_type and not is_primitive_type(value_type):
            self.find_type(value_type)

        if result_type and not is_primitive_type(result_type):
            self.find_type(result_type)

        if arg_list is None:
            return
        for arg in arg_list:
            if arg and not is_primitive_type(arg):
                self.find_type(arg)
