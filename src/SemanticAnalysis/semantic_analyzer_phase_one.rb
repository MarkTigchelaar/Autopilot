


class SemanticAnalyzerPhaseOne
    def initialize()
        @error_list = Array.new()
    end

    def analyze_node(ast_node)

        case ast_node.class.name
        when "DefineStatement"
            puts "DefineStatement"
        when "EnumStatement"
            puts "EnumStatement"
        when "ErrorStatement"
            puts "ErrorStatement"
        when "PreFixExpression"
            puts "PreFixExpression"
        when "NameExpression"
            puts "NameExpression"
        when "OperatorExpresison"
            puts "OperatorExpresison"
        when "CollectionExpression"
            puts "CollectionExpression"
        when "MethodCallExpression"
            puts "MethodCallExpression"
        when "CallExpression"
            puts "CallExpression"
        when "FunctionArgument"
            puts "FunctionArgument"
        when "FunctionStatement"
            puts "FunctionStatement"
        when "ImportStatement"
            puts "ImportStatement"
        when "InterfaceStatement"
            puts "InterfaceStatement"
        when "ModuleStatement"
            puts "ModuleStatement"
        when "StructField"
            puts "StructField"
        when "StructStatement"
            puts "StructStatement"
        when "UnionItemListType"
            puts "UnionItemListType"
        when "UnionStatement"
            puts "UnionStatement"
        when "UnittestStatement"
            puts "UnittestStatement"
        when "AssignmentStatement"
            puts "AssignmentStatement"
        when "BreakStatement"
            puts "BreakStatement"
        when "ContinueStatement"
            puts "ContinueStatement"
        when "ElifStatement"
            puts "ElifStatement"
        when "ElseStatement"
            puts "ElseStatement"
        when "ForStatement"
            puts "ForStatement"
        when "IfStatement"
            puts "IfStatement"
        when "LoopStatement"
            puts "LoopStatement"
        when "ReassignmentOrCallStatement"
            puts "ReassignmentOrCallStatement"
        when "ReturnStatement"
            puts "ReturnStatement"
        when "StatementList"
            puts "StatementList"
        when "CaseStatement"
            puts "CaseStatement"
        when "SwitchStatement"
            puts "SwitchStatement"
        when "UnlessStatement"
            puts "UnlessStatement"
        when "WhileStatement"
            puts "WhileStatement"
        else
            raise Exception.new("Unknown abstract syntax tree node #{ast_node.class.name}")
        end
    end

    def extend_error_list(parser_error_list)
        parser_error_list.concat(@error_list)
    end
end