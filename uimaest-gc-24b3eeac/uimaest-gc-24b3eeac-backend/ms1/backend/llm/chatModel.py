from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_structured_chat_agent
from llm.transcript import refining_query
from llm.aiderscript import ReactComponentCoder
from langchain.prompts.chat import ChatPromptTemplate
from aider.coders import Coder
# from dotenv import load_dotenv
# from aider.coders import Coder
# load_dotenv()

 
GROQ_LLM = ChatOpenAI(temperature=0, model_name="gpt-4o")
GPT_LLM = ChatOpenAI(temperature=0, model_name="gpt-4o")

def human_response(query):
    """
    Generates a human-like response for non-UI related queries.

    This function provides a brief response indicating that the system can only assist with UI-related tasks.

    Args:
        query (str): The user's query.

    Returns:
        str: A response message indicating the system's UI focus.
    """

    template = """
            You are a UI Buddy.
            User is asking a query. However you can only work as a UI Buddy. Give a meaningful small response in 10 to 30 words responding user query and telling him that you can only work for UI related things.  
            USER_QUERY : 
    """
    return GROQ_LLM.invoke(template + query).content

tools = [
    Tool(
        name="transcript",
        func=refining_query,
        description="Use this tool when there is any keyword in the input related to React js or front-end design",
        return_direct=True,
    ),
    Tool(
        name="Interaction",
        func=human_response,
        description="Use this tool when input has nothing related to React js or front-end design/ development",
        return_direct=True,
    )
]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                    Respond to the human as helpfully and accurately as possible. You have access to the following tools:
                    {tools}
                    Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).
                    Valid "action" values: "Final Answer" or {tool_names}
                    Provide only ONE action per $JSON_BLOB, as shown:
                    ```
                    {{
                      "action": $TOOL_NAME,
                      "action_input": $INPUT
                    }}
                    ```
                    Follow this format:
                    Question: input question to answer
                    Thought: consider previous and subsequent steps
                    Action:
                    ```
                    $JSON_BLOB
                    ```
                    Observation: action result
                    ... (repeat Thought/Action/Observation N times)
                    Thought: I know what to respond
                    Action:
                    ```
                    {{
                      "action": "Final Answer",
                      "action_input": "Final response to human"
                    }}
                    Begin! Reminder to ALWAYS respond with a valid json blob of a single action. 
                    First check the whole input, 
                    if any part input has anything related to frontend UI web developmen Strictly Use transcript toolt. 
                    Only if no part input has nothing related to frontend UI web development, use interaction tool. 
                    Format is Action:```$JSON_BLOB```then Observation
           """,
        ),
        ("human", """{input}
        {agent_scratchpad}
        (reminder to respond in a JSON blob no matter what)"""),
        ("placeholder", "{chat_history}"),
    ]
)

agent = create_structured_chat_agent(GPT_LLM, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

def chatAgent(query: str, coder: ReactComponentCoder, dir):
    """
    Processes a user query to update or generate UI components using AI.

    This function determines whether the query is related to UI development and uses AI to generate or update React components accordingly.

    Args:
        query (str): The user's query.
        coder (ReactComponentCoder): An instance of ReactComponentCoder to handle UI generation.
        dir (str): The directory where the React application is located.

    Returns:
        str: A message indicating the result of the UI update or the response to the query.
    """
    
    def generate_ui(inp, dir):
        """
        Generates or updates UI components based on the provided input.

        Args:
            inp (str): The input or instructions for generating UI components.
            dir (str): The directory where the React application is located.

        This method uses AI to generate or update React components, ensuring proper styling and imports.
        """

        dir = dir.replace("\\", "/")
        system1 = f"""
            You are a smart React js developer
            Use tailwind css for styling , do not use materail UI
            For navigation use react-router-dom, like BrowserRouter, Routes and Route.
            If any existing component is being updated, carefully make the required changes and imports in the existing components.
            If you create any new component add that component file in the chat.
            Also import that component in App.jsx.
            Always create new components inside {dir}/src/Components folder.
        """

        print ("the dir oath  ",dir)
        query = inp
        input = system1 + query
        coder.generate_ui(input, dir)

    def descriptive_user_ui_req(query):
        """
        Provides technical instructions for enhancing UI based on user queries.

        Args:
            query (str): The user's query.

        Returns:
            str: Technical instructions for UI enhancement.
        """
        template = """
                You are a React developer, use your knowledge to determine which components and section could you add to enhance the UI. 
                You need to return all components and instructions needed to create the UI. I will pass your instructions to Aider-chat which will build it for me.
                So, give short technical instructions around 20 to 30 words and don't include code in your response.
                If user is asking to update existing Component, then don't add something new, only add what user is asking.
                USER_QUERY : 
        """
        return GPT_LLM.invoke(template + query).content

    agentResponse = agent_executor.invoke({"input": query})
    agentResponse = agentResponse["output"] 
    agentResponseList = agentResponse.split("\n\n")

    if agentResponseList[0] == "tool":
        for i in range(1, len(agentResponseList)):
            print("***", dir)
            generate_ui(agentResponseList[i], dir)
        return "Your UI has been updated! Please verify."
    else:
        return agentResponse
