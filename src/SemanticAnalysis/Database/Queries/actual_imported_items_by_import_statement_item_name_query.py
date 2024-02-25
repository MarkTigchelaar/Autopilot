from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.AnalysisComponents.module_path_matcher import ModulePathMatcher
from SemanticAnalysis.AnalysisComponents.analysis_utilities  import split_path_and_file_name

class ActualImportedItemsByImportStatementItemNameQuery(Query):
    def __init__(self, object_id, import_item) -> None:
        super().__init__(object_id)
        self.foreign_module_item_list = None
        self.import_item = import_item

    def execute(self, database) -> None:
        typename_table = database.get_table("typenames")
        import_table = database.get_table("imports")
        module_table = database.get_table("modules")
        type_row = typename_table.get_item_by_id(self.object_id)
        current_module_id = type_row.module_id
        import_statement = import_table.get_row_by_id(self.import_item.import_statement_id)
        foreign_module_name = import_statement.imported_module_name_token
        path = import_statement.path #path to other module, could contain :, meaning multiple moduels could match

        possible_modules = module_table.get_modules_data_for_name(foreign_module_name.literal)
        starting_directory, _ = split_path_and_file_name(self.import_item.name_token.file_name)
        matcher = ModulePathMatcher(current_module_id, path, starting_directory, DummyErrorManager())

        matcher.collect_valid_paths()
        matching_module_ids = matcher.collect_matching_module_ids(possible_modules)
        self.foreign_module_item_list = list()
        for module_id in matching_module_ids:
            matching_items = typename_table.get_items_by_module_id(module_id)
            self.foreign_module_item_list.extend(matching_items)

    def has_next(self) -> bool:
        if self.foreign_module_item_list is None:
            return False
        return self.index < len(self.foreign_module_item_list)

    def next(self):
        row = self.foreign_module_item_list[self.index]
        self.index += 1
        return row


class DummyErrorManager:
    def add_semantic_error(self, _, __):
        pass
