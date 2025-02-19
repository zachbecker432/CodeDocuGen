from util import FunctionDetails
import openai
from typing import List
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def summarize_code(function_details: FunctionDetails, references: List[str]):
    """ Use an LLM to generate summaries and usage examples for C# functions, fields, and classes. """
    
    #reference_text = f"The following files reference this function: {'\n'.join(references)}." if references else "No references found."
    reference_text = f"The following files reference this function: No references found."
    
    system_prompt = f"""
        You are an AI assistant that summarizes C# code elements and generates example usage.
        Below is a {function_details.type} named '{function_details.name}'. Use the provided XML comment and code snippet as context.
    """

    prompt = f"""
        ### XML Comment:
        {function_details.xml_comment}

        ### Code Snippet:
        {function_details.code}
        
        ### Function References:
        {reference_text}
        
        ### Task:
        1. Summarize this {function_details.type}.
        2. If it's a function, generate an example usage snippet based on the Function References, 
            if there are none generate an example based on the XML Comment and the actual function code using your own knowledge.
        
        ### Summary:
        """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes code and generates examples."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content