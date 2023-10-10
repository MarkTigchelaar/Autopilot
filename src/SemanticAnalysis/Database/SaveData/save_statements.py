from SemanticAnalysis.Database.SaveData.saver import Saver

class StatementSaver(Saver):
    def __init__(self, object_id):
        self.object_id = object_id
        self.sequence_number = 0

    def save_statements(self, statement_table, statements, scope_level):
        for statement in statements:
            self.sequence_number += 1
            statement_table.insert(statement.get_descriptor_token(), statement, self.object_id, self.sequence_number, scope_level)
            if statement.has_nested_statements():
                self.save_statements(statement_table, statement.get_statements(), scope_level + 1)
            if statement.has_next_statement_in_block():
                self.save_next_statement_in_block(statement_table, statement, scope_level)


    def save_next_statement_in_block(self, statement_table, statement, scope_level):
        self.sequence_number += 1
        statement_table.insert(statement.get_descriptor_token(), statement, self.object_id, self.sequence_number, scope_level)
        if statement.has_nested_statements():
            self.save_statements(statement_table, statement.get_statements(), scope_level + 1)
        if statement.has_next_statement_in_block():
            self.save_next_statement_in_block(statement_table, statement, scope_level)