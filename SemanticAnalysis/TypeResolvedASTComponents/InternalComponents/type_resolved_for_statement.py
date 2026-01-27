from SemanticAnalysis.TypeResolvedASTComponents.InternalComponents.base_types import (
    TypeResolvedBranchingLogic,
    TypeResolvedBranchingDeclaration,
)


class TypeResolvedForStatement(TypeResolvedBranchingLogic):
    def __init__(self, raw_node, error_manager, module_collection, parent):
        super().__init__(raw_node, error_manager, module_collection, parent)

        self.unwrapped_optional_variable_name = None
        self.second_unwrapped_optional_variable_name = None
        self.type_resolved_optional_collection_name = None
        self.type_resolved_collection_name = None
        self.type_resolved_index_or_key_name = None
        self.type_resolved_map_value_name = None
        self.type_resolved_index_start_name = None
        self.type_resolved_index_stop_name = None
        self.type_resolved_iter_size = None
        self.resolved_optional_type_declarations = []

        if self.raw_node.optional_collection_name:
            self.type_resolved_optional_collection_name = (
                self._find_local_variable_by_name(
                    self.raw_node.optional_collection_name
                )
            )
            if self.type_resolved_optional_collection_name:
                key_and_value_tuple = (
                    self.type_resolved_optional_collection_name.get_key_and_value_refs()
                )
                self.unwrapped_optional_variable_name = key_and_value_tuple[0]
                self.second_unwrapped_optional_variable_name = key_and_value_tuple[1]
            else:
                raise Exception("Variable_declaration not found")

        if self.raw_node.collection_name:
            self.type_resolved_collection_name = self._find_local_variable_by_name(
                self.raw_node.collection_name
            )
            if not self.type_resolved_collection_name:
                self.type_resolved_collection_name = (
                    self._attempt_primitive_type_aqquisition(
                        self.raw_node.collection_name
                    )
                )
                if not self.type_resolved_collection_name:
                    raise Exception("Variable_declaration not found")

        if self.raw_node.index_or_key_name_token:
            self.type_resolved_index_or_key_name = self._find_local_variable_by_name(
                self.index_or_key_name_token
            )

            if self.type_resolved_index_or_key_name:
                collection_name = self.type_resolved_optional_collection_name
                if self.type_resolved_collection_name:
                    collection_name = self.type_resolved_collection_name
                value_declaraton = TypeResolvedBranchingDeclaration(
                    self.raw_node.index_or_key_name_token,
                    collection_name,
                    self.unwrapped_optional_variable_name,
                )
                self.resolved_optional_type_declarations.append(value_declaraton)
            else:
                self.type_resolved_index_or_key_name = (
                    self._attempt_primitive_type_aqquisition(
                        self.raw_node.index_or_key_name_token
                    )
                )
                if self.type_resolved_index_or_key_name:
                    return
                raise Exception("Variable_declaration not found")

        if self.raw_node.map_value_name_token:
            self.type_resolved_map_value_name = self._find_local_variable_by_name(
                self.raw_node.map_value_name_token
            )
            if not self.type_resolved_map_value_name:
                self.type_resolved_map_value_name = (
                    self._attempt_primitive_type_aqquisition(
                        self.raw_node.map_value_name_token
                    )
                )
                if not self.type_resolved_map_value_name:
                    raise Exception("Variable_declaration not found")

        if self.raw_node.index_start_name:
            self.type_resolved_index_start_name = self._find_local_variable_by_name(
                self.raw_node.index_start_name
            )
            if not self.type_resolved_index_start_name:
                self.type_resolved_index_start_name = (
                    self._attempt_primitive_type_aqquisition(
                        self.raw_node.index_start_name
                    )
                )
                if not self.type_resolved_index_start_name:
                    raise Exception("Variable_declaration not found")

        if self.raw_node.index_stop_name:
            self.type_resolved_index_stop_name = self._find_local_variable_by_name(
                self.raw_node.index_stop_name
            )
            if not self.type_resolved_index_stop_name:
                self.type_resolved_index_stop_name = (
                    self._attempt_primitive_type_aqquisition(
                        self.raw_node.index_stop_name
                    )
                )
                if not self.type_resolved_index_stop_name:
                    raise Exception("Variable_declaration not found")

        if self.raw_node.iter_size:
            self.type_resolved_iter_size = self._find_local_variable_by_name(
                self.raw_node.iter_size
            )
            if not self.type_resolved_iter_size:
                self.type_resolved_iter_size = self._attempt_primitive_type_aqquisition(
                    self.raw_node.iter_size
                )
                if not self.type_resolved_iter_size:
                    raise Exception("Variable_declaration not found")

    def resolve_types(self):
        super().resolve_types()

    def get_variable_declarations(self):
        return self.resolved_optional_type_declarations
