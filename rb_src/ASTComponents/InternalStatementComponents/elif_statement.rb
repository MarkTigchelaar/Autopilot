
class ElifStatement
    def initialize(if_statement)
        @if_statement = if_statement
    end

    def visit(semantic_analyzer)
        semantic_analyzer.analyze_node_locally(self)
    end

    def get_unwrapped_var()
        @if_statement.get_unwrapped_var()
    end

    def get_option()
        @if_statement.get_option()
    end

    def get_ast()
        @if_statement.get_ast()
    end

    def get_statements()
        @if_statement.get_statements()
    end

    def toJSON()
        json = @if_statement.toJSON()
        json["type"] = "elif"
        return json
    end

    def _printLiteral
        if(@if_statement != nil)
            return @if_statement._printLiteral()
        end
        return ""
    end

    def _printTokType(type_list)
        if(@if_statement != nil)
            @if_statement._printTokType(type_list)
        end
    end
end
