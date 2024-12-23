from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
llm2 = ChatOpenAI(temperature=0, model_name="gpt-4o")

template = """
    You are a professional web developer in React js. Your task is to divide a task related to React development into smaller, manageable and independent subtasks. 
    I have a complex task that I need to complete. Please help me divide this task into smaller, manageable sub-tasks. The sub-tasks should cover all necessary aspects from planning to implementation. Here is an example of how a task could be divided into sub-tasks:
    divide the task strictly into 3 sub tasks, the first sub task will give the structure of the task. Second sub task will give the functionality and content of the task. and third task will give proper styling and design to the task.
    **Example Task: Create a Navigation Bar for a Website**

    1. Create the react structure of Nav bar.
    2. Add sections and menu items, Integrate links and interactions.
    3. Style the navigation bar with tailwind css according to the image in the chat, make the navigation bar responsive, add interactive elements using JavaScript.

    Using this format as a guide, please provide a detailed breakdown of each step required to complete my task.

    only give the three subtasks in three paragraphs without and headings or special characters.
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages(messages=[system_message_prompt, human_message_prompt])
chain = chat_prompt | llm2

def primaryTasks(requirement: str):
    """
    Divides a complex React development task into smaller, manageable subtasks.

    This function uses a language model to break down a given task into three subtasks:
    1. Structure of the task.
    2. Functionality and content of the task.
    3. Styling and design of the task.

    Args:
        requirement (str): The complex task description that needs to be divided.

    Returns:
        list: A list of strings, each representing a subtask.
    """

    output = chain.invoke({
        "text": requirement,
    })
    primaryRequirements = output.content.split('\n\n')

    return primaryRequirements