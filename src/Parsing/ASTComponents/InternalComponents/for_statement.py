
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
    
    def add_variable_name(self, unwrapped_option_token):
        self.unwrapped_optional_variable_name = unwrapped_option_token
    
    def add_second_variable_name(self, unwrapped_option_token):
        self.second_unwrapped_optional_variable_name = unwrapped_option_token
    
    def add_option_collection(self, optional_collection_token):
        self.optional_collection_name = optional_collection_token

    def add_loop_name(self, loop_name_token):
        self.loop_name = loop_name_token

    def add_index_or_key_name(self, index_or_key_name_token):
        self.index_or_key_name_token = index_or_key_name_token
    
    def add_map_value_name(self, map_value_name_token):
        self.map_value_name_token = map_value_name_token

    def add_index_start_name(self, index_start_token):
        self.index_start_name = index_start_token

    def add_index_stop_name(self, index_stop_token):
        self.index_stop_name = index_stop_token

    def add_collection_name(self, collection_token):
        self.collection_name = collection_token

    def add_iteration_step_size(self, iteration_step_token):
        self.iter_size = iteration_step_token

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