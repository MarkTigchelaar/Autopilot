from SemanticAnalysis.TypeResolvedASTComponents.type_resolved_ast_node import TypeResolvedASTNode
from SemanticAnalysis.TypeResolvedASTComponents.ExternalComponents.function import TypeResolvedFunction


class TypeResolvedStructField(TypeResolvedASTNode):
    def resolve_types(self):
        type_token = self.raw_node.get_type()
        actual_type = self._attempt_type_instance_aqqusition(type_token)
        if actual_type:
            self._set_verified_type_reference(actual_type)
        else:
            self._add_type_error(type_token)


class TypeResolvedInterfaceReference(TypeResolvedASTNode):
    def resolve_types(self):
        interface_token = self.raw_node
        actual_type = self._attempt_type_instance_aqqusition(interface_token)
        if actual_type:
            self._set_verified_type_reference(actual_type)
        else:
            self._add_type_error(interface_token)


class TypeResolvedStruct(TypeResolvedASTNode):
    def __init__(self, raw_node, error_manager, type_resolved_module, parent):
        super().__init__(raw_node, error_manager, type_resolved_module, parent)
        self.resolved_fields = []
        for field in raw_node.get_fields():
            resolved_field = TypeResolvedStructField(
                field,
                error_manager,
                type_resolved_module, 
                self
            )
            self.resolved_fields.append(resolved_field)
        self.resolved_interfaces = []
        for interface in raw_node.get_interfaces():
            resolved_field = TypeResolvedInterfaceReference(
                interface,
                error_manager,
                type_resolved_module, 
                self
            )
            self.resolved_fields.append(resolved_field)
        self.resolved_functions = []
        for function in raw_node.get_functions():
            resolved_field = TypeResolvedFunction(
                function,
                error_manager,
                type_resolved_module, 
                self
            )
            self.resolved_fields.append(resolved_field)


    def resolve_types(self):
        for field in self.resolved_fields:
            field.resolve_types()
        for interface in self.resolved_interfaces:
            interface.resolve_types()
        for function in self.resolved_functions:
            function.resolve_types()