from Parsing.ASTComponents.make_ast_node_map import make_ast_map

class ParsingDriver:
    def __init__(self, tokenizer, err_manager):
        self.err_manager = err_manager
        self.tokenizer = tokenizer
        self.node_func_map = make_ast_map()

    def current_file(self):
        return self.tokenizer.current_file()

    def add_error(self, token, err_message):
        self.err_manager.add_parser_error(token, err_message)

    def has_errors(self):
        return self.err_manager.has_errors()

    def discard_token(self):
        self.tokenizer.next_token()

    def next_token(self):
        return self.tokenizer.next_token()

    def peek_token(self):
        return self.tokenizer.peek_next_token()

    def make_node(self, node_key):
        if node_key not in self.node_func_map:
            raise Exception("INTERNAL ERROR: node key " + str(node_key) + "not found")
        return self.node_func_map[node_key]()
