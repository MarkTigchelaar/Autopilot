from SemanticAnalysis.Database.Queries.query import Query


class SingleDefineQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.define = None

    def execute(self, database) -> None:
        define_table = database.get_table("defines")
        self.define = define_table.get_item_by_id(self.object_id)

    def has_next(self) -> bool:
        return self.define is not None

    def next(self):
        temp =  self.define
        self.define = None
        return temp
