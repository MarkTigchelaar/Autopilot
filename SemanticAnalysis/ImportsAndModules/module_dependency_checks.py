from typing import List
from ASTComponents.AggregatedComponents.modules import RawModule, RawModuleCollection
from ErrorHandling.module_dependency_error_manager import (
    ModuleDependencyCycleErrorManager,
)
from ErrorHandling.module_semantic_error_messages import (
    MODULE_DEPENDENCY_CYCLE_DETECTED,
)


class StackItem:
    def __init__(self, node_index, module_name, dependency_index):
        self.node_index = node_index
        self.module_name = module_name
        self.dependency_index = dependency_index


class CycleStackTrace:
    def __init__(self):
        self.stack = []

    def push(self, node_index, module_name, dependency_index):
        self.stack.append(StackItem(node_index, module_name, dependency_index))

    def pop(self):
        return self.stack.pop()

    def get_stack_trace(self):
        return self.stack


# This class assumes that a module name can possibly refer to exactly one module.
# The problem of importing different modules with the same name is already dealt with,
# and halts compilation before reaching this code path.
class ModuleDependencyChecker:
    def __init__(
        self,
        module_dependency_cycle_error_manager: ModuleDependencyCycleErrorManager,
        raw_module_collection: RawModuleCollection,
    ) -> None:
        self.error_manager = module_dependency_cycle_error_manager
        self.raw_module_collection = raw_module_collection
        self.modules: List[RawModule] = self.raw_module_collection.get_raw_modules()
        self.node_graph = dict()
        self.cycle_found = False
        self.indicies_of_nodes_visited = set()

    def get_dependency_graph(self) -> dict:
        return self.node_graph

    def dependency_graph_has_cycles(self) -> bool:
        return self.cycle_found
    
    def get_error_manager(self) -> ModuleDependencyCycleErrorManager:
        return self.error_manager

    def build_dependency_graph(self) -> None:
        # does not detect cycles here
        main_index = None
        main_module = None
        for i, raw_module in enumerate(self.modules):
            if raw_module.name == "main":
                main_index = i
                main_module = raw_module
                break
        indicies_of_dependencies = self.find_dependency_indicies(main_index)
        main_node = self.make_graph_node(
            main_module.name,
            indicies_of_dependencies,
            main_module.directory_path,
            main_index,
        )
        if main_node is None:
            raise Exception("main node cannot be None")
        self.add_to_node_graph(main_node)

        self.visit_dependency_nodes(main_node)
        self.indicies_of_nodes_visited = set()

    # Nodes are connected here
    # Cycles are seen in the graph at this point, but are not reported
    def find_dependency_indicies(self, module_index):
        indicies_of_dependencies = []
        dependant_module = self.modules[module_index]
        for i, raw_module in enumerate(self.modules):
            if raw_module in dependant_module.dependencies:
                indicies_of_dependencies.append(i)
        return indicies_of_dependencies

    def make_graph_node(
        self, module_name, dependency_index_list, abs_location, node_index
    ):
        # Seen module is listed in dependencies of existing node,
        # so a cycle is already recorded, no problem here.
        if node_index in self.indicies_of_nodes_visited:
            return None
        self.indicies_of_nodes_visited.add(node_index)
        return {
            "name": module_name,
            "location_path": abs_location,
            "dependency_indicies": dependency_index_list,
            "node_index": node_index,
        }

    def visit_dependency_nodes(self, dependant_node):
        for index in dependant_node["dependency_indicies"]:
            dependency_module = self.modules[index]
            indicies_of_dependencies = self.find_dependency_indicies(index)
            node = self.make_graph_node(
                dependency_module.name,
                indicies_of_dependencies,
                dependency_module.directory_path,
                index,
            )
            if node:
                self.add_to_node_graph(node)
                self.visit_dependency_nodes(node)

    # A node (module representation) can only continue onward to another module
    # being a unseen module, or a seen module, or the module has no dependencies
    # If seen (a cycle), the code continues even after building the error stack,
    # because there can be even more cycles to report also
    # (down through other dependencies not seen yet)
    def check_dependency_graph(self):
        self.indicies_of_nodes_visited = set()
        main_node = None
        for node_idx in self.node_graph:
            node = self.node_graph[node_idx]
            if node["name"] == "main":
                main_index = node_idx
                main_node = node
                break
        if main_node is None:
            raise Exception("Could not find main node in module graph")

        stack_trace = CycleStackTrace()
        self.visit_module_graph(stack_trace, main_node)

    def visit_module_graph(self, stack_trace, node):
        if node["node_index"] in self.indicies_of_nodes_visited:
            self.generate_cycle_error(node, stack_trace)
            return
        self.indicies_of_nodes_visited.add(node["node_index"])
        for dependency_node_idx in node["dependency_indicies"]:
            dependency_node = self.node_graph[dependency_node_idx]
            stack_trace.push(node["node_index"], node["name"], dependency_node_idx)
            self.visit_module_graph(stack_trace, dependency_node)
            stack_trace.pop()
        self.indicies_of_nodes_visited.remove(node["node_index"])

    def add_to_node_graph(self, node):
        if node["node_index"] in self.node_graph:
            return
        self.node_graph[node["node_index"]] = node

    def generate_cycle_error(self, node, stack_trace):
        stack_from_main = stack_trace.get_stack_trace()
        modules_involved_in_cycle = None
        for i in range(len(stack_from_main)):
            if stack_from_main[i].node_index == node["node_index"]:
                modules_involved_in_cycle = stack_from_main[i:]
                break
        if modules_involved_in_cycle is None:
            raise Exception("Could not locate cycle creating module in stack trace")
        import_statement_module_name_tokens = []
        for stack_item in modules_involved_in_cycle:
            import_statement_module_name_token = (
                self.find_import_module_name_of_dependency(stack_item)
            )
            import_statement_module_name_tokens.append(
                import_statement_module_name_token
            )
        self.error_manager.add_error(
            MODULE_DEPENDENCY_CYCLE_DETECTED, import_statement_module_name_tokens
        )

    def find_import_module_name_of_dependency(self, stack_item: StackItem):
        node_index = stack_item.node_index
        dependant_module = self.modules[node_index]
        dependency_index = stack_item.dependency_index

        dependency_module_node = self.node_graph[dependency_index]
        dependency_module_name = dependency_module_node["name"]
        import_statement_module_token = None
        for import_statement in dependant_module.imports:
            if import_statement.get_source_name().literal == dependency_module_name:
                import_statement_module_token = import_statement.get_source_name()
        if import_statement_module_token is None:
            raise Exception("Could not locate module name in modules import statements")
        return import_statement_module_token
