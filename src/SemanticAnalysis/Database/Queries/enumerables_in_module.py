from SemanticAnalysis.Database.Queries.query import Query
from SemanticAnalysis.Database.Queries.current_module_id_query import CurrentModuleIdQueryQuery

class EnumerablesInModuleQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.enumerables = None

    def execute(self, database) -> None:
        typename_table = database.get_table("typenames")
        enumerable_table = database.get_table("enumerables")
        current_module_id = database.execute_query(CurrentModuleIdQueryQuery(self.object_id)).next()
        self.enumerables = list()
        for typename in typename_table.get_items_by_module_id(current_module_id):
            if not enumerable_table.is_object_defined(typename.object_id):
                continue
            if typename.category in ("union", "enum", "error"):
                enumerable = enumerable_table.get_item_by_id(typename.object_id)
                union_proxy = EnumerableContainer(typename.name_token, typename.category, enumerable.item_list)
                self.enumerables.append(union_proxy)



    def has_next(self) -> bool:
        if self.enumerables is None:
            return False
        return self.index < len(self.enumerables)

    def next(self):
        row = self.enumerables[self.index]
        self.index += 1
        return row


class EnumerableContainer:
    def __init__(self, name_token, category, item_list) -> None:
        self.name_token = name_token
        self.category = category
        self.fields = item_list
