class MethodCallExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node_locally(ast_node)
        methods_or_fields = ast_node.getMethods()
        for method_or_field in methods_or_fields do
            # revisit this, is likely to explode with different types
            # at least the types will be distinct
            # someone could go struct.field.{a,b,c,d}, that would get past parser!
            # might have to break out the class name stuff for this, very smelly!
            args = method_or_field.getArguments()
            for arg_expression in args do
                @main_analyzer.analyze_node_locally(arg_expression)
            end
        end
    end
end
