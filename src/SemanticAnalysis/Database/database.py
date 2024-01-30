from SemanticAnalysis.Database.Tables.typenames import TypeNameTable
from SemanticAnalysis.Database.Tables.modules import ModuleTable
from SemanticAnalysis.Database.Tables.files import FileTable
from SemanticAnalysis.Database.Tables.imports import ImportTable
from SemanticAnalysis.Database.Tables.defines import DefineTable
from SemanticAnalysis.Database.Tables.enumerables import EnumerableTable
from SemanticAnalysis.Database.Tables.modifiers import ModifierTable
from SemanticAnalysis.Database.Tables.functions import FunctionTable
from SemanticAnalysis.Database.Tables.functions import FunctionHeaderTable
from SemanticAnalysis.Database.Tables.interfaces import InterfaceTable
from SemanticAnalysis.Database.Tables.statements import StatementTable
from SemanticAnalysis.Database.Tables.structs import StructTable


class Database:
    def __init__(self, error_manager):
        self.objects = []
        self.error_manager = error_manager
        self.tables = {
            "typenames": TypeNameTable(),
            "modules": ModuleTable(),
            "files": FileTable(),
            "imports": ImportTable(),
            "defines": DefineTable(),
            "enumerables": EnumerableTable(),
            "modifiers": ModifierTable(),
            "functions": FunctionTable(),
            "fn_headers": FunctionHeaderTable(),
            "interfaces": InterfaceTable(),
            "statements": StatementTable(),
            "structs": StructTable(),
        }
        self.current_module_id = None

    def set_current_module_id(self, module_id):
        self.current_module_id = module_id

    def get_current_module_id(self):
        return self.current_module_id

    def get_tablename_for_object(self, object_id):
        for table_name in self.tables:
            table = self.get_table(table_name)
            if table_name in ("typenames"):
                continue
            if table.is_object_defined(object_id):
                return table_name
        raise Exception("INTERNAL ERROR: table name for object id was not found")

    def save_object(self, object_ref):
        self.objects.append(object_ref)
        return len(self.objects) - 1

    def get_object(self, object_id):
        return self.objects[object_id]

    def get_table(self, table_name):
        if table_name not in self.tables:
            raise Exception(
                f'INTERNAL ERROR: database asked for table "{table_name}", but isn\'t present'
            )
        return self.tables[table_name]

    def object_count(self):
        return len(self.objects)
