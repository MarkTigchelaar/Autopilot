from SemanticAnalysis.Database.SaveData.saver import Saver

class FnHeaderSaver(Saver):
    def __init__(self, database, fn_headers):
        self.database = database
        self.fn_headers = fn_headers
        self.header_ids = []
    

    def save_header_ids(self):
        for header in self.fn_headers:
            header_id = self.database.save_object(header)
            self.header_ids.append(header_id)
        return self.header_ids

    def save_headers(self):
        current_module_id = self.database.get_current_module_id()
        type_name_table = self.database.get_table("typenames")
        header_table = self.database.get_table("fn_headers")
        modifier_table = self.database.get_table("modifiers")
        for i, header_id in enumerate(self.header_ids):
            acyclic_token = self.fn_headers[i].acyclic_token
            inline_token = self.fn_headers[i].inline_token
            public_token = self.fn_headers[i].public_token
            mods = []
            for tok in [acyclic_token, inline_token, public_token]:
                if tok:
                    mods.append(tok)
            if len(mods) > 0:
                modifier_table.insert(
                    header_id,
                    mods
                )
            header_table.insert(
                header_id, 
                self.fn_headers[i]
            )
            type_name_table.insert(
                self.fn_headers[i].name_token,
                "fn_header",
                current_module_id,
                header_id
            )
