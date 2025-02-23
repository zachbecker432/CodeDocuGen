from dataclasses import dataclass
from typing import List
import re

@dataclass
class FunctionDetails:
    name: str
    type: str
    class_name: str
    xml_comment: str
    code: str
    references: List['FunctionDetails']

FUNCTION_PATTERN = re.compile(
            r'^\s*(?:static|public|private|protected|internal|void)'    # Access modifiers
            r'\s+(?:static\s+)?'                                        # Optional static
            r'(?:[\w\<\>\[\]]+\s+)?'                                    # Return type
            r'(?P<name>\w+)'                                            # Function name
            r'\s*\([^)]*\)'                                             # Parameters
            r'\s*(?:\{|;)?'                                             # Opening brace or semicolon
        )