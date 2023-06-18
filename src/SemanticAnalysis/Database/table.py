

class Table:
    def __init__(self, table_name, column_names):
        self.column_names = column_names
        self.index = dict()
        self.index_column_number = None
        self.name = table_name
    
    def make_index(self, col_name):
        for col, i in enumerate(self.column_names):
            if col == col_name:
                self.index_column_number = i
                break
        if self.index_column_number is None:
            raise Exception("INTERNAL ERROR: column name " + col_name + " not found")
    
    def make_blank_row(self):
        return Row(self.column_names)

    def insert_row(self, row):
        idx_column = row.cells[self.index_column_number]
        if len(row.columns) != len(self.column_names):
            raise Exception("INTERNAL ERROR: row being inserted does not have same columns as table.")
        if idx_column.cell_name != self.column_names[self.index_column_number]:
            raise Exception("INTERNAL ERROR: row does not contain indexed column")
        if idx_column.cell_item in self.index:
            raise Exception("INTERNAL ERROR: row contains duplicated value found in index")
        else:
            self.index[idx_column.cell_item] = row
    
    def get_row(self, key):
        if key not in self.index:
            raise Exception("INTERNAL ERROR: key " + str(key) + "not in table")
        return self.index[key]
    
    def get_rows(self, keys):
        return [self.get_row(key) for key in keys]

class Row:
    def __init__(self, column_names):
        self.column_names = column_names
        self.cells = []

    def insert_cell(self, cell):
        if cell.name not in self.column_names:
            raise Exception("INTERNAL ERROR: cell " + cell.name + "does not have a valid column name")
        idx = len(self.cells)
        if self.column_names[idx] != cell.name:
            raise Exception("INTERNAL ERROR: cell " + cell.name + "is in the incorrect column position")
        self.cells.append(cell)

class Cell:
    def __init__(self, cell_name, cell_item):
        self.name = cell_name
        self.item = cell_item




