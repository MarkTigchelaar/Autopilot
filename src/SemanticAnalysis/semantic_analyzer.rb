

class SemanticAnalyzer
    def initialize()
        @error_list = Array.new()

        # maybe have some types as fields here, and in other fields?
        # enable triggering of functionality from this main analyzer


        @reference_graph_analyzer = ReferenceGraphAnalyzer.new()
        @function_call_graph_analyzer = CallGraphAnalyzer.new()

        @function_analyzer = FunctionAnalyzer.new(self)
        @struct_analyzer = StructAnalyzer.new(self)
        @define_analyzer = DefineAnalyzer.new(self)
        @enum_analyzer = EnumAnalyzer.new(self)
        @error_analyzer = ErrorAnalyzer.new(self)
        @import_analyzer = ImportAnalyzer.new(self)
        @module_analyzer = ModuleAnalyzer.new(self)
        @union_analyzer = UnionAnalyzer.new(self)
        @union_item_analyzer = UnionItemAnalyzer.new(self)
        @unittest_analyzer = UnittestAnalyzer.new(self)
        @interface_analyzer = InterfaceAnalyzer.new(self)
        
        # Internal statements
        @statement_list_analyzer = StatementListAnalyzer.new(self)
        
        @switch_analyzer = SwitchStatementAnalyzer.new(self)
        @case_statement_analyzer = CaseStatementAnalyzer.new(self)

        @assignment_analyzer = AssignmentAnalyzer.new(self)
        @reassign_or_call_analyzer = ReAssignOrCallAnalyzer.new(self)

        @unless_analyzer = UnlessAnalyzer.new(self)
        @if_analyzer = IfAnalyzer.new(self)
        @elif_analyzer = ElifAnalyzer.new(self)
        @else_analyzer = ElseAnalyzer.new(self)

        @loop_analyzer = LoopAnalyzer.new(self)
        @for_loop_analyzer = ForLoopAnalyzer.new(self)
        @while_loop_analyzer = WhileLoopAnalyzer.new(self)
         
        @continue_analyzer = ContinueAnalyzer.new(self)
        @break_analyzer = BreakAnalyzer.new(self)
        @return_analyzer = ReturnAnalyzer.new(self)

        @struct_field_analyzer = StructFieldAnalyzer.new(self)
        @function_argument_analyzer = FunctionArgumentAnalyzer.new(self)
        @function_call_analyzer = FunctionCallExpAnalyzer.new(self)
        @method_call_analyzer = MethodCallExpAnalyzer.new(self)
        @collection_analyzer = CollectionExpAnalyzer.new(self)
        @operator_analyzer = OperatorExpAnalyzer.new(self)
        @name_analyzer = NameExpAnalyzer.new(self)
        @prefix_analyzer = PrefixExpAnalyzer.new(self)
    end

    def analyze_node(ast_node)
        case ast_node.class.name
        when "ModuleStatement"
            @module_analyzer.analyze_node(ast_node)
        when "DefineStatement"
            @define_analyzer.analyze_node(ast_node)
        when "EnumStatement"
            @enum_analyzer.analyze_node(ast_node)
        when "ErrorStatement"
            @error_analyzer.analyze_node(ast_node)
        when "ImportStatement"
            @import_analyzer.analyze_node(ast_node)
        when "InterfaceStatement"
            @interface_analyzer.analyze_node(ast_node)
        when "UnionStatement"
            @union_analyzer.analyze_node(ast_node)
        when "UnionItemListType"
            @union_item_analyzer.analyze_node(ast_node)
        when "UnittestStatement"
            @unittest_analyzer.analyze_node(ast_node)
        when "StructStatement"
            @struct_analyzer.analyze_node(ast_node)
        when "StructField"
            @struct_field_analyzer.analyze_node(ast_node)
        when "FunctionStatement"
            @function_analyzer.analyze_node(ast_node)
        when "FunctionArgument"
            @function_argument_analyzer.analyze_node(ast_node)
        when "StatementList"
            @statement_list_analyzer.analyze_node(ast_node)
        when "PreFixExpression"
            @prefix_analyzer.analyze_node(ast_node)
        when "NameExpression"
            @name_analyzer.analyze_node(ast_node)
        when "OperatorExpresison"
            @operator_analyzer.analyze_node(ast_node)
        when "CollectionExpression"
            @collection_analyzer.analyze_node(ast_node)
        when "MethodCallExpression"
            @method_call_analyzer.analyze_node(ast_node)
        when "CallExpression"
            @function_call_analyzer.analyze_node(ast_node)
        when "AssignmentStatement"
            @assignment_analyzer.analyze_node(ast_node)
        when "ReassignmentOrCallStatement"
            @reassign_or_call_analyzer.analyze_node(ast_node)
        when "BreakStatement"
            @break_analyzer.analyze_node(ast_node)
        when "ContinueStatement"
            @continue_analyzer.analyze_node(ast_node)
        when "ReturnStatement"
            @return_analyzer.analyze_node(ast_node)
        when "UnlessStatement"
            @unless_analyzer.analyze_node(ast_node)
        when "IfStatement"
            @if_analyzer.analyze_node(ast_node)
        when "ElifStatement"
            @elif_analyzer.analyze_node(ast_node)
        when "ElseStatement"
            @else_analyzer.analyze_node(ast_node)
        when "LoopStatement"
            @loop_analyzer.analyze_node(ast_node)
        when "ForStatement"
            @for_loop_analyzer.analyze_node(ast_node)
        when "WhileStatement"
            @while_loop_analyzer.analyze_node(ast_node)
        when "SwitchStatement"
            @switch_analyzer.analyze_node(ast_node)
        when "CaseStatement"
            @case_statement_analyzer.analyze_node(ast_node)
        else
            raise Exception.new("Unknown abstract syntax tree node #{ast_node.class.name}")
        end
    end

    def add_semantic_error(error)
        @error_list.append(error)
    end
    
    def extend_error_list(parser_error_list)
        parser_error_list.concat(@error_list)
    end
end






# These classes will be moved, but they are just stubs right now

class ReferenceGraphAnalyzer
    def initialize()
        @reference_fields = Hash.new() # type => field type list
    end
end

class CallGraphAnalyzer
    def initialize()
        @function_calls = Hash.new() # function name => call list
    end
end

class StructAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class FunctionAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class ImportAnalyzer

    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class DefineAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class EnumAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class ErrorAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class ModuleAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class UnionAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class UnionItemAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class UnittestAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class InterfaceAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class StatementListAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class SwitchStatementAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class CaseStatementAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class AssignmentAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class ReAssignOrCallAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class UnlessAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class IfAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class ElifAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class ElseAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class LoopAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class ForLoopAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class WhileLoopAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class ContinueAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class BreakAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class ReturnAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class StructFieldAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class FunctionArgumentAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class FunctionCallExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class MethodCallExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class CollectionExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class OperatorExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class NameExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end

class PrefixExpAnalyzer
    def initialize(main_analyzer)
        @main_analyzer = main_analyzer
    end

    def analyze_node(ast_node)
        return
    end
end