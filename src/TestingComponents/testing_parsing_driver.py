from ErrorHandling.parsing_error_messages import EMPTY_STATEMENT
from TestingComponents.TestingASTComponents.make_test_ast_node_map import make_test_ast_map
from driver import Driver
from TestingComponents.dummy_semantic_driver import DummySemanticDriver

class TestingParsingDriver(Driver):
    def __init__(self, tokenizer, err_manager, allow_empty_stmts = False):
        super().__init__(tokenizer, err_manager, DummySemanticDriver())
        self.node_func_map = make_test_ast_map()
        self.allow_empty_stmts = allow_empty_stmts

    def add_error(self, token, err_message):
        if err_message == EMPTY_STATEMENT and self.allow_empty_stmts:
            return
        self.err_manager.add_parser_error(token, err_message)

    # No semantic analysis for you!
    def analyze_locally(self, analysis_fn, save_fn, node):
        return
