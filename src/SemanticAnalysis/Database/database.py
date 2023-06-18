from table import *
from table_makers import make_all_tables

class Database:
    def __init__(self):
        self.tables = make_all_tables()
        self.current_module_id = None
        self.current_sr_file_name = None
        self.object_id_sequence = 0
    
    def next_object_id(self):
        temp = self.object_id_sequence
        self.object_id_sequence += 1
        return temp

    def make_blank_row(self, table_name):
        if table_name not in self.tables:
            raise Exception("INTERNAL ERROR: table name not found")
        return self.tables[table_name].make_blank_row()