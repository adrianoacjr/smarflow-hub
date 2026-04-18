class UserAlreadyExistsError(Exception):
    pass

class InvalidPasswordError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class UnauthenticatedUserError(Exception):
    pass

class InactiveUserError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class SamePasswordError(Exception):
    pass
