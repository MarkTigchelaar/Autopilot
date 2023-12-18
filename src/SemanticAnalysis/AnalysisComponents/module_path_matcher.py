import os
import ErrorHandling.semantic_error_messages as ErrMsg
from symbols import CARROT, RANGE, COLON, DOT
# class Token:
#     def __init__(self, literal: str):
#         self.literal = literal


# class PathItem:
#     def __init__(self, node_token: Token, direction_token: Token):
#         self.node_token = node_token
#         self.direction_token = direction_token


# class ModulePathIdRow:
#     def __init__(self, path, module_id, name):
#         self.path = path
#         self.module_id = module_id
#         self.name = name


class ModulePathMatcher:
    def __init__(self, current_module_id, path_list, starting_directory, error_manager):
        self.current_module_id = current_module_id
        self.path_list = path_list
        self.starting_directory = self.reformat_path_list(starting_directory)
        self.error_manager = error_manager
        self.upward_search_restricted = False
        self.matching_directories = set()

    def collect_valid_paths(self):
        self._collect_valid_paths_helper(self.starting_directory, 0)

    def collect_matching_module_ids(self, module_list):
        matching_modules = [
            module.module_id
            for module in module_list
            if self.reformat_path_list(module.path) in self.matching_directories
            and module.module_id != self.current_module_id
        ]
        return matching_modules

    def reformat_path_list(self, path_string):
        norm_path = os.path.normpath(path_string)
        # norm path is a straight shot from the root to the directory
        # no .. included
        return norm_path

    def _collect_valid_paths_helper(self, directory, index):
        i = index
        while i < len(self.path_list):
            path_item = self.path_list[i]

            if path_item.direction_token.type_symbol == RANGE:
                if self.upward_search_restricted:
                    self.error_manager.add_semantic_error(
                        path_item.direction_token, ErrMsg.PATH_BACKTRACKING
                    )
                    return
                directory = os.path.dirname(directory)
            elif path_item.direction_token.type_symbol == CARROT:
                if self.upward_search_restricted:
                    self.error_manager.add_semantic_error(
                        path_item.direction_token, ErrMsg.PATH_BACKTRACKING
                    )
                    return
                found = False
                i += 1
                path_item = self.path_list[i]
                for _ in range(10):
                    if os.path.basename(directory) == path_item.node_token.literal: 
                        # should probably add a new wildcard for going upwards
                        found = True
                        break
                    directory = os.path.dirname(directory)
                if not found:
                    self.error_manager.add_semantic_error(
                        path_item.node_token, ErrMsg.IMPORT_PATH_MISSING_PARENT_FOLDER
                    )
                    return
            elif path_item.direction_token.type_symbol == COLON:
                i += 1
                if i < len(self.path_list):
                    child_folder = self.path_list[i].node_token.literal
                    matching_subdirectories = self._check_subfolders(
                        directory, child_folder, i + 1
                    )
                    for subdirectory in matching_subdirectories:
                        self._collect_valid_paths_helper(subdirectory, i + 1)
            elif path_item.direction_token.type_symbol == DOT:
                self.upward_search_restricted = True
                if i < len(self.path_list):
                    child_folder = self.path_list[i].node_token.literal
                    directory = os.path.join(directory, child_folder)

            i += 1
        directory = self.reformat_path_list(directory)
        self.matching_directories.add(directory)

    def _check_subfolders(self, directory, target_folder, index):
        matching_subdirectories = []
        for root, dirs, _ in os.walk(directory):
            if target_folder in dirs:
                matching_subdirectories.append(os.path.join(root, target_folder))
        return matching_subdirectories

# Example usage
# current_module_id = 1

# path_list = [
#     PathItem(Token("current_folder_name"), Token("..")),
#     PathItem(Token("otherfolder"), Token("..")),
#     PathItem(Token("another_folder"), Token("down_into_a_folder")),
#     PathItem(Token(":"), Token("one_of_the_folders")),
#     PathItem(Token("last_folder"), Token("")),
# ]

# starting_directory = "/path/to/current_folder_name"

# module_list = [
#     ModulePathIdRow("/path/to/current_folder_name", 1, "current_folder_name"),
#     ModulePathIdRow("/path/to/otherfolder", 2, "otherfolder"),
#     ModulePathIdRow(
#         "/path/to/another_folder/down_into_a_folder", 3, "down_into_a_folder"
#     ),
#     ModulePathIdRow("/path/to/one_of_the_folders/last_folder", 4, "last_folder"),
# ]

# matcher = ModulePathMatcher(current_module_id, path_list, starting_directory)
# matcher.collect_valid_paths()
# matching_modules = matcher.collect_matching_modules(module_list)

# for module in matching_modules:
#     print(
#         f"Matching Module: {module.name}, ID: {module.module_id}, Path: {module.path}"
#     )
