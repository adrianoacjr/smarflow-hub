from dataclasses import dataclass

@dataclass(frozen=True)
class ChannelBinding:
    source: str
    external_ref: str
