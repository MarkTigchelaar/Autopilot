
class Query:
    def __init__(self, object_id) -> None:
        self.object_id = object_id
        self.index = 0

    def execute(self, _) -> None:
        raise NotImplementedError("Subclasses must implement this method")
    
    def has_next(self) -> bool:
        raise NotImplementedError("Subclasses must implement this method")
    
    def next(self):
        raise NotImplementedError("Subclasses must implement this method")

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.has_next():
            return self.next()
        else:
            raise StopIteration
