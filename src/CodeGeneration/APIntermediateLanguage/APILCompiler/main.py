"""
    apil: Autopilot Intermediate Language
    This represents a distinct, and seperate language from the autopilot language.
    This language is used to represent the logic written in the autopilot language in a more low level manner.
    This seperation of compilers simplifies the process of writing a compiler for the autopilot language.
    This compiler assumes correct syntax and semantics, and does several basic reductions and optimizations.
    The results is april: Autopilot Reduced Intermediate Language, which is a more abstract assembly language.
"""

from typing import List, Dict



class SectionContainer:
    def __init__(self):
        self.sections = dict()

    def add_section(self, name, section_content_list):
        self.sections[name] = section_content_list

    def get_sections(self):
        return self.sections

def compile_apil_to_april(apil_program: List[str]) -> List[str]:
    april_program = apil_main(apil_program)

    with open("output.april", "w") as file:
        for line in april_program:
            file.write(line + "\n")
    return april_program

def apil_main(apil_program: List[str]) -> List[str]:
    april_program = []
    # modules = split_sections(apil_program, "DEFINE MODULE", "END MODULE")
    # print_modules(modules)
    # assign_types_to_variables(modules)
    parsed_modules = parse_apil(apil_program)
    #renamed_program = rename_variables(parsed_modules)



    return april_program





def print_modules(section_container: SectionContainer):
    f = open("modules.txt", "w")
    for module_name, module_content in section_container.get_sections().items():
        f.write(f"Module: {module_name}\n")
        for line in module_content:
            f.write(line + "\n")
        f.write("\n")
    f.close()

# DEFINE MODULE <name>
def get_section_name(module_line: str) -> str:
    module_line = module_line.strip()
    print("module_line", module_line)
    return module_line.split(" ")[2]



def assign_types_to_variables(section_container):
    for module_name in section_container.get_sections():
        module = section_container.get_sections()[module_name]
        assign_types_to_variables_in_module(module)

def assign_types_to_variables_in_module(module):
    functions = split_sections(module, "DEFINE FUNCTION", "END FUNCTION")
    print_functions(functions)
    pass


def print_functions(functions):
    f = open("functions.txt", "w")
    function_map = functions.get_sections()
    for function_name in function_map:
        f.write(f"Function: {function_name}\n")
        function_content = function_map[function_name]
        for line in function_content:
            f.write(line + "\n")
        f.write("\n")
    f.close()






# These are the classes that represent the intermediate languages AST
class Module:
    def __init__(self):
        self.name = None
        self.imports = []
        self.key_value_defines = []
        self.list_type_defines = []
        self.stack_type_defines = []
        self.queue_type_defines = []
        self.option_type_defines = []
        self.result_type_defines = []
        self.function_type_defines = []
        self.enums = []
        self.structs = []
        self.inline_structs = []
        self.interfaces = []
        self.functions = []
        self.inline_functions = []
        self.unions = []
        self.errors = []
        self.unittests = []

class Import:
    def __init__(self):
        self.module_name = None
        self.imports = []

class ImportItem:
    def __init__(self):
        self.name = None
        self.alias = None


class MapDefine:
    def __init__(self):
        self.sub_type = None
        self.name = None
        self.key_type = None
        self.value_value = None

class LinearDefine:
    def __init__(self):
        self.sub_type = None
        self.name = None
        self.element_type = None

class FailableDefine:
    def __init__(self):
        self.sub_type = None
        self.name = None
        self.element_type = None
        self.error_type = None

class FunctionSignatureDefine:
    def __init__(self):
        self.name = None
        self.args = []
        self.return_type = None

class Enum:
    def __init__(self):
        self.name = None
        self.element_type = None
        self.values = []

class EnumElement:
    def __init__(self):
        self.name = None
        self.value = None

class Union:
    def __init__(self):
        self.name = None
        self.elements = []

class UnionElement:
    def __init__(self):
        self.name = None
        self.element_type = None

class Error:
    def __init__(self):
        self.name = None
        self.error_types = []


class Interface:
    def __init__(self):
        self.name = None
        self.fn_signatures = []

class Struct:
    def __init__(self):
        self.name = None
        self.fields = []
        self.methods = []
        self.interfaces = []





class Function:
    def __init__(self):
        self.name = None
        self.args = []
        self.return_type = None
        self.locals = []
        self.statements = []


