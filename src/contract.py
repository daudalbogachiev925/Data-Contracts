from dataclasses import dataclass, field
from typing import List, Dict, Optional
import yaml

@dataclass
class FieldSpec:
    name: str
    type: str
    required: bool = True
    description: str = ""
    pii: bool = False
    enum: Optional[List[str]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None

@dataclass
class DataContract:
    name: str
    version: str
    owner: str
    description: str
    fields: List[FieldSpec]
    sla_freshness_hours: int = 24
    sla_availability: float = 0.99
    consumers: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, path):
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        fields = [FieldSpec(**f) for f in data.pop("fields", [])]
        return cls(fields=fields, **data)

    def to_dict(self):
        from dataclasses import asdict
        return asdict(self)
