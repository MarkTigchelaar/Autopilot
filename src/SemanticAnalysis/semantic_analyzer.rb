require_relative './ExternalStatementAnalyzers/struct_analyzer.rb'
require_relative './ExternalStatementAnalyzers/function_analyzer.rb'
require_relative './ExternalStatementAnalyzers/define_analyzer.rb'
require_relative './ExternalStatementAnalyzers/enum_analyzer.rb'
require_relative './ExternalStatementAnalyzers/error_analyzer.rb'
require_relative './ExternalStatementAnalyzers/import_analyzer.rb'
require_relative './ExternalStatementAnalyzers/module_analyzer.rb'
require_relative './ExternalStatementAnalyzers/union_analyzer.rb'
require_relative './ExternalStatementAnalyzers/unittest_analyzer.rb'
require_relative './ExternalStatementAnalyzers/interface_analyzer.rb'

require_relative './statement_list_analyzer_arg_list.rb'
require_relative './InternalStatementAnalyzers/statement_list_analyzer.rb'
require_relative './InternalStatementAnalyzers/switch_analyzer.rb'
require_relative './InternalStatementAnalyzers/assignment_analyzer.rb'
require_relative './InternalStatementAnalyzers/reassign_or_call_analyzer.rb'
require_relative './InternalStatementAnalyzers/unless_analyzer.rb'
require_relative './InternalStatementAnalyzers/if_analyzer.rb'
require_relative './InternalStatementAnalyzers/elif_analyzer.rb'
require_relative './InternalStatementAnalyzers/else_analyzer.rb'
require_relative './InternalStatementAnalyzers/loop_analyzer.rb'
require_relative './InternalStatementAnalyzers/for_analyzer.rb'
require_relative './InternalStatementAnalyzers/while_analyzer.rb'
require_relative './InternalStatementAnalyzers/continue_analyzer.rb'
require_relative './InternalStatementAnalyzers/break_analyzer.rb'
require_relative './InternalStatementAnalyzers/return_analyzer.rb'

require_relative './ExpressionAnalyzers/function_call_analyzer.rb'
require_relative './ExpressionAnalyzers/method_call_analyzer.rb'
require_relative './ExpressionAnalyzers/collection_analyzer.rb'
require_relative './ExpressionAnalyzers/operator_analyzer.rb'
require_relative './ExpressionAnalyzers/name_analyzer.rb'
require_relative './ExpressionAnalyzers/prefix_analyzer.rb'

require_relative './analysis_utilities.rb'

