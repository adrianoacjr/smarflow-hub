class ClientNotFoundError(Exception):
    pass

class ClientAlreadyExistsError(Exception):
    pass

class ClientInactiveError(Exception):
    pass

class InvalidClientPlanError(Exception):
    pass
