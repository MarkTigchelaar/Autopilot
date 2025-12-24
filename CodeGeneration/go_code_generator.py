from typing import List, Any

from ASTComponents.AggregatedComponents.modules import RawModule
from ASTComponents.ExternalComponents.function_statement import FunctionStatement
from ASTComponents.ExternalComponents.function_header_statement import FunctionHeaderStatement

from ASTComponents.InternalComponents.assign_statement import AssignmentStatement
from ASTComponents.InternalComponents.return_statement import ReturnStatement
from ASTComponents.InternalComponents.if_statement import IfStatement
from ASTComponents.InternalComponents.elif_statement import ElifStatement
from ASTComponents.InternalComponents.else_statement import ElseStatement
from ASTComponents.InternalComponents.unless_statement import UnlessStatement
from ASTComponents.InternalComponents.switch_statement import SwitchStatement
from ASTComponents.InternalComponents.loop_statement import LoopStatement
from ASTComponents.InternalComponents.while_statement import WhileStatement
from ASTComponents.InternalComponents.for_statement import ForStatement
from ASTComponents.InternalComponents.break_statement import BreakStatement
from ASTComponents.InternalComponents.continue_statement import ContinueStatement
from ASTComponents.InternalComponents.defer_statement import DeferStatement
from ASTComponents.InternalComponents.re_assign_or_method_call import ReassignmentOrMethodCall
from CodeGeneration.code_generator import CodeGenerator

