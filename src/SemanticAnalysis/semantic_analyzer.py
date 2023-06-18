class SemanticAnalyzer:
    def __init__(self, error_manager):
        self.error_manager = error_manager
        self.local_analyzer = None

    def add_error(self, token, message):
        self.error_manager.add_semantic_error(token, message)

    def save_item_to_data_store(self, ast_node):
        pass

    def begin_local_analysis(self):
        if not self.local_analyzer:
            self.local_analyzer = LocalVariableTracker()

    def finish_local_analysis(self):
        self.local_analyzer = None

    def enter_sub_statement(self, analysis_fn, ast_node):
        self.local_analyzer.increase_scope_depth()
        analysis_fn(self, ast_node)
        self.local_analyzer.decrease_scope_depth()

    def enter_loop_statement(self, analysis_fn, ast_node):
        self.local_analyzer.found_loop(ast_node.loop_name)
        self.enter_sub_statement(analysis_fn, ast_node)
        self.local_analyzer.exiting_loop()

    def is_loop_name_defined(self, loopname_token):
        return self.local_analyzer.is_defined_loop_name(loopname_token.literal)

    def currently_in_loop(self):
        return self.local_analyzer.is_in_loop()
    
    def register_local_variable(self, var_token):
        self.local_analyzer.variable_declare(var_token.literal)

class DeclaredLocalVariable:
    def __init__(self, name, scope_level):
        self.name = name
        self.scope_level = scope_level

class LocalVariableTracker:
    def __init__(self):
        self.loops = [] # names of loop or None for unnamed loops
        self.declared_variables = [] # name + scope level
        self.current_sope_level = 0

    def found_loop(self, name = None):
        self.loops.append(name)
    
    def is_in_loop(self):
        return len(self.loops) > 0

    def exiting_loop(self):
        self.loops.pop()

    def increase_scope_depth(self):
        self.current_sope_level += 1

    def decrease_scope_depth(self):
        # args and struct fields are at level 0.
        self.current_sope_level -= 1
        if self.current_sope_level < 0:
            raise Exception("INTERNAL ERROR: scope level below 0.")
    
        for i in range(len(self.declared_variables)-1, 0, -1):
            if self.declared_variables[i].scope_level > self.current_sope_level:
                self.declared_variables.pop(i)

    def variable_declare(self, name):
        var = DeclaredLocalVariable(name, self.current_sope_level)
        self.declared_variables.append(var)
    
    def is_variable_declared(self, variable_token):
        for var in self.declared_variables:
            if var.name == variable_token.literal:
                return True
        return False
    
    def is_defined_loop_name(self, loop_name):
        for loop in self.loops:
            if loop == loop_name:
                return True
        return False


# Base class
class Item:
    def __init__(self, scope_level, module_name, item):
        self.scope_level = scope_level
        self.module_name = module_name
        self.item = item

    def get_filename(self):
        raise Exception("Not implemented")


class ObjectRow:
    def __init__(self, id, item, next_item):
        self.id = id
        self.item = item
        self.next_item = next_item

    def unpack_into_row(self):
        row = Row()
        row.id = self.id
        row.module = self.item.module_name
        row.filename = self.item.get_filename()
        row.line = self.item.get_line()
        row.column = self.itme.get_column()
        row.literal = self.item.get_literal()
        row.data_type = self.item.get_data_type()
        row.parent_id = self.item.get_parent_id()
        row.scope_level = self.item.get_construct_type()
        row.next_item_id = self.item.get_next_item_id()
        return row



class Row:
    def __init__(self):
        self.id = None
        self.module = None
        self.filename = None
        self.line = None
        self.column = None
        self.literal = None
        self.data_type = None
        self.parent_id = None
        self.scope_level = None
        self.construct_type = None
        self.next_item_id = None


class Table:
    def __init__(self):
        self.rows = list()
    
    def add_row(self, row):
        self.rows.append(row)

class SemanticAnalyzerV2:
    def __init__(self, error_manager):
        self.error_manager = error_manager
        self.id_seq = 0
        self.object_list = list()
        self.denormalized_table = Table()
    
    def add_error(self, token, message):
        self.error_manager.add_semantic_error(token, message)

    # Next item is the next thing at that scope level, or
    # if the current is at the end of scope, then it's the next thing up one level
    def add_item(self, item, next_item):
        self.id_seq += 1
        self.object_list.append(ObjectRow(self.id_seq, item, next_item))

    # After collecting everything, convert 
    # everything into a flat table for analysis
    def denormalize(self):
        for item in self.object_list:
            row = item.unpack_into_row()
            self.denormalized_table.add_row(row)

