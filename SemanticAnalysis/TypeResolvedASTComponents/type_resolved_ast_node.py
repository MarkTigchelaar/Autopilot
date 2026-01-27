from abc import ABC, abstractmethod

from ErrorHandling.semantic_error_manager import SemanticErrorManager
from ErrorHandling.semantic_error_messages import TYPE_NOT_DEFINED




class TypeResolvedASTNode(ABC):
    def __init__(
        self,
        raw_node,
        error_manager: SemanticErrorManager,
        type_resolved_module,
        parent,
    ):
        self.raw_node = raw_node
        self.error_manager = error_manager
        self.type_resolved_module = type_resolved_module
        self.parent = parent
        self.verified_raw_type_reference = None
        self.verified_resolved_type_reference  = None
        type_resolved_module.register_raw_type_to_resolved_type(raw_node, self)

    def _find_local_variable_by_name(self, value_name_token):
        return self.parent._find_local_variable_by_name(value_name_token)

    @abstractmethod
    def resolve_types(self):
        raise NotImplementedError()
    
    def resolve_types_in_expressions(self):
        return

    def get_variable_declarations(self):
        return []
    
    @abstractmethod
    def check_type_usage(self):
        raise NotImplementedError()

    def _set_type_resolved_type_reference(self):
        resolved_type = self.type_resolved_module.lookup_resolved_type(self.verified_raw_type_reference)
        self.verified_resolved_type_reference = resolved_type

    def _get_resolved_type_reference(self):
        return self.verified_resolved_type_reference

    def _add_type_error(self, value_type_token):
        self.error_manager.add_error(value_type_token, TYPE_NOT_DEFINED)

    def _attempt_type_instance_aqqusition(self, name_token):
        matching_item = self._get_non_import_types_by_name_in_current_module(
            name_token
        )
        if not matching_item:
            matching_item = self._get_import_types_by_name_in_current_module(
                name_token
            )
        if not matching_item:
            matching_item = (
                self._attempt_primitive_type_aqquisition(name_token)
            )
        return matching_item
    
    def _attempt_primitive_type_aqquisition(self, value_name_token):
        return self.type_resolved_module.get_primitive_by_item_type_name(value_name_token)

    def _get_import_types_by_name_in_current_module(self, name_token):
        matching_items = self.type_resolved_module.get_imported_types_by_name(
            name_token
        )
        if len(matching_items) > 1:
            raise Exception("Duplicate items should be caught before this step")
        elif len(matching_items) == 0:
            return None
        return matching_items[0]

    def _get_non_import_types_by_name_in_current_module(self, name_token):
        matching_items = self.type_resolved_module.get_non_imported_types_by_name(
            name_token
        )
        if len(matching_items) > 1:
            raise Exception("Duplicate items should be caught before this step")
        elif len(matching_items) == 0:
            return None
        return matching_items[0]

    def _set_verified_raw_type_reference(self, verified_raw_type_reference) -> None:
        if isinstance(verified_raw_type_reference, TypeResolvedASTNode):
            raise Exception("This is not meant to be a Resolved type!")
        self.verified_raw_type_reference = verified_raw_type_reference

    def get_verifiable_type(self):
        return self.verified_raw_type_reference


class TypeResolvedDefine(TypeResolvedASTNode):
    def get_key_and_value_refs(self):
        return (self._get_resolved_type_reference(), None)
