import re
from typing import List, Dict, Tuple
from util import FunctionDetails

class CSharpParser:
    def _extract_function_block(self, lines: List[str], start_index: int) -> Tuple[List[str], int]:
        """
        Extract a complete function block by tracking brace matching.
        
        Args:
            lines: List of code lines
            start_index: Starting line index of the function
            
        Returns:
            Tuple containing the function lines and ending index
        """
        function_lines = []
        brace_count = 0
        started = False

        for i, line in enumerate(lines[start_index:], start=start_index):
            if '{' in line:
                brace_count += line.count('{')
                started = True
            if '}' in line:
                brace_count -= line.count('}')
                
            function_lines.append(line)
            
            if started and brace_count <= 0:
                return function_lines, i + 1
                
        return function_lines, len(lines)

    def parse_cs_file(self, filepath: str) -> Dict[str, FunctionDetails]:
        """
        Parse a C# file to extract functions and their XML documentation.
        
        Args:
            filepath: Path to the C# file
            
        Returns:
            Dictionary mapping function names to their details
        """
        FUNCTION_PATTERN = re.compile(
            r'^\s*(?:static|public|private|protected|internal|void)'    # Access modifiers
            r'\s+(?:static\s+)?'                                        # Optional static
            r'(?:[\w\<\>\[\]]+\s+)?'                                    # Return type
            r'(?P<name>\w+)'                                            # Function name
            r'\s*\([^)]*\)'                                             # Parameters
            r'\s*(?:\{|;)?'                                             # Opening brace or semicolon
        )
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        functions = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            if match := FUNCTION_PATTERN.search(line):
                function_name = match.group("name")
                
                # Get XML comments
                xml_lines = []
                for j in range(i-1, -1, -1):
                    if not lines[j].strip().startswith("///"):
                        break
                    xml_lines.insert(0, lines[j].strip())
                
                # Get function implementation
                function_block, i = self._extract_function_block(lines, i)
                
                function_details = FunctionDetails(
                    name=function_name,
                    type="function",
                    xml_comment="\n".join(xml_lines),
                    code="".join(function_block)
                )
                
                functions.append(function_details)
                
                self.print_function_details(function_name, function_details)
            else:
                i += 1
                
        return functions

    def print_function_details(self, function_name: str, function_details: FunctionDetails) -> None:
        """
        Pretty prints the extracted function details from C# files.
        """
        print(f"\nFunction: {function_name}")
        if function_details.xml_comment:
            print("\nXML Comment:")
            print(function_details.xml_comment)
        print("\nCode:")
        print(function_details.code)
        print('-'*30)