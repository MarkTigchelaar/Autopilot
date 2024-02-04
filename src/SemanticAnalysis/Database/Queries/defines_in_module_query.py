from SemanticAnalysis.Database.Queries.query import Query

class DefinesInModuleQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.module_defines = None

    def execute(self, database) -> None:
        define_table = database.get_table("defines")
        define_row = define_table.get_item_by_id(self.object_id)
        # Don't use current module id query here, this object
        # can be in a different module
        current_module_id = define_row.current_module_id
        if define_table.is_module_id_defined(current_module_id):
            self.module_defines = define_table.get_items_by_module_id(current_module_id)
        else:
            self.module_defines = list()

    def has_next(self) -> bool:
        if self.module_defines is None:
            return False
        return self.index < len(self.module_defines)

    def next(self):
        row = self.module_defines[self.index]
        self.index += 1
        return row
