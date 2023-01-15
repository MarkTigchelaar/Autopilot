


class BreakStatement:
    def __init__(self):
        self.label_name_token = None

    def add_label_name(self, label_name):
        self.label_name_token = label_name