#remember to not use this if the syntax analyzer has errors already
# semantic errors can still happen before syntax errors, so allow for that.
# ex. a function is Ok, syntax wise, but has semantic error, next function parsed has syntax errors.
class SemanticAnalyzer
    def initialize(test_config = nil)
        @error_list = Array.new()
        @current_module = "_"
        @current_module = test_config.module_name() if test_config

        @function_analyzer = FunctionAnalyzer.new(self)
        @struct_analyzer = StructAnalyzer.new(self)
        @define_analyzer = DefineAnalyzer.new(self)
        @enum_analyzer = EnumAnalyzer.new(self)
        @error_analyzer = ErrorAnalyzer.new(self)
        @import_analyzer = ImportAnalyzer.new(self)
        @module_analyzer = ModuleAnalyzer.new(self)
        @union_analyzer = UnionAnalyzer.new(self)
        @unittest_analyzer = UnittestAnalyzer.new(self)
        @interface_analyzer = InterfaceAnalyzer.new(self)


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

        # expressions
        @function_call_analyzer = FunctionCallExpAnalyzer.new(self)
        @method_call_analyzer = MethodCallExpAnalyzer.new(self)
        @collection_analyzer = CollectionExpAnalyzer.new(self)
        @operator_analyzer = OperatorExpAnalyzer.new(self)
        @name_analyzer = NameExpAnalyzer.new(self)
        @prefix_analyzer = PrefixExpAnalyzer.new(self)
        @expression_type = nil
    end

    def analyze_node_locally(ast_node)
        case ast_node.class.name
        when "ModuleStatement"
            @module_analyzer.analyze_node_locally(ast_node)
        when "DefineStatement"
            @define_analyzer.analyze_node_locally(ast_node)
        when "EnumStatement"
            @enum_analyzer.analyze_node_locally(ast_node)
        when "ErrorStatement"
            @error_analyzer.analyze_node_locally(ast_node)
        when "ImportStatement"
            @import_analyzer.analyze_node_locally(ast_node)
        when "InterfaceStatement"
            @interface_analyzer.analyze_node_locally(ast_node)
        when "UnionStatement"
            @union_analyzer.analyze_node_locally(ast_node)
        when "UnittestStatement"
            @unittest_analyzer.analyze_node_locally(ast_node)
        when "StructStatement"
            @struct_analyzer.analyze_node_locally(ast_node)
        when "FunctionStatement"
            @function_analyzer.analyze_node_locally(ast_node)
        when "StatementList"
            @statement_list_analyzer.analyze_node_locally(ast_node)
        when "PreFixExpression"
            @prefix_analyzer.analyze_node_locally(ast_node)
        when "NameExpression"
            @name_analyzer.analyze_node_locally(ast_node)
        when "OperatorExpresison"
            @operator_analyzer.analyze_node_locally(ast_node)
        when "CollectionExpression"
            @collection_analyzer.analyze_node_locally(ast_node)
        when "MethodCallExpression"
            @method_call_analyzer.analyze_node_locally(ast_node)
        when "CallExpression"
            @function_call_analyzer.analyze_node_locally(ast_node)
        when "AssignmentStatement"
            @assignment_analyzer.analyze_node_locally(ast_node)
        when "ReassignmentOrCallStatement"
            @reassign_or_call_analyzer.analyze_node_locally(ast_node)
        when "BreakStatement"
            @break_analyzer.analyze_node_locally(ast_node)
        when "ContinueStatement"
            @continue_analyzer.analyze_node_locally(ast_node)
        when "ReturnStatement"
            @return_analyzer.analyze_node_locally(ast_node)
        when "UnlessStatement"
            @unless_analyzer.analyze_node_locally(ast_node)
        when "IfStatement"
            @if_analyzer.analyze_node_locally(ast_node)
        when "ElifStatement"
            @elif_analyzer.analyze_node_locally(ast_node)
        when "ElseStatement"
            @else_analyzer.analyze_node_locally(ast_node)
        when "LoopStatement"
            @loop_analyzer.analyze_node_locally(ast_node)
        when "ForStatement"
            @for_loop_analyzer.analyze_node_locally(ast_node)
        when "WhileStatement"
            @while_loop_analyzer.analyze_node_locally(ast_node)
        when "SwitchStatement"
            @switch_analyzer.analyze_node_locally(ast_node)
        when "CaseStatement"
            @case_statement_analyzer.analyze_node_locally(ast_node)
        else
            raise Exception.new("Unknown abstract syntax tree node #{ast_node.class.name}")
        end
    end

    def set_current_module(current)
        @current_module = current
    end

    def add_semantic_error(error)
        @error_list.append(error)
    end
    
    def extend_error_list(parser_error_list)
        parser_error_list.concat(@error_list)
        @error_list = Array.new()
    end

    def reset()
        @error_list = Array.new()
        @current_module = "_"
    end

    def getExpressionTypeToken()
        @expression_type
    end

    def setExpressionTypeToken(typeToken = nil)
        @expression_type = typeToken
    end

    def astSubTreeCompatableWithOperator(operator)
        compatabilityList = getCompatabilityListForOperator(operator)
        for item in compatabilityList
            if item == @expression_type.getType()
                return true
            elsif @expression_type.getType() == IDENTIFIER
                raise Exception.new("non constants are not implemented yet")
            end
        end
    end
end