class GoCodeGenerator(CodeGenerator):

    def generate_code(self):
        print("Here in go code generator")
        self._generate_package()
        self._generate_errors()
        self._generate_enums()
        self._generate_type_defintions()
        self._generate_structs()
        self._generate_functions()
        self._generate_unittests()

    def trigger_output(self):
        # run go compiler, or just print out to file (BytesIO, or actual file)
        with open("result.go", "w") as go_program:
            go_program.write("\n".join(self.output_code_lines))

    
        
    def _generate_package(self):
        self.begin_line()
        self.add_to_current_line("package main\n")
        self.complete_line()

    def _generate_errors(self):
        pass

    def _generate_enums(self):
        pass

    def _generate_type_defintions(self):
        pass
    def _generate_structs(self):
        pass

    def _generate_unittests(self):
        pass



    def _generate_functions(self):
        for raw_module in self.raw_modules:
            if raw_module.name == "main":
                self._place_main_function_first(raw_module)
            
            self._generate_functions_in_module(raw_module)
    
    def _place_main_function_first(self, raw_module: RawModule):
        main_function_index = None
        for i in range(len(raw_module.functions)):
            function = raw_module.functions[i]
            if function.get_name().literal == "main":
                if i == 0:
                    return
                main_function_index = i
                break
        if main_function_index is None:
            raise Exception("main function not found")
        main_function = raw_module.functions.pop(main_function_index)
        raw_module.functions.insert(0, main_function)


    def _generate_functions_in_module(self, raw_module: RawModule):
        module_name = raw_module.get_module_name_token().literal
        for function in raw_module.functions:
            self._write_function_header(function, module_name)
            self._write_function_body(function)
            self.add_to_current_line("\n")
            self.complete_line()

    
    def _write_function_header(self, function: FunctionStatement, module_name: str):
        header: FunctionHeaderStatement = function.get_header()
        self.add_to_current_line_w_space("func")
        prefix = ''
        if module_name != "main":
            prefix = module_name + '_'
        self.add_to_current_line(prefix + header.get_name().literal)
        self.add_to_current_line("(")
        arguments = header.get_args()
        for i in range(len(arguments)):
            argument = arguments[i]
            self.add_to_current_line_w_space(argument.get_name().literal)
            self.add_to_current_line(argument.get_type().literal)
            if i >= len(arguments) - 1:
                break
            self.add_to_current_line_w_space(",")
        self.add_to_current_line_w_space(")")
        return_type = header.get_return_type()
        if return_type:
            self.add_to_current_line_w_space(return_type.literal)
        


    def _write_function_body(self, function: FunctionStatement):
        self.add_to_current_line("{")
        self.complete_line()
        self._write_statements(function.get_statements())
        self.add_to_current_line("}")

    def _write_statements(self, statements: List[Any]):
        self.increase_indent_level()
        
        for statement in statements:
            match str(statement.__class__.__name__):
                case "AssignmentStatement":
                    #print("assign statement")
                    self._write_assignment_statement(statement)
                case "ReturnStatement":
                    self._write_return_statement(statement)
                case "IfStatement":
                    self._write_if_statement(statement)
                case "UnlessStatement":
                    self._write_unless_statement(statement)
                case "SwitchStatement":
                    self._write_switch_statement(statement)
                case "LoopStatement":
                    self._write_loop_statement(statement)
                case "WhileStatement":
                    self._write_while_statement(statement)
                case "ForStatement":
                    self._write_for_statement(statement)
                case "BreakStatement":
                    self._write_break_statement(statement)
                case "ContinueStatement":
                    self._write_continue_statement(statement)
                case "DeferStatement":
                    self._write_defer_statement(statement)
                case "ReassignmentOrMethodCall":
                    self._write_re_assignment_or_method_call(statement)
                case _:
                    print(f"{str(statement.__class__.__name__)} not implemented")
        self.decrease_indent_level()
    


        
    def _write_assignment_statement(self, statement: AssignmentStatement):
        self.begin_line()
        self.add_to_current_line_w_space("var")
        self.add_to_current_line_w_space(statement.get_name().literal)
        type_token = statement.get_type()
        if type_token:
            self.add_to_current_line_w_space(type_token.literal)
            self.add_to_current_line_w_space("=")
        else:
            self.add_to_current_line_w_space(":=")
        self._write_expression(statement.get_expression_ast())
        self.complete_line()


    def _write_return_statement(self, statement: ReturnStatement):
        self.begin_line()
        self.add_to_current_line_w_space("return")
        if statement.has_expression_ast():
            self._write_expression(statement.get_expression_ast())
        self.complete_line()

    def _write_if_statement(self, statement: IfStatement | ElifStatement, is_elif = False):
        test_expression = statement.get_expression_ast()
        sub_statements = statement.get_statements()
        
        if is_elif:
            self.add_to_current_line(" else ")
        else:
            self.begin_line()
        self.add_to_current_line("if(")
        self._write_expression(test_expression)
        self.add_to_current_line(") {")
        self.complete_line()
        self._write_statements(sub_statements)
        self.begin_line()
        self.add_to_current_line("}")
        if statement.has_next_statement_in_block():
            chained_statement = statement.get_next_statement_in_block()
            match str(chained_statement.__class__.__name__):
                case "ElifStatement":
                    self._write_if_statement(chained_statement, True)
                case "ElseStatement":
                    self._write_else_statement(chained_statement)
                case _:
                    raise Exception("Unknown statement")
        else:
            self.complete_line()

    def _write_else_statement(self, statement: ElseStatement):
        sub_statements = statement.get_statements()
        #self.begin_line(False)
        self.add_to_current_line(" else {")
        self.complete_line()
        self._write_statements(sub_statements)
        self.begin_line()
        self.add_to_current_line("}")
        self.complete_line()

    def _write_unless_statement(self, statement: UnlessStatement):
        test_expression = statement.get_expression_ast()
        sub_statements = statement.get_statements()
        self.begin_line()
        self.add_to_current_line("if(!(")
        self._write_expression(test_expression)
        self.add_to_current_line(")) {")
        self.complete_line()
        self._write_statements(sub_statements)
        self.begin_line()
        self.add_to_current_line("}")
        self.complete_line()

    def _write_switch_statement(self, statement: SwitchStatement):
        self.begin_line()
        self.add_to_current_line("switch ")
        test_exp = statement.get_test_expression()
        self._write_expression(test_exp)
        self.add_to_current_line(" {")
        self.complete_line()
        for case_stmt in statement.get_non_default_statements():
            self.begin_line()
            self.add_to_current_line("case ")
            for i, case_value in enumerate(case_stmt.get_values()):
                if case_value.minus_sign:
                    self.add_to_current_line_w_space(case_value.minus_sign.literal)
                self.add_to_current_line(case_value.value.literal)
                if i < len(case_stmt.get_values()) -1:
                    self.add_to_current_line(",")
            self.add_to_current_line(":")
            self.complete_line()
            self._write_statements(case_stmt.get_statements())
        if statement.has_default_case():
            default_case = statement.get_default_statemnt()
            self.begin_line()
            self.add_to_current_line("default:")
            self.complete_line()
            self._write_statements(default_case.get_statements())
        self.begin_line()
        self.add_to_current_line("}")
        self.complete_line()


    
    def _write_loop_statement(self, statement: LoopStatement):
        self.begin_line()
        self.add_to_current_line("for {")
        self.complete_line()
        self._write_statements(statement.get_statements())
        self.begin_line()
        self.add_to_current_line("}")
        self.complete_line()

    def _write_while_statement(self, statement: WhileStatement):
        self.begin_line()
        self.add_to_current_line("for (")
        self._write_expression(statement.get_expression_ast())
        self.add_to_current_line(") {")
        self.complete_line()
        self._write_statements(statement.get_statements())
        self.begin_line()
        self.add_to_current_line("}")
        self.complete_line()

    def _write_for_statement(self, statement: ForStatement):
        # range type
        # key value pair type
        # regular collection type
        # optional collection type, both types
        if statement.is_collection_iteration():
            self._write_collection_for_statement(statement)
        elif statement.is_range_iteration():
            self._write_range_for_statement(statement)
        else:
            raise Exception("Still not implemented")
    
    def _write_collection_for_statement(self, statement: ForStatement):
        if statement.is_optional_type():
            raise Exception("Optional types are not implemented")
        self.begin_line()
        self.add_to_current_line_w_space("for")
        key_or_regular_item_name = statement.get_index_or_key_name()
        if statement.is_key_value_type_iteration():
            map_value_item_name = statement.get_map_value_name()
            self.add_to_current_line(key_or_regular_item_name.literal)
            self.add_to_current_line_w_space(",")
            self.add_to_current_line(map_value_item_name.literal)
        else:
            self.add_to_current_line_w_space("_,")
            self.add_to_current_line_w_space(key_or_regular_item_name.literal)

        self.add_to_current_line_w_space(":= range")
        collection_name = statement.get_collection_name()
        self.add_to_current_line_w_space(collection_name.literal)
        self.add_to_current_line("{")
        self.complete_line()
        self._write_statements(statement.get_statements())
        self.begin_line()
        self.add_to_current_line("}")
        self.complete_line()


    def _write_range_for_statement(self, statement: ForStatement):
        start = statement.get_index_start_name()
        stop = statement.get_index_stop_name()
        step = statement.get_iteration_step_size()
        index_variable = statement.get_index_or_key_name()
        self.begin_line()
        loop_header = f"for {index_variable.literal} := {start.literal}; {index_variable.literal} < {stop.literal}; {index_variable.literal} += {step.literal}"
        self.add_to_current_line_w_space(loop_header)
        self.add_to_current_line("{")
        self.complete_line()
        self._write_statements(statement.get_statements())
        self.begin_line()
        self.add_to_current_line("}")
        self.complete_line()




    def _write_break_statement(self, statement: BreakStatement):
        self.begin_line()
        self.add_to_current_line("break")
        self.complete_line()

    def _write_continue_statement(self, statement: ContinueStatement):
        self.begin_line()
        self.add_to_current_line("continue")
        self.complete_line()

    def _write_defer_statement(self, statement: DeferStatement):
        self.begin_line()
        self.add_to_current_line("defer ")
        deferred_statement = statement.get_method_or_reassignment()
        l_value_exp = deferred_statement.get_l_value()
        self._write_expression(l_value_exp)
        self.complete_line()

    def _write_re_assignment_or_method_call(self, statement: ReassignmentOrMethodCall):
        self.begin_line()
        is_re_assignment = statement.get_assignment_token() is not None
        if is_re_assignment:
            print("Not implemented")
            return
        self._write_expression(statement.get_l_value())
        self.complete_line()

    def _write_expression(self, expression: Any, add_parens = True):
        match str(expression.__class__.__name__):
            case "NameExpression":
                self.add_to_current_line(expression.get_name().literal)
            case "OperatorExpression":
                if add_parens:
                    self.add_to_current_line("(")
                self._write_expression(expression.get_lhs_exp())
                self.add_to_current_line(expression.get_name().literal)
                self._write_expression(expression.get_rhs_exp())
                if add_parens:
                    self.add_to_current_line(")")
            case "FunctionCallExpression":
                self.add_to_current_line(expression.get_name().get_name().literal)
                self.add_to_current_line("(")
                arguments = expression.get_argument_list()
                for i, arg_expression in enumerate(arguments):
                    self._write_expression(arg_expression)
                    if i >= len(arguments) - 1:
                        continue
                    self.add_to_current_line_w_space(",")
                self.add_to_current_line(")")
            case "MethodCallOrFieldExpression":
                self.add_to_current_line(expression.struct_name_exp.token.literal)
                self.add_to_current_line(".")
                for i, fn_exp in enumerate(expression.get_field_or_methods()):
                    self._write_expression(fn_exp)
                    if i < len(expression.get_field_or_methods()) - 1:
                        self.add_to_current_line(".")
            case "CollectionExpression":
                self._write_collection_expression(expression)
            # case "CollectionAccessExpression":
            case _:
                print(f"{str(expression.__class__.__name__)} not implemented")


    def _write_collection_expression(self, expression: Any):
        sub_expressions = expression.get_collection_elements()
        if expression.is_hash_type():
            key_type = expression.get_type() or "UNKNOWN"
            value_type = expression.get_value_type() or "UNKNOWN"
            #self.begin_line()
            self.add_to_current_line_w_space(f"map[{key_type}]{value_type}")
            self.add_to_current_line("{")
            self.complete_line()
        self.increase_indent_level()
        for i, sub_exp in enumerate(sub_expressions):
            self.begin_line()
            self._write_expression(sub_exp, False)
            if i < len(sub_expressions) - 1:
                self.add_to_current_line(",")
            self.complete_line()
        self.decrease_indent_level()
        self.begin_line()
        self.add_to_current_line("}")
        self.complete_line()
        
