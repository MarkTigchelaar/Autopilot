from SemanticAnalysis.Database.SaveData.saver import Saver


class StatementSaver(Saver):
    def __init__(self, object_id):
        self.object_id = object_id
        self.sequence_number = 0

    def save_statements(self, statement_table, statements, scope_level = 0):
        for statement in statements:
            self.sequence_number += 1
            descriptor = statement.get_descriptor_token()
            if descriptor is None:
                raise Exception(
                    f"INTERNAL ERROR: descriptor token is None in instance of {type(statement)}"
                )
            statement_table.insert(
                descriptor, statement, self.object_id, self.sequence_number, scope_level
            )
            if statement.has_nested_statements():
                self.save_statements(
                    statement_table, statement.get_statements(), scope_level + 1
                )
            if statement.has_next_statement_in_block():
                self.save_next_statement_in_block(
                    statement_table, statement.next_statement_in_block, scope_level
                )

    def save_next_statement_in_block(self, statement_table, statement, scope_level):
        self.sequence_number += 1
        descriptor = statement.get_descriptor_token()
        if descriptor is None:
            raise Exception(
                f"INTERNAL ERROR: descriptor token is None in instance of {type(statement)}"
            )
        statement_table.insert(
            descriptor, statement, self.object_id, self.sequence_number, scope_level
        )
        if statement.has_nested_statements():
            self.save_statements(
                statement_table, statement.get_statements(), scope_level + 1
            )
        if statement.has_next_statement_in_block():
            self.save_next_statement_in_block(
                statement_table, statement.next_statement_in_block, scope_level
            )
