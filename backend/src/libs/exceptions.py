

class AlreadyExists(Exception):
    # Entity already exists or violates uniqueness rules
    pass


class NotFound(Exception):
    # Entity not found
    pass

class PaginationError(Exception):
    pass