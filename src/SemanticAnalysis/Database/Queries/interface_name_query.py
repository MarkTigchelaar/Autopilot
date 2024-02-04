from SemanticAnalysis.Database.Queries.query import Query

class InterfaceNameQuery(Query):
    def __init__(self, object_id) -> None:
        super().__init__(object_id)
        self.name_token = None

    def execute(self, database) -> None:
        interface_table = database.get_table("interfaces")
        self.name_token = interface_table.get_item_by_id(self.object_id)

    def has_next(self) -> bool:
        return self.name_token is not None

    def next(self):
        temp =  self.name_token
        self.name_token = None
        return temp

