from SemanticAnalysis.Database.table import Table
from SemanticAnalysis.Database.table_makers import make_all_tables

class Database:
    def __init__(self):
        self.tables = make_all_tables()
        self.object_id_sequence = 0
    

    def upload(self, ast_node_saver):
        pass # saver class knows the exact insert query for all tables needed for that type
        

    def process_queries(self, analyzer):
        pass # begin analysis

    def next_object_id(self):
        temp = self.object_id_sequence
        self.object_id_sequence += 1
        return temp

    def make_blank_row(self, table_name):
        if table_name not in self.tables:
            raise Exception("INTERNAL ERROR: table name not found")
        return self.tables[table_name].make_blank_row()
    
