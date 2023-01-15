

class ContinueStatement:
    def __init__(self):
        self.continue_token = None

    def add_descriptor_token(self, continue_token):
        self.continue_token = continue_token