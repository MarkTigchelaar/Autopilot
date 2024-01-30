from ASTComponents.InternalComponents.for_statement import ForStatement
from TestingComponents.testing_utilities import token_to_json


class TestingForStatement:
    def __init__(self):
        self.for_statement = ForStatement()

    def add_descriptor_token(self, token):
        self.for_statement.add_descriptor_token(token)

    def get_descriptor_token(self):
        return self.for_statement.get_descriptor_token()

    def add_assignment_type(self, assign_token):
        self.for_statement.add_assignment_type(assign_token)

    def add_variable_name(self, unwrapped_option_token):
        self.for_statement.add_variable_name(unwrapped_option_token)

    def add_second_variable_name(self, unwrapped_option_token):
        self.for_statement.add_second_variable_name(unwrapped_option_token)

    def add_option_collection(self, option_collection_var_token):
        self.for_statement.add_option_collection(option_collection_var_token)

    def add_loop_name(self, loop_name_token):
        self.for_statement.add_loop_name(loop_name_token)

    def add_index_or_key_name(self, index_name_token):
        self.for_statement.add_index_or_key_name(index_name_token)

    def add_map_value_name(self, map_value_name_token):
        self.for_statement.add_map_value_name(map_value_name_token)

    def add_index_start_name(self, index_start_token):
        self.for_statement.add_index_start_name(index_start_token)

    def add_index_stop_name(self, index_stop_token):
        self.for_statement.add_index_stop_name(index_stop_token)

    def add_collection_name(self, collection_token):
        self.for_statement.add_collection_name(collection_token)

    def add_iteration_step_size(self, iteration_step_token):
        self.for_statement.add_iteration_step_size(iteration_step_token)

    def add_statements(self, statements):
        self.for_statement.add_statements(statements)

    def print_literal(self, repr_list: list) -> None:
        if self.for_statement.optional_assignment_type:
            repr_list.append(self.for_statement.optional_assignment_type.literal + " ")

        if self.for_statement.unwrapped_optional_variable_name:
            repr_list.append(
                self.for_statement.unwrapped_optional_variable_name.literal + " "
            )

        if self.for_statement.second_unwrapped_optional_variable_name:
            repr_list.append(
                self.for_statement.second_unwrapped_optional_variable_name.literal + " "
            )

        if self.for_statement.optional_collection_name:
            repr_list.append(self.for_statement.optional_collection_name.literal + " ")

        if self.for_statement.index_or_key_name_token:
            repr_list.append(self.for_statement.index_or_key_name_token.literal + " ")

        if self.for_statement.map_value_name_token:
            repr_list.append(self.for_statement.map_value_name_token.literal + " ")

        if self.for_statement.collection_name:
            repr_list.append(self.for_statement.collection_name.literal + " ")

        if self.for_statement.index_start_name:
            repr_list.append(self.for_statement.index_start_name.literal + " ")

        if self.for_statement.index_stop_name:
            repr_list.append(self.for_statement.index_stop_name.literal + " ")

        if self.for_statement.iter_size:
            repr_list.append(self.for_statement.iter_size.literal + " ")

        if self.for_statement.loop_name:
            repr_list.append(self.for_statement.loop_name.literal + " ")


    def print_token_types(self, type_list: list) -> None:
        if self.for_statement.optional_assignment_type:
            type_list.append(
                self.for_statement.optional_assignment_type.type_symbol + " "
            )

        if self.for_statement.unwrapped_optional_variable_name:
            type_list.append(
                self.for_statement.unwrapped_optional_variable_name.type_symbol + " "
            )

        if self.for_statement.second_unwrapped_optional_variable_name:
            type_list.append(
                self.for_statement.second_unwrapped_optional_variable_name.type_symbol
                + " "
            )

        if self.for_statement.optional_collection_name:
            type_list.append(
                self.for_statement.optional_collection_name.type_symbol + " "
            )

        if self.for_statement.collection_name:
            type_list.append(self.for_statement.collection_name.type_symbol + " ")

        if self.for_statement.index_or_key_name_token:
            type_list.append(
                self.for_statement.index_or_key_name_token.type_symbol + " "
            )

        if self.for_statement.map_value_name_token:
            type_list.append(self.for_statement.map_value_name_token.type_symbol + " ")

        if self.for_statement.index_start_name:
            type_list.append(self.for_statement.index_start_name.type_symbol + " ")

        if self.for_statement.index_stop_name:
            type_list.append(self.for_statement.index_stop_name.type_symbol + " ")

        if self.for_statement.iter_size:
            type_list.append(self.for_statement.iter_size.type_symbol + " ")

        if self.for_statement.loop_name:
            type_list.append(self.for_statement.loop_name.type_symbol + " ")

    def to_json(self) -> dict:
        return {
            "type": "for_loop",
            "name": token_to_json(self.for_statement.loop_name),
            "optional_assignment_type": token_to_json(
                self.for_statement.optional_assignment_type
            ),
            "unwrapped_optional": token_to_json(
                self.for_statement.unwrapped_optional_variable_name
            ),
            "second_unwrapped_optional": token_to_json(
                self.for_statement.second_unwrapped_optional_variable_name
            ),
            "optional_collection": token_to_json(
                self.for_statement.optional_collection_name
            ),
            "collection": token_to_json(self.for_statement.collection_name),
            "index_or_key_name": token_to_json(
                self.for_statement.index_or_key_name_token
            ),
            "value_name": token_to_json(self.for_statement.map_value_name_token),
            "range_start": token_to_json(self.for_statement.index_start_name),
            "range_stop": token_to_json(self.for_statement.index_stop_name),
            "range_step": token_to_json(self.for_statement.iter_size),
            "statememts": self.statements_to_json(),
        }

    def statements_to_json(self):
        stmts = list()
        for stmt in self.for_statement.statements:
            stmts.append(stmt.to_json())
        return stmts
