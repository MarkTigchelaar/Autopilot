from Parsing.ASTComponents.ExternalComponents.struct_statement import StructStatement, StructField
from TestingComponents.testing_utilities import token_to_json



class TestingStructStatement:
    def __init__(self):
        self.struct_statement = StructStatement()

    def add_name(self, name_token):
        self.struct_statement.add_name(name_token)

    def add_acyclic_token(self, acyclic_token):
        self.struct_statement.add_acyclic_token(acyclic_token)
    
    def add_inline_token(self, inline_token):
        self.struct_statement.add_inline_token(inline_token)
    
    def add_public_token(self, pub_token):
        self.struct_statement.add_public_token(pub_token)

    def add_field(self, field):
        self.struct_statement.add_field(field)

    def add_function(self, function):
        self.struct_statement.add_function(function)

    def add_interface(self, interface_token):
        self.struct_statement.add_interface(interface_token)

    def print_literal(self, repr_list: list) -> None:
        if self.struct_statement.acyclic_token:
            repr_list.append(self.struct_statement.acyclic_token.literal + " ")
        if self.struct_statement.inline_token:
            repr_list.append(self.struct_statement.inline_token.literal + " ")
        if self.struct_statement.public_token:
            repr_list.append(self.struct_statement.public_token.literal + " ")
        repr_list.append(self.struct_statement.name_token.literal + " ")
        for interface in self.struct_statement.interfaces:
            repr_list.append(interface.literal + " ")
        for field in self.struct_statement.fields:
            field = field.struct_field
            # if field.acyclic_token:
            #     repr_list.append(field.acyclic_token.literal + " ")
            if field.public_token:
                repr_list.append(field.public_token.literal + " ")
            repr_list.append(field.field_name_token.literal + " ")
            repr_list.append(field.type_token.literal + " ")
        for function in self.struct_statement.functions:
            function.print_literal(repr_list)
        
            

    def print_token_types(self, type_list: list) -> None:
        if self.struct_statement.acyclic_token:
            type_list.append(self.struct_statement.acyclic_token.type_symbol + " ")
        if self.struct_statement.inline_token:
            type_list.append(self.struct_statement.inline_token.type_symbol + " ")
        if self.struct_statement.public_token:
            type_list.append(self.struct_statement.public_token.type_symbol + " ")
        type_list.append(self.struct_statement.name_token.type_symbol + " ")
        for interface in self.struct_statement.interfaces:
            type_list.append(interface.type_symbol + " ")
        for field in self.struct_statement.fields:
            field = field.struct_field
            # if field.acyclic_token:
            #     type_list.append(field.acyclic_token.type_symbol + " ")
            if field.public_token:
                type_list.append(field.public_token.type_symbol + " ")
            type_list.append(field.field_name_token.type_symbol + " ")
            type_list.append(field.type_token.type_symbol + " ")
        for function in self.struct_statement.functions:
            function.print_token_types(type_list)

    def to_json(self) -> dict:
        return {
            "type" : "struct",
            "name" : token_to_json(self.struct_statement.name_token),
            "attributes" : {
                "acyclic" : token_to_json(self.struct_statement.acyclic_token),
                "public" : token_to_json(self.struct_statement.public_token),
                "inline" : token_to_json(self.struct_statement.inline_token)
            },
            "interfaces" : self.interfaces_to_json(),
            "fields" : self.fields_to_json(),
            "functions" : self.functions_to_json()
        }

    def interfaces_to_json(self):
        interface_list = list()
        for interface in self.struct_statement.interfaces:
            interface_list.append(token_to_json(interface))
        return interface_list

    def fields_to_json(self):
        field_list = list()
        for field in self.struct_statement.fields:
            field_list.append(field.to_json())
        return field_list

    def functions_to_json(self):
        function_list = list()
        for function in self.struct_statement.functions:
            function_list.append(function.to_json())
        return function_list

class TestingStructField:
    def __init__(self):
        self.struct_field = StructField()
    
    def add_public_token(self, public_token):
        self.struct_field.add_public_token(public_token)
    
    # def add_acyclic_token(self, acyclic_token):
    #     self.struct_field.add_acyclic_token(acyclic_token)
    
    # def add_inline_token(self, inline_token):
    #     self.struct_field.add_inline_token(inline_token)
    
    def add_field_name(self, field_name_token):
        self.struct_field.add_field_name(field_name_token)
    
    def add_type_token(self, type_token):
        self.struct_field.add_type_token(type_token)
    
    def to_json(self) -> dict:
        return {
            "type" : "field",
            "name" : token_to_json(self.struct_field.field_name_token),
            "type" : token_to_json(self.struct_field.type_token),
            "public" : token_to_json(self.struct_field.public_token)
        }