from dataclasses import dataclass
from typing import Optional, Dict, Any


class Diffable:
    def diff(self, other: "Diffable") -> Dict[str, Any]:
        raise NotImplementedError


@dataclass
class Parameter(Diffable):
    key: str
    value: Any

    def diff(self, other: Optional["Parameter"]) -> Dict[str, Any]:
        if other is None:
            return {"type": "removed", "old": self.value, "new": None}

        if self.value != other.value:
            return {"type": "modified", "old": self.value, "new": other.value}

        return {} 


@dataclass
class Metric(Diffable):
    key: str
    value: float

    def diff(self, other: Optional["Metric"]) -> Dict[str, Any]:
        if other is None:
            return {"type": "removed", "old": self.value, "new": None}

        if self.value != other.value:
            return {"type": "modified", "old": self.value, "new": other.value}

        return {}


@dataclass
class Dataset(Diffable):
    hash: str
    num_rows: int

    def diff(self, other: Optional["Dataset"]) -> Dict[str, Any]:
        if other is None:
            return {"type": "removed", "old": self.hash, "new": None}

        diff = {}
        if self.hash != other.hash:
            diff["hash_changed"] = {"old": self.hash, "new": other.hash}

        if self.num_rows != other.num_rows:
            diff["rows_changed"] = {"old": self.num_rows, "new": other.num_rows}

        if not diff:
            return {}

        return {"type": "modified", **diff}
