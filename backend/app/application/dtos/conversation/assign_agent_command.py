from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True, slots=True)
class AssignAgentCommand:
    conversation_id: UUID
    agent_id: int
