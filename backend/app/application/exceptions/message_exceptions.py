class MessageValidationError (Exception):
    pass

class CustomerNotFoundError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class MessageNotFoundError(Exception):
    pass

class InvalidMessageFlowError(Exception):
    pass

class MessageDeliveryError(Exception):
    pass

class InvalidMessageStatusTransitionError(Exception):
    pass
