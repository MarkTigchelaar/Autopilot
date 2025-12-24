from abc import ABC, abstractmethod

from ErrorHandling.semantic_error_manager import SemanticErrorManager
from ErrorHandling.semantic_error_messages import TYPE_NOT_DEFINED


class TypeResolvedASTNode(ABC):
    def __init__(
        self,
        raw_node,
        error_manager: SemanticErrorManager,
        type_annontated_module,
        parent,
    ):
        self.raw_node = raw_node
        self.error_manager = error_manager
        self.type_annontated_module = type_annontated_module
        self.parent = parent
        self.verified_type_reference = None

    @abstractmethod
    def resolve_types(self):
        raise NotImplementedError()

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
                self.type_annontated_module.get_primitive_by_item_type_name(name_token)
            )
        return matching_item

    def _get_import_types_by_name_in_current_module(self, name_token):
        matching_items = self.type_annontated_module.get_imported_types_by_name(
            name_token
        )
        if len(matching_items) > 1:
            raise Exception("Duplicate items should be caught before this step")
        elif len(matching_items) == 0:
            return None
        return matching_items[0]

    def _get_non_import_types_by_name_in_current_module(self, name_token):
        matching_items = self.type_annontated_module.get_non_imported_types_by_name(
            name_token
        )
        if len(matching_items) > 1:
            raise Exception("Duplicate items should be caught before this step")
        elif len(matching_items) == 0:
            return None
        return matching_items[0]

    def _set_verified_type_reference(self, verified_type_reference) -> None:
        self.verified_type_reference = verified_type_reference

    def get_verifiable_type(self):
        return self.verified_type_reference
