from Parsing.ASTComponents.make_ast_node_map import make_ast_map

class Driver:
    # analyzer collects data first pass, saves compiler from 2nd pass
    def __init__(self, tokenizer, err_manager, analyzer):
        self.err_manager = err_manager
        self.tokenizer = tokenizer
        self.node_func_map = make_ast_map()
        self.analyzer = analyzer


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


    # This method enables the SemanticAnalyzer to piggyback off of the parsing code
    # and analyze ast nodes locally as soon as they are parsed;
    # then collect (semantically) unresolved items into a data store
    # (all in a single pass) for global analysis later.
    def analyze_locally(self, analysis_fn, save_fn, root_node):
        if root_node is None:
            return
        analysis_fn(self.analyzer, root_node)
        save_fn(self.analyzer, root_node)
