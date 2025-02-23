import re
from typing import List, Dict, Tuple
from util import FunctionDetails, FUNCTION_PATTERN

class CSharpParser:
    def _extract_function_block(self, lines: List[str], start_index: int) -> Tuple[List[str], List[str]]:
        """
        Extract a complete function block by tracking brace matching and detect function calls.
        
        Args:
            lines: List of code lines
            start_index: Starting line index of the function
            
        Returns:
            Tuple containing:
                - List of function block lines
                - List of function calls found within the block
        """
        function_block = []
        function_calls = []
        brace_count = 0
        started = False

        # Pattern to match function calls - matches word followed by opening parenthesis
        call_pattern = re.compile(r'(\w+)\s*\(')

        for i, line in enumerate(lines[start_index:], start=start_index):
            if '{' in line:
                brace_count += line.count('{')
                started = True
            if '}' in line:
                brace_count -= line.count('}')
                
            function_block.append(line)
            
            # Find function calls in this line
            if calls := call_pattern.findall(line):
                # Filter out control flow keywords
                filtered_calls = [call for call in calls 
                                if call not in ('if', 'for', 'while', 'switch', 'catch')]
                function_calls.extend(filtered_calls)
            
            if started and brace_count <= 0:
                break
                
        return function_block, list(set(function_calls))
    
    def parse_files(self, filepaths: List[str]) -> Dict[str, List[FunctionDetails]]:
        """
        Parse multiple C# files and extract functions with their documentation.
        
        Args:
            filepaths: List of paths to C# files to parse
            
        Returns:
            Dictionary mapping filenames to lists of function details
        """
        parsed_files = {}
        for filepath in filepaths:
            functions = self.parse_cs_file(filepath)
            # Extract just the filename without path
            filename = filepath.split('.')[0]
            parsed_files[filename] = functions
            
        return parsed_files

    def parse_cs_file(self, filepath: str) -> List[FunctionDetails]:
        """
        Parse a C# file to extract functions and their XML documentation.
        
        Args:
            filepath: Path to the C# file
            
        Returns:
            Dictionary mapping function names to their details
        """
        
        
        class_name = filepath.split('.')[0]
        functions = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Find all function matches in the file
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not (match := FUNCTION_PATTERN.search(line)):
                continue
                
            # Get XML comments by looking backwards
            xml_lines = []
            for comment_line in reversed(lines[:line_num]):
                if not comment_line.strip().startswith("///"):
                    break
                xml_lines.insert(0, comment_line.strip())
            
            # Get function implementation
            function_block, function_calls = self._extract_function_block(lines, line_num)
            
            # TODO: Get references to the function calls

            # Create and store function details
            function = FunctionDetails(
                name=match.group("name"),
                type="function",
                class_name=class_name, 
                xml_comment="\n".join(xml_lines),
                code="".join(function_block),
                references=[]
            )
            functions.append(function)
            
            self.print_function_details(match.group("name"), function)
                
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