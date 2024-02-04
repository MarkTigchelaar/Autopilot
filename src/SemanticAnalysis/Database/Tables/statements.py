class StatementTable:
    def __init__(self):
        self.by_key = dict()
        self.by_container_id = dict()

    def get_size(self):
        return len(self.by_key)

    def has_contents(self):
        return len(self.by_key) > 0

    def insert(
        self, stmt_type_token, statement, container_object_id, sequence_num, scope_depth
    ):
        if stmt_type_token is None:
            print(type(statement))
        # Container id is always the function, or unittest object id.
        potential_key = StatementTableKey(sequence_num, container_object_id)
        if potential_key in self.by_key:
            raise Exception("INTERNAL ERROR: id of modifed ast node already defined")

        row = StatementRow(
            stmt_type_token, statement, container_object_id, sequence_num, scope_depth
        )
        self.by_key[potential_key] = row

        if container_object_id not in self.by_container_id:
            self.by_container_id[container_object_id] = list()
        self.by_container_id[container_object_id].append(row)

    def is_object_defined(self, container_object_id, sequence_num = None):
        if sequence_num is None:
            return False
        potential_key = StatementTableKey(sequence_num, container_object_id)
        return potential_key in self.by_key

    def get_item_by_id_and_seq_num(self, container_object_id, sequence_num):
        return self.by_key[StatementTableKey(sequence_num, container_object_id)]

    def get_rows_by_container_id(self, container_id):
        rows = self.by_container_id[container_id]
        rows.sort(key=lambda x: x.sequence_num, reverse=False)
        return rows


class StatementTableKey:
    def __init__(self, sequence, container_id):
        self.sequence = sequence
        self.container_id = container_id

    def __hash__(self):
        return int(str(self.sequence) + str(self.container_id))

    def __eq__(self, other):
        return (
            self.sequence == other.sequence and self.container_id == other.container_id
        )


class StatementRow:
    def __init__(
        self,
        stmt_type_token,
        statement,
        container_object_id,  # function / unittest
        sequence_num,  # ordering of statements, depth first
        scope_depth,
    ):
        self.statement = statement
        self.container_object_id = container_object_id
        self.sequence_num = sequence_num
        self.scope_depth = scope_depth
        self.stmt_type_token = stmt_type_token
