class UnittestAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        add_test_name_extern_argument()
        statements = ast_node.getStatements()
        @main_analyzer.analyze_node_locally(statements)
    end

    def add_test_name_extern_argument()
        name_tok = ast_node.getName()
        msg = "Name collision, identifier name matches unit test name"
        @main_analyzer.add_statement_external_identifier(msg, name_tok, "test_name")
    end
end
