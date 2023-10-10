


class FunctionStatement:
    def __init__(self):
        self.header = None
        self.statements = None
        self.acyclic_token = None
        self.inline_token = None
        self.pub_token = None

    def add_header(self, header):
        self.header = header
    
    def add_statements(self, statements):
        self.statements = statements
    
    def add_acyclic_token(self, acyclic_token):
        self.acyclic_token = acyclic_token

    def add_inline_token(self, inline_token):
        self.inline_token = inline_token
    
    def add_public_token(self, pub_token):
        self.pub_token = pub_token

"""
,
    {
        "general_component" : "save_function",
        "test_manifest_file" : "../TestFiles/SemanticAnalyzerTests/save_function_tests.json"
    }
"""