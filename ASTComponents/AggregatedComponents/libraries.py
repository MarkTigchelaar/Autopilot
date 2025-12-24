

"""
relies on library config, currently json files
ALL LibraryItem types are public.
interfaces cannot be used by non library items,
including items of a different library
"""
class LibraryItem:
    def __init__(self, item_name):
        self.item_name = item_name

    def get_name(self) -> str:
        return self.item_name




class LibraryEnum(LibraryItem):
    def __init__(self, config):
        super().__init__(config["name"])
        pass

# class LibraryError(LibraryItem):
#     def __init__(self, config):
#         pass

class LibraryUnion(LibraryItem):
    def __init__(self, config):
        super().__init__(config["name"])
        pass

class LibraryFunction(LibraryItem):
    def __init__(self, config):
        super().__init__(config["name"])
        pass

class LibraryStruct(LibraryItem):
    def __init__(self, config):
        super().__init__(config["name"])
        pass

class LibraryInterface(LibraryItem):
    def __init__(self, config):
        super().__init__(config["name"])
        pass

# Only library optionals, and results are public, module versions are not
class LibraryOptional(LibraryItem):
    def __init__(self, config):
        super().__init__(config["name"])
        pass

class LibraryResult(LibraryItem):
    def __init__(self, config):
        super().__init__(config["name"])
        pass

# Errors not public, since the are only used in Result types
class Library:
    def __init__(self, json_config):
        self.item_names: dict[str, str] = dict()
        self.enum_defs: dict[str, LibraryEnum] = dict()
        #self.error_defs: dict[str, LibraryError] = dict()
        self.union_defs: dict[str, LibraryUnion] = dict()
        self.function_defs: dict[str, LibraryFunction] = dict()
        self.struct_defs: dict[str, LibraryStruct] = dict()
        self.interface_defs: dict[str, LibraryInterface] = dict()
        self.optional_defs: dict[str, LibraryOptional] = dict()
        self.result_defs: dict[str, LibraryResult] = dict()

        for config in json_config["enums"]:
            library_type_def = LibraryEnum(config)
            self.enum_defs[library_type_def.get_name()] = library_type_def
            self.item_names[library_type_def.get_name()] = "enums"
        
        # for config in json_config["errors"]:
        #     library_type_def = LibraryError(config)
        #     self.error_defs[library_type_def.get_name()] = library_type_def
        #     self.item_names[library_type_def.get_name()] = "errors"

        for config in json_config["unions"]:
            library_type_def = LibraryUnion(config)
            self.union_defs[library_type_def.get_name()] = library_type_def
            self.item_names[library_type_def.get_name()] = "unions"

        for config in json_config["functions"]:
            library_type_def = LibraryFunction(config)
            self.function_defs[library_type_def.get_name()] = library_type_def
            self.item_names[library_type_def.get_name()] = "functions"
        
        for config in json_config["structs"]:
            library_type_def = LibraryStruct(config)
            self.struct_defs[library_type_def.get_name()] = library_type_def
            self.item_names[library_type_def.get_name()] = "structs"

        for config in json_config["interfaces"]:
            library_type_def = LibraryInterface(config)
            self.interface_defs[library_type_def.get_name()] = library_type_def
            self.item_names[library_type_def.get_name()] = "interfaces"

        for config in json_config["optionals"]:
            library_type_def = LibraryOptional(config)
            self.optional_defs[library_type_def.get_name()] = library_type_def
            self.item_names[library_type_def.get_name()] = "optionals"

        for config in json_config["results"]:
            library_type_def = LibraryResult(config)
            self.result_defs[library_type_def.get_name()] = library_type_def
            self.item_names[library_type_def.get_name()] = "results"


    def has_item(self, item_name: str) -> bool:
        return item_name in self.item_names
    
    def get_item(self, item_name: str) -> LibraryItem:
        if not self.has_item(item_name):
            raise Exception("Item is not in library")
        type_key = self.item_names[item_name]
        match type_key:
            case "enums":
                return self.enum_defs[item_name]
            case "errors":
                return self.error_defs[item_name]
            case "unions":
                return self.union_defs[item_name]
            case "functions":
                return self.function_defs[item_name]
            case "structs":
                return self.struct_defs[item_name]
            case "interfaces":
                return self.interface_defs[item_name]
