from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# We are using a chat model in Groq
llm = ChatOpenAI(temperature=0, model_name="gpt-4o")

def refining_error_query(log):
    """
    Refines error logs into prompts for GPT models to handle UI-related errors.

    This function takes error logs as input, processes them to generate prompts
    specifically designed for GPT models. The prompts focus on addressing UI-related
    errors found in the logs. If no UI-related errors are detected, the function
    returns a message indicating so.

    Args:
        log (str): The error log to be processed.

    Returns:
        str: A refined prompt or message indicating the absence of UI-related errors.

    The function uses a predefined template to format the error log into a prompt
    and invokes a language model to generate the output.
    """

    template = """
            You are an Expert Prompt engineer. You'll be given error logs, 
            understand the logs properly and generate prompts to give to GPT models. 
            Make sure the prompts handle all the errors occurred in error logs that are related to UI.
            If you don't find error related to UI just say no errors related to UI.
            only give prompts in plain text without headings in separate paragraphs. 
            
            USER_REQUEST: {log}

            PROMPT:  
            """
    promt_template = template
    prompt = promt_template.format(log=log)
    output = llm.invoke(prompt)

    return output.content