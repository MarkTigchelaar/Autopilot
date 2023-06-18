


class BreakStatement:
    def __init__(self):
        self.label_name_token = None
        self.descriptor_token = None

    def add_label_name(self, label_name):
        self.label_name_token = label_name

    def add_descriptor_token(self, token):
        self.descriptor_token = token

    def get_descriptor_token(self):
        return self.descriptor_token
    
    def has_nested_statements(self):
        return False