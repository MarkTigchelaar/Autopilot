import os
import ErrorHandling.filesystem_semantic_error_messages as ErrMsg
from Tokenization.symbols import CARROT, RANGE, COLON, DOT

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

    def get_matching_directories(self):
        return self.matching_directories

    def collect_matching_module_ids(self, module_list):
        matching_modules = [
            module.module_id
            for module in module_list
            if self.reformat_path_list(module.path) in self.matching_directories
            and module.module_id != self.current_module_id
        ]
        return matching_modules
    
    def collect_matching_modules(self, raw_modules):
        return [
            module for module in raw_modules if self.reformat_path_list(module.directory_path) in self.matching_directories
        ]

    def reformat_path_list(self, path_string):
        norm_path = os.path.normpath(path_string)
        # norm path is a straight shot from the root to the directory
        # no .. included
        return norm_path

    def _collect_valid_paths_helper(self, directory, index):
        i = index
        while i < len(self.path_list):
            path_item = self.path_list[i]
            if path_item.direction_token is None:
                break
            elif path_item.direction_token.internal_type == RANGE:
                if self.upward_search_restricted:
                    self.error_manager.add_error(
                        path_item.direction_token, ErrMsg.PATH_BACKTRACKING
                    )
                    return
                directory = os.path.dirname(directory)
                child_folder = path_item.node_token.literal
                directory = os.path.join(directory, child_folder)
            elif path_item.direction_token.internal_type == CARROT:
                if self.upward_search_restricted:
                    self.error_manager.add_error(
                        path_item.direction_token, ErrMsg.PATH_BACKTRACKING
                    )
                    return
                found = False

                for _ in range(10):
                    if os.path.basename(directory) == path_item.node_token.literal: 
                        found = True
                        i += 1
                        if i < len(self.path_list):
                            path_item = self.path_list[i]
                        else:
                            path_item = None
                        break
                    directory = os.path.dirname(directory)
                
                if path_item:
                    child_folder = path_item.node_token.literal
                else:
                    child_folder = ""
                directory = os.path.join(directory, child_folder)
                if not found:
                    self.error_manager.add_error(
                        path_item.node_token, ErrMsg.IMPORT_PATH_MISSING_PARENT_FOLDER
                    )
                    return
            elif path_item.direction_token.internal_type == COLON:
                
                if i == 0 and len(self.path_list) == 2:
                    # import ... from module name:module_name
                    # This means that a special case is present, collect ALL subdirectories
                    # of the current directory
                    matching_subdirectories = self._check_subfolders(directory)
                    for subdirectory in matching_subdirectories:
                        # dirty way to just add to the set.
                        self._collect_valid_paths_helper(subdirectory, len(self.path_list) + 1)
                    break
                i += 1
                if i < len(self.path_list):
                    child_folder = self.path_list[i].node_token.literal
                    matching_subdirectories = self._check_subfolders(
                        directory, child_folder
                    )
                    for subdirectory in matching_subdirectories:
                        self._collect_valid_paths_helper(subdirectory, i + 1)
                elif i == len(self.path_list) and len(self.path_list) == 1:
                    child_folder = self.path_list[i-1].node_token.literal
                    matching_subdirectories = self._check_subfolders(
                        directory, child_folder
                    )
                    for subdirectory in matching_subdirectories:
                        self._collect_valid_paths_helper(subdirectory, i + 1)

                    
            elif path_item.direction_token.internal_type == DOT:
                self.upward_search_restricted = True
                if i < len(self.path_list):
                    child_folder = self.path_list[i].node_token.literal
                    directory = os.path.join(directory, child_folder)

            i += 1
        directory = self.reformat_path_list(directory)
        if os.path.exists(directory):
            self.matching_directories.add(directory)

    def _check_subfolders(self, directory, target_folder = ""):
        matching_subdirectories = []
        for root, dirs, _ in os.walk(directory):
            if target_folder in dirs or target_folder == "":
                matching_subdirectories.append(os.path.join(root, target_folder))
        return matching_subdirectories
