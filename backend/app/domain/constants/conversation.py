CONVERSATION_HISTORY_SIZE: int = 10
AI_CONFIDENCE_THRESHOLD: float = 0.65

HUMAN_ESCALATION_TRIGGERS: frozenset[str] = frozenset({
    "falar com atendente",
    "falar com humano",
    "atendente humano",
    "quero um humano",
    "preciso de ajuda humana",
    "falar com pessoa",
    "speak to agent",
    "talk to human",
    "human agent",
    "real person",
})