class Variable:
    def __init__(self):
        self.name = None
        self.type = None
        self.types_module_of_origin = None
        self.value = None




def split_sections(apil_program: List[str], section_start, section_end) -> SectionContainer:
    section_container = SectionContainer()
    current_module = []
    line = 0
    end_line = len(apil_program)
    while line < end_line:
        if section_start in apil_program[line]: # ignore spaces on LHS
            module_name = get_section_name(apil_program[line])
            line += 1
            while line < end_line and not (f"{section_end} {module_name}" in apil_program[line]):
                current_module.append(apil_program[line])
                line += 1
            line += 1
            section_container.add_section(module_name, current_module)
            current_module = []
        else:
            line += 1

    return section_container


def parse_apil(apil_program):
    module_sections = split_sections(apil_program, "DEFINE MODULE", "END MODULE")
    sections = module_sections.get_sections()
    modules = []
    main_module = parse_module(sections["main"], "main")
    modules.append(main_module)
    for module_name in sections:
        if module_name != "main":
            module = parse_module(sections[module_name], module_name)
            modules.append(module)


def parse_module(section: List[str], module_name: str) -> Module:
    module = Module()
    module.name = module_name
    parse_imports(module, section)
    parse_key_value_defines(module, section)
    parse_list_defines(module, section)
    parse_stack_defines(module, section)
    parse_queue_defines(module, section)
    parse_option_defines(module, section)
    parse_result_defines(module, section)
    parse_function_defines(module, section)
    parse_enums(module, section)
    parse_structs(module, section)
    parse_inline_structs(module, section)
    parse_interfaces(module, section)
    parse_functions(module, section)
    parse_inline_functions(module, section)
    parse_unions(module, section)
    parse_errors(module, section)
    parse_unittests(module, section)
    return module

def parse_imports(module: Module, section: List[str]):
    import_section = split_sections(section, "IMPORT MODULE", "END IMPORT")
    imports = import_section.get_sections()
    for import_name in imports:
        import_stmt = Import()
        import_stmt.module_name = import_name
        import_items = imports[import_name]
        for item in import_items:
            item = item.strip()
            import_item = ImportItem()
            import_item.name = item.split(" ")[1]
            import_item.alias = item.split(" ")[2]
            import_stmt.imports.append(import_item)
        module.imports.append(import_stmt)

def parse_key_value_defines(module: Module, section: List[str]):
    map_sections = split_sections(section, "DEFINE Map", "END Map")
    hash_sections = split_sections(section, "DEFINE HashMap", "END HashMap")
    tree_setions = split_sections(section, "DEFINE Dictionary", "END Dictionary")
    add_kv_defines(module, map_sections, "Map")
    add_kv_defines(module, hash_sections, "HashMap")
    add_kv_defines(module, tree_setions, "Dictionary")

def add_kv_defines(module: Module, section: List[str], sub_type: str):
    for tree_name in section.get_sections():
        tree_define = MapDefine()
        tree_define.name = tree_name
        tree_define.sub_type = sub_type
        tree_define.key_type = section.get_sections()[tree_name][0].split(" ")[1]
        tree_define.value_type = section.get_sections()[tree_name][1].split(" ")[1]
        module.key_value_defines.append(tree_define)

def parse_list_defines(module: Module, section: List[str]):
    list_types = parse_linear_collection_defines(section, "List", "DEFINE List", "END List")
    module.list_type_defines.extend(list_types)
    linked_list_types = parse_linear_collection_defines(section, "LinkedList", "DEFINE LinkedList", "END LinkedList")
    module.list_type_defines.extend(linked_list_types)
    vector_types = parse_linear_collection_defines(section, "Vector", "DEFINE Vector", "END Vector")
    module.list_type_defines.extend(vector_types)


def parse_stack_defines(module: Module, section: List[str]):
    stack_defines = parse_linear_collection_defines(module, section, "Stack", "DEFINE Stack", "END Stack")
    module.stack_type_defines.extend(stack_defines)

def parse_queue_defines(module: Module, section: List[str]):
    queue_defines = parse_linear_collection_defines(section, "Queue", "DEFINE Queue", "END Queue")
    module.queue_type_defines.extend(queue_defines)
    fifo_queue_defines = parse_linear_collection_defines(section, "FifoQueue", "DEFINE FifoQueue", "END FifoQueue")
    module.queue_type_defines.extend(fifo_queue_defines)
    priority_queue_defines = parse_linear_collection_defines(section, "PriorityQueue", "DEFINE PriorityQueue", "END PriorityQueue")
    module.queue_type_defines.extend(priority_queue_defines)
    deque_defines = parse_linear_collection_defines(section, "Deque", "DEFINE Deque", "END Deque")
    module.queue_type_defines.extend(deque_defines)


def parse_linear_collection_defines(section: List[str], sub_type: str, start: str, end: str):
    list_sections = split_sections(section, start, end)
    parsed_sections = list()
    for list_name in list_sections.get_sections():
        list_define = LinearDefine()
        list_define.name = list_name
        list_define.sub_type = sub_type
        list_define.element_type = list_sections.get_sections()[list_name][0].split(" ")[1]
        parsed_sections.append(list_define)
    return parsed_sections

def parse_option_defines(module: Module, section: List[str]):
    option_defines = parse_failable_types(section, "Option", "DEFINE Option", "END Option")
    module.option_type_defines.extend(option_defines)

def parse_result_defines(module: Module, section: List[str]):
    result_defines = parse_failable_types(section, "Result", "DEFINE Result", "END Result")
    module.result_type_defines.extend(result_defines)

def parse_failable_types(section: List[str], sub_type: str, start: str, end: str):
    failable_sections = split_sections(section, start, end)
    parsed_sections = list()
    for failable_name in failable_sections.get_sections():
        failable_define = FailableDefine()
        failable_define.name = failable_name
        failable_define.sub_type = sub_type
        elements = failable_sections.get_sections()[failable_name]
        failable_define.element_type = failable_sections.get_sections()[failable_name][0].split(" ")[1]
        if len(elements) == 2:
            failable_define.error_type = failable_sections.get_sections()[failable_name][1].split(" ")[1]
        else:
            raise Exception("Failable types must have exactly 2 elements")
        parsed_sections.append(failable_define)
    return parsed_sections

def parse_function_defines(module: Module, section: List[str]):
    function_defines = parse_function_signatures(section)
    module.function_type_defines.extend(function_defines)



def parse_function_signatures(section: List[str]):
    function_sections = split_sections(section, "DEFINE FUNCTION_SIGNATURE", "END FUNCTION_SIGNATURE")
    function_signatures = list()
    for function_name in function_sections.get_sections():
        function_define = FunctionSignatureDefine()
        function_define.name = function_name
        function_content = function_sections.get_sections()[function_name]

        for element in function_content:
            components = element.split(" ")
            elem_type = components[1]
            elem_type = elem_type.strip()
            if components[0] == "RETURN_TYPE":
                function_define.return_type = elem_type
                continue
            function_define.args.append(elem_type)
        function_signatures.append(function_define)
    return function_signatures
        


def parse_enums(module: Module, section: List[str]):
    enum_sections = split_sections(section, "DEFINE ENUM", "END ENUM")
    for enum_name in enum_sections.get_sections():
        enum_define = Enum()
        enum_define.name = enum_name
        enum_content = enum_sections.get_sections()[enum_name]
        for element in enum_content:
            components = element.split(" ")
            if components[0] == "TYPE":
                enum_define.element_type = components[1]
                continue
            enum_element = EnumElement()
            enum_element.name = components[1]
            enum_element.value = components[2]
            enum_define.values.append(enum_element)
        module.enums.append(enum_define)

def parse_unions(module: Module, section: List[str]):
    union_sections = split_sections(section, "DEFINE UNION", "END UNION")
    for union_name in union_sections.get_sections():
        union_define = Union()
        union_define.name = union_name
        union_content = union_sections.get_sections()[union_name]
        for element in union_content:
            components = element.split(" ")
            union_element = UnionElement()
            union_element.name = components[1]
            union_element.element_type = components[2]
            union_define.elements.append(union_element)
        module.unions.append(union_define)

def parse_errors(module: Module, section: List[str]):
    error_sections = split_sections(section, "DEFINE ERROR", "END ERROR")
    for error_name in error_sections.get_sections():
        error_define = Error()
        error_define.name = error_name
        error_content = error_sections.get_sections()[error_name]
        for element in error_content:
            components = element.split(" ")
            error_define.error_types.append(components[1])
        module.errors.append(error_define)

