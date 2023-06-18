from SemanticAnalysis.Database.SaveData.saver import Saver


def save_enum(analyzer, ast_node):
    enum_saver = EnumSaver(ast_node)
    analyzer.save_item_to_data_store(enum_saver)


class EnumSaver(Saver):

    def __init__(self):
        pass

    # def save_to_db(self, database):
    #     pass