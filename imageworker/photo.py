from dataclasses import dataclass


@dataclass
class PhotoObject:
    content: bytes
    size: int
    path: str
