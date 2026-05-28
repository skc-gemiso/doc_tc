from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ConvertTask:
    taskId: int
    srcPath: str
    tarPath: str
    callBack: str
    isThumbNail: bool = False
    isCatalog: bool = False
    width: int = 700
    height: int = 500

    @classmethod
    def from_dict(cls, data: dict) -> "ConvertTask":
        return cls(
            taskId=data["taskId"],
            srcPath=data["srcPath"],
            tarPath=data["tarPath"],
            callBack=data["callBack"],
            isThumbNail=data.get("isThumbNail", False),
            isCatalog=data.get("isCatalog", False),
            width=data.get("width", 700),
            height=data.get("height", 500),
        )
