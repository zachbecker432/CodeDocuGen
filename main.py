import os
from typing import List
from code_parser import CSharpParser
from llm_summarizer import summarize_code

if __name__ == "__main__":
    parser = CSharpParser()
    solution_dir = "csharp-testdata-mini"
    
    # Check if the solution directory exists
    if not os.path.exists(solution_dir):
        raise FileNotFoundError(f"Solution directory '{solution_dir}' does not exist")
        
    solution_dict = {}
    # Get all C# files in the solution directory    
    cs_files = [(root, f) for root, _, files in os.walk(solution_dir) 
                for f in files if f.endswith('.cs')]
    
    for root, file in cs_files:
        filepath = os.path.join(root, file)
        file_name, _ = os.path.splitext(file)
        file_functions = parser.parse_cs_file(filepath)
        rel_path = os.path.relpath(filepath, solution_dir)
        # Process each function with the LLM
        llm_responses = []
        for function in file_functions:
            # Get references to this function from other files
            references = List[str]  # TODO: Implement reference finding
            
            # Generate LLM summary and examples
            llm_response = summarize_code(
                function,
                references
            )
            llm_responses.append(llm_response)
        
        # Store responses in solution dictionary
        solution_dict[rel_path] = llm_responses

    for file, responses in solution_dict.items():
        print(f"File: {file}")
        for response in responses:
            print(f"Response: {response}")
            print("-"*100)


