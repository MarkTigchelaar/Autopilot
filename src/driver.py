from ASTComponents.make_ast_node_map import make_ast_map

class Driver:
    def __init__(self, tokenizer, err_manager):
        self.err_manager = err_manager
        self.tokenizer = tokenizer
        self.node_func_map = make_ast_map()
        self.modifier_container = None


    def current_file(self):
        return self.tokenizer.current_file()


    def add_error(self, token, err_message):
        self.err_manager.add_parser_error(token, err_message)


    def has_errors(self):
        return self.err_manager.has_errors()


    def discard_token(self):
        self.tokenizer.next_token()

    def get_modifier_container(self):
        if self.modifier_container is None:
            self.modifier_container = ModifierContainer()
        return self.modifier_container

    def delete_modifier_container(self):
        self.modifier_container = None

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
        analysis_fn(AnalyzerShim(self.err_manager), root_node)
        #save_fn(self.analyzer, root_node)

# This is to patch over the semantic analyzer being tossed
# into the local analysis functions. Is setting up for a refactor later
class AnalyzerShim:
    def __init__(self, error_manager):
        self.error_manager = error_manager

    def add_error(self, token, message, shadowed_token=None):
        self.error_manager.add_semantic_error(token, message, shadowed_token)


class ModifierContainer:
    def __init__(self):
        self.public_token = None
        self.inline_token = None
        self.acyclic_token = None

    def add_public_token(self, token):
        self.public_token = token

    def add_inline_token(self,inline_token):
        self.inline_token = inline_token

    def add_acyclic_token(self, token):
        self.acyclic_token = token

    def get_public_token(self):
        return self.public_token

    def get_inline_token(self):
        return self.inline_token

    def get_acyclic_token(self):
        return self.acyclic_token