def parse_interfaces(module: Module, section: List[str]):
    interface_sections = split_sections(section, "DEFINE INTERFACE", "END INTERFACE")
    for interface_name in interface_sections.get_sections():
        interface_define = Interface()
        interface_define.name = interface_name
        interface_content = interface_sections.get_sections()[interface_name]
        func_signatures = parse_function_signatures(interface_content)
        interface_define.fn_signatures.extend(func_signatures)
        module.interfaces.append(interface_define)

def parse_functions(module: Module, section: List[str]):
    function_sections = split_sections(section, "DEFINE FUNCTION", "END FUNCTION")
    for function_name in function_sections.get_sections():
        function_content = function_sections.get_sections()[function_name]

        function_define = Function()
        function_define.name = function_name
        #parse_body = False
        for element in function_content:
            components = element.split(" ")
            if components[0] == "RETURN_TYPE":
                function_define.return_type = components[1]
                continue
            elif components[0] == "ARGUMENT":
                arg = Variable()
                arg.name = components[1]
                arg.type = components[2]
                function_define.args.append(arg)
                continue
            elif components[0] == "BEGIN":
                #parse_body = True
                continue
            elif components[0] == "DECLARE":
                local = Variable()
                local.name = components[1]
                local.type = components[2]
                function_define.locals.append(local)
                continue
            elif "=" in element:
                components = element.split("=")
                assigned_variable = components[0].strip()
                rhs = parse_rhs(components[1].strip())


            function_define.statements.append(element)
        module.functions.append(function_define)


def parse_rhs(rhs: str):
    if "+" in rhs:
        pass
    elif "-" in rhs:
        pass
    elif "*" in rhs:
        pass
    elif "/" in rhs:
        pass
    elif "%" in rhs:
        pass
    elif "^" in rhs:
        pass
    elif "==" in rhs:
        pass
    elif "!=" in rhs:
        pass
    elif "<" in rhs:
        pass
    elif ">" in rhs:
        pass
    elif "<=" in rhs:
        pass
    elif ">=" in rhs:
        pass

class Statement:
    def __init__(self):
        self.assigned_variable = None
        self.destination_label = None
        self.operation = None
        self.label_name = None
        self.left_operand = None
        self.right_operand = None

def parse_inline_functions(module: Module, section: List[str]):
    pass

def parse_unittests(module: Module, section: List[str]):
    pass

def parse_structs(module: Module, section: List[str]):
    pass

def parse_inline_structs(module: Module, section: List[str]):
    pass







    #     if "IMPORT" in line:

    #     elif "DEFINE LinkedList" in line:

    #     elif "DEFINE Vector" in line:

    #     elif "DEFINE List" in line:




    #     elif "DEFINE Stack" in line:


    #     elif "DEFINE Queue" in line:

    #     elif "DEFINE FifoQueue" in line:

    #     elif "DEFINE PriorityQueue" in line:

    #     elif "DEFINE Deque" in line:




    #     elif "DEFINE ENUM" in line:

    #     elif "DEFINE UNION" in line:

    #     elif "DEFINE ERROR" in line:

    #     elif "DEFINE STRUCT" in line:

    #     elif "DEFINE INLINE_STRUCT" in line:

    #     elif "DEFINE INTERFACE" in line:

    #     elif "DEFINE UNITTEST" in line:

    return module



"""
    TODO:
        rename all elements in module to have module-data_structure-name format, to ensure no name conflicts
        join all modules into one, check for name collisions - raise exception if found
        do function inlining, also renaming of variables in functions being inlined
        possibly merge enums into code as constants
        pull struct methods out of structs, add the struct as the argument, rename self.<method|field> to <struct_name>.<method|field>
        rename struct methods as <struct_name>_<method_name> and replace calls to <struct_name>.<method_name> with <struct_name>_<method_name>(<struct_name>, ...)
        construct v tables for structs using interface(s) and add them as function pointer fields to the struct
        when called, push function pointer onto stack, and call special instruction to call function pointer.
        This special instruction should just call the function call instruction, but with the command to use the top of stack, rather than pointer in instructions.
        This will allow for dynamic dispatch of functions, as well as methods used in interfaces. (It's the same thing!)
"""