class ConversationNotFoundError(Exception):
    pass

class ConversationAlreadyResolvedError(Exception):
    pass

class ConversationInvalidTransitionError(Exception):
    pass

class AgentNotAvailableError(Exception):
    pass
