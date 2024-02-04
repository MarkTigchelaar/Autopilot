from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.AnalysisComponents.module_path_matcher import ModulePathMatcher
from SemanticAnalysis.AnalysisComponents.analysis_utilities  import split_path_and_file_name

class ImportedItemsByImportStatementItemNameQuery(Query):
    def __init__(self, object_id, item_name_token) -> None:
        super().__init__(object_id)
        self.foreign_module_item_list = None
        self.item_name_token = item_name_token

    def execute(self, database) -> None:
        typename_table = database.get_table("typenames")
        import_table = database.get_table("imports")
        module_table = database.get_table("modules")
        type_row = typename_table.get_item_by_id(self.object_id)
        import_statement = import_table.get_item_by_id(self.object_id)
        path = import_statement.path
        dir_of_import_item, _ = split_path_and_file_name(self.item_name_token.file_name)
        current_module_id = type_row.module_id
        current_module_name = module_table.get_module_by_id(current_module_id).module_name
        module_rows_of_same_name = module_table.get_modules_data_for_name(current_module_name.literal)
        matcher = ModulePathMatcher(current_module_id, path, dir_of_import_item, DummyErrorManager())
        matching_module_ids = matcher.collect_matching_module_ids(module_rows_of_same_name)
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