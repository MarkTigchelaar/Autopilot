def get_token_literal(token):
    if token is None:
        return ""
    return token.literal


def split_path_and_file_name(directory_path_and_name):
    if not directory_path_and_name.endswith(".ap"):
        raise Exception("INTERNAL ERROR: token found to have filename without .ap file extension")
    
    directory_path_and_name = directory_path_and_name.split("/")
    directory_path = directory_path_and_name[0:-1]
    directory_path = "/".join(directory_path) + "/"

    file_name = directory_path_and_name[-1]
    return directory_path, file_name
