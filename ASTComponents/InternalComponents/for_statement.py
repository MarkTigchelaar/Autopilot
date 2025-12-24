from Tokenization.symbols import LET

class ForStatement:
    def __init__(self):
        self.optional_assignment_type = None
        self.unwrapped_optional_variable_name = None
        self.second_unwrapped_optional_variable_name = None
        self.optional_collection_name = None
        self.collection_name = None
        self.index_or_key_name_token = None
        self.map_value_name_token = None
        self.index_start_name = None
        self.index_stop_name = None
        self.iter_size = None
        self.loop_name = None
        self.statements = None
        self.descriptor_token = None

    def add_assignment_type(self, assign_token):
        self.optional_assignment_type = assign_token

    def get_assignment_type(self):
        return self.optional_assignment_type

    def get_variable_name(self):
        return self.unwrapped_optional_variable_name

    def is_optional_type(self):
        return self.optional_assignment_type is not None

    def is_option_type(self):
        return self.is_optional_type()

    def is_let_var_type(self):
        if not self.is_option_type():
            return False
        return self.get_assignment_type().internal_type == LET

    def is_range_iteration(self):
        return self.index_start_name is not None and self.index_stop_name is not None
    
    def is_collection_iteration(self):
        return self.collection_name is not None
    
    def is_key_value_type_iteration(self):
        key_or_regular_item_name = self.get_index_or_key_name()
        map_value_item_name = self.get_map_value_name()
        return None not in (key_or_regular_item_name, map_value_item_name)
    
    def add_variable_name(self, unwrapped_option_token):
        self.unwrapped_optional_variable_name = unwrapped_option_token

    def get_unwrapped_optional_variable_name(self):
        return self.unwrapped_optional_variable_name
    
    def add_second_variable_name(self, unwrapped_option_token):
        self.second_unwrapped_optional_variable_name = unwrapped_option_token
    
    def has_second_optional_variable(self):
        return self.second_unwrapped_optional_variable_name is not None
    
    def get_second_optional_variable(self):
        return self.second_unwrapped_optional_variable_name

    def add_option_collection(self, optional_collection_token):
        self.optional_collection_name = optional_collection_token

    def get_optional_variable_name(self):
        return self.optional_collection_name

    def add_loop_name(self, loop_name_token):
        self.loop_name = loop_name_token

    def get_loop_name(self):
        return self.loop_name

    def add_index_or_key_name(self, index_or_key_name_token):
        self.index_or_key_name_token = index_or_key_name_token

    def get_index_or_key_name(self):
        return self.index_or_key_name_token
    
    def add_map_value_name(self, map_value_name_token):
        self.map_value_name_token = map_value_name_token

    def get_map_value_name(self):
        return self.map_value_name_token

    def add_index_start_name(self, index_start_token):
        self.index_start_name = index_start_token

    def get_index_start_name(self):
        return self.index_start_name

    def add_index_stop_name(self, index_stop_token):
        self.index_stop_name = index_stop_token

    def get_index_stop_name(self):
        return self.index_stop_name

    def add_collection_name(self, collection_token):
        self.collection_name = collection_token

    def get_collection_name(self):
        return self.collection_name

    def add_iteration_step_size(self, iteration_step_token):
        self.iter_size = iteration_step_token

    def get_iteration_step_size(self):
        return self.iter_size

    def add_statements(self, statements):
        self.statements = statements

    def get_statements(self):
        return self.statements

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token
    
    def has_nested_statements(self):
        return True
    
    def has_next_statement_in_block(self):
        return False
    
    def accept(self, visitor, scope_depth):
        visitor.analyze_for_statement(self, scope_depth)

    def accept_typesetter(self, visitor):
        if self.optional_collection_name:
            visitor.set_type_on_variable(self.optional_collection_name)
        if self.collection_name:
            visitor.set_type_on_variable(self.collection_name)
        if self.index_start_name:
            visitor.set_type_on_variable(self.index_start_name)
        if self.index_stop_name:
            visitor.set_type_on_variable(self.index_stop_name)

    
    def accept_resolved_function(self, type_annotater):
        return type_annotater.make_for_statement(self)