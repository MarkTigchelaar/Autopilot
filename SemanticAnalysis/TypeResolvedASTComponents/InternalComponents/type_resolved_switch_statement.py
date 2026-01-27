from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import (
    TypeResolvedASTNode,
)
from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import (
    TypeResolvedStatementWithExpression,
)


class TypeResolvedSwitchStatement(TypeResolvedStatementWithExpression):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
        self.resolved_case_statements = [
            TypeResolvedCaseStatement(case, error_manager, module_collection, self)
            for case in raw_node.get_statements()
        ]

    def resolve_types(self):
        super().resolve_types()
        for case_statement in self.resolved_case_statements:
            case_statement.resolve_types()


class TypeResolvedEnumReference(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
    

    def resolve_types(self):
        enum_name_token = self.raw_node.get_enum_name()
        actual_enum_reference = self._attempt_type_instance_aqqusition(enum_name_token)
        if actual_enum_reference:
            self._set_verified_raw_type_reference(actual_enum_reference)
        else:
            self._add_type_error(enum_name_token)



class TypeResolvedCaseValue(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)

    def resolve_types(self):
        value_name_token = self.raw_node.get_value()
        primitive_type_reference = self._attempt_primitive_type_aqquisition(value_name_token)
        if primitive_type_reference:
            self._set_verified_raw_type_reference(primitive_type_reference)
            return
        variable_ref = self.parent.parent._find_local_variable_by_name(value_name_token)
        if variable_ref:
            self.variable_ref = variable_ref
            self._set_verified_raw_type_reference(variable_ref.get_referenced_type())
        else:
            raise Exception("Variable_declaration not found")


class TypeResolvedCaseStatement(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)
        self.enum_references = None
        self.values = None
        self.resolved_sub_statements = [
            statement.accept_resolved_function(parent.parent)
            for statement in self.raw_node.get_statements()
        ]
        if self.raw_node.has_enum_references():
            self.enum_references = [
                TypeResolvedEnumReference(
                    enum, error_manager, module_collection, parent
                )
                for enum in self.raw_node.get_enum_references()
            ]
        if self.raw_node.has_values():
            self.values = [
                TypeResolvedCaseValue(value, error_manager, module_collection, parent)
                for value in self.raw_node.get_values()
            ]

    def resolve_types(self):
        for stmt in self.resolved_sub_statements:
            stmt.resolve_types()
