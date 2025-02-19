from dataclasses import dataclass

@dataclass
class FunctionDetails:
    name: str
    type: str
    xml_comment: str
    code: str