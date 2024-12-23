# import shutil
# import zipfile
# import uvicorn
# from fastapi import FastAPI, File, UploadFile, Body
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# import os
# import subprocess
# import json
# import dotenv
# from llm.aiderscript import ReactComponentCoder
# from llm.chatModel import chatAgent
# import threading
# from errors.extract_errors import refining_error_query
# from react_project import start_vite_app
# from templates import extract_file_paths
# import requests
# import logging
# from aider.coders import Coder
# from aider.models import Model


# dotenv.load_dotenv()
# app = FastAPI()
# coder = None
# cnt = 0

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust this to the specific origins you want to allow
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# # @app.post("/uploadfile/")
# # async def create_upload_file(file: UploadFile, dir: str = Body(...)):
# #     """
# #     Endpoint to upload a file and process it using a chat agent.

# #     Args:
# #         file (UploadFile): The file to be uploaded.
# #         dir (str): The directory where the file will be processed.

# #     Returns:
# #         dict: A dictionary containing the response message and status.
# #     """
# #     global coder
# #     if coder is None:
# #         logging.info("Initializing coder in /uploadfile endpoint")
# #         coder = ReactComponentCoder()
# #         coder.init_aider(dir)

# #     content = await file.read()
# #     content_str = content.decode('utf-8')
# #     response = chatAgent(query=content_str, coder=coder, dir=dir)
# #     return {"message": response, "status": True}

# @app.post("/query")
# async def upload_query(query: str = Body(...), dir: str = Body(...)):
#     """
#     Endpoint to process a query using a chat agent.

#     Args:
#         query (str): The query to be processed.
#         dir (str): The directory where the query will be processed.

#     Returns:
#         dict: A dictionary containing the response message and status.
#     """
#     global coder
#     if cnt == 0:
#         logging.info("Initializing coder in /query endpoint")
#         coder = ReactComponentCoder()
#         coder.init_aider(dir)

#     cnt += 1
#     src = str(os.path.abspath(dir))
#     query += "do not use materail ui and styled components for generating the ui"
#     response = chatAgent(query=query, coder=coder, dir=src)
        
#     return {"message": response, "status": True}

# @app.get("/run")
# async def run_react_app(dir: str):
#     """
#     Endpoint to initialize and run a React application.

#     Args:
#         dir (str): The directory of the React application.

#     Returns:
#         dict: A dictionary containing the status and port information.
#     """

#     global coder
#     logging.info("Initializing coder in /run endpoint")
#     coder = ReactComponentCoder()
#     coder.init_aider(dir)
#     src = str(os.path.abspath(dir))
#     # response = requests.get(f"http://127.0.0.1:9999/api/set-dir?dir={src}")
#     # if response.status_code != 200:
#     #     return {"status": False, "error": "Failed to set directory"}
#     os.system("FOR /F \"tokens=5\" %a IN ('netstat -aon ^| find \":3001\" ^| find \"LISTENING\"') DO taskkill /f /pid %a")
#     threading.Thread(target=start_vite_app, args=(dir, coder)).start()
#     return {"status": True, "PORT": 3001}

# @app.post("/upload-image/")
# async def upload_image(file: UploadFile = File(...)):
    
#     if file.content_type not in ["image/jpeg", "image/png"]:
#         raise HTTPException(status_code=400, detail="File must be a JPEG or PNG image")

#     file_location = f"../templates/images/{file.filename}"
#     with open(file_location, "wb") as f:
#         f.write(await file.read())
    
#     return {"info": f"file '{file.filename}' saved at '{file_location}'"}


# # @app.get("/templates")
# # async def get_template():
# #     """
# #     Endpoint to retrieve available templates.

# #     Returns:
# #         list: A list of file paths for available templates.
# #     """

# #     templates = extract_file_paths(os.path.dirname(os.path.abspath(__file__))+"\\..\\templates\\src\\user_templates")
# #     return templates


# # @app.post("/upload_project")
# # async def upload_folder(zip_file: UploadFile = File(...), project_name: str = Body(...), project_desc: str = Body(...)):
# #     """
# #     Endpoint to upload a project folder in zip format.

# #     Args:
# #         zip_file (UploadFile): The zip file containing the project.
# #         project_name (str): The name of the project.
# #         project_desc (str): The description of the project.

# #     Returns:
# #         dict: A dictionary containing the message and status of the upload.
# #     """

# #     if zip_file.filename.endswith(".zip") and zip_file.file.read(1024 * 25 * 1024) is not None:
# #         temp_dir = os.path.join(os.getcwd(), "temp")
# #         os.makedirs(temp_dir, exist_ok=True)
# #         with zipfile.ZipFile(zip_file.file, 'r') as zip_ref:
# #             zip_ref.extractall(temp_dir)
# #         folder_dir = os.path.join(os.getcwd(), f"temp/{zip_file.filename[:len(zip_file.filename)-4]}")
# #         templates_dir = os.path.join(os.getcwd(), "../", "templates", "src", "user_templates")
# #         os.makedirs(templates_dir, exist_ok=True)
# #         try:
# #             shutil.move(folder_dir, templates_dir)
# #         except:
# #             return {"error": f"Folder name with same name already exists!", "status": False}
# #         json_desc = {
# #             "name": project_name,   
# #             "description": project_desc, 
# #             "dir": f"..\\templates\\src\\user_templates\\{zip_file.filename[:len(zip_file.filename)-4]}", 
# #             "image": "https://us-tuna-sounds-images.voicemod.net/d907fb84-bc33-4801-960f-4d4db01c0ed5-1670526673405.png"
# #         }
# #         with open(f"..\\templates\\src\\user_templates\\{zip_file.filename[:len(zip_file.filename)-4]}\\details.json", "w") as f:
# #             json.dump(json_desc, f, indent=4)
# #         return {"message": f"Project uploaded", "status": True}
# #     else:
# #         return {"error": "Invalid zip file or exceeds 25MB size limit", "status": False}

# @app.post("/new_project")
# async def new_react_app(project_name: str = Body(...), project_desc: str = Body(...)):
#     """
#     Endpoint to create a new React application.

#     Args:
#         project_name (str): The name of the new project.
#         project_desc (str): The description of the new project.

#     Returns:
#         dict: A dictionary containing the status and message of the creation.
#     """

#     os.system(f"xcopy /s /e /y /i template_folder\\new_project ..\\templates\\src\\user_templates\\{project_name}")
#     json_desc = {
#         "name": project_name, 
#         "description": project_desc, 
#         "dir": f"..\\templates\\src\\user_templates\\{project_name}", 
#         "image": "https://us-tuna-sounds-images.voicemod.net/d907fb84-bc33-4801-960f-4d4db01c0ed5-1670526673405.png"
#     }
#     with open(f"{json_desc['dir']}\\details.json", "w") as f:
#         json.dump(json_desc, f, indent=4)
#     with open(f"{json_desc['dir']}\\package.json", "r+") as f:
#         packageJson = json.loads(f.read())
#         packageJson["name"] = project_name
#         f.seek(0)
#         f.truncate()
#         json.dump(packageJson, f, indent=4)
    
#     # Initialize coder if not already initialized
#     cnt = 0
#     global coder
#     if coder is None:
#         coder = ReactComponentCoder()
#         coder.init_aider(json_desc['dir'])

#     # Ensure coder is properly initialized before calling clear_history_files
#     if coder is not None:
#         coder.clear_history_files()
#     else:
#         return {"Status": False, "Message": "Failed to initialize coder"}

#     # git_intilisation = execute_git_commands(json_desc['dir'])
#     # if git_intilisation['status'] == "error":
#     #     return git_intilisation
#     return {"Status": True, "Message": "New Project Added!"}

# # --------------------------------- Git Api's and functions ------------------------------

# # TODO: Complete the function by uncommenting and configuring the necessary git commands.
# #       - Add the remote repository URL to the 'git remote add origin' command.
# #       - Ensure the branch name is dynamically set if needed, especially for fetch and push operations.
# #       - Consider adding error handling for specific git operations to provide more detailed feedback.
# #       - Uncomment 'git status' if you want to check the status before committing.
# #       - Uncomment and configure 'git fetch', 'git rebase', and 'git push' commands as per the workflow requirements.

branch = "uiMaestro-branch"

def execute_git_commands(dir):
    """
    Execute a series of git commands in the specified directory.

    Args:
        dir (str): The directory where the git commands will be executed.

    Returns:
        dict: A dictionary containing the status and message of the execution.
    """
     
    commands = [
        ['git', 'init'],
        # ['git', 'remote', 'add', 'origin', repository],
        ['git', 'checkout', '-b', branch],
        ['git', 'add', '.'],
        # ['git', 'status'],
        ['git', 'commit', '-m', 'intialcommit'],
        # # ['git', 'fetch', 'origin', request.branch_name],
        # # ['git', 'rebase', '-X', 'theirs', f'origin/{request.branch_name}'],
        # ['git', 'push', 'origin', request.branch_name],
    ]

    try:
        for command in commands:
            subprocess.run(command, cwd=dir, check=True, text=True)
        return {"status": "success", "message": "Git commands executed successfully."}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}

# # @app.post("/gitpush")
# # def execute_git_push(dir, repository):
# #     """
# #     Execute git push command to push changes to a remote repository.

# #     Args:
# #         dir (str): The directory where the git commands will be executed.
# #         repository (str): The remote repository URL.

# #     Returns:
# #         dict: A dictionary containing the status and message of the execution.
# #     """

# #     response = show_origin(dir)
# #     commands = []
# #     if response['status']:
# #         commands = [['git', 'push', 'origin', branch]]
# #     else:
# #         commands = [['git', 'remote', 'add', 'origin', repository],
# #                     ['git', 'push', 'origin', branch]]
# #     try:
# #         for command in commands:
# #             subprocess.run(command, cwd=dir, check=True, text=True)
# #         return {"status": "success", "message": "Git commands executed successfully."}
# #     except subprocess.CalledProcessError as e:
# #         return {"status": "error", "message": str(e)}

# # def show_origin(dir):
# #     """
# #     Show the remote origin of the git repository in the specified directory.

# #     Args:
# #         dir (str): The directory where the git command will be executed.

# #     Returns:
# #         dict: A dictionary containing the status and message of the execution.
# #     """

# #     commands = [['git', 'remote', 'show', 'origin']]
# #     try:
# #         for command in commands:
# #             subprocess.run(command, cwd=dir, check=True, text=True)
# #         return {"status": True, "message": "Git commands executed successfully."}
# #     except subprocess.CalledProcessError as e:
# #         return {"status": False, "message": str(e)}

# # # # ---------------------------------Error Handling --------------------------------------

# # class ErrorLog(BaseModel):
# #     error: str
# #     errorInfo: str = None

# # @app.post("/log-error")
# # async def log_error(error_log: ErrorLog):
# #     """
# #     Endpoint to log and handle runtime errors.

# #     Args:
# #         error_log (ErrorLog): The error log containing error details.

# #     Returns:
# #         dict: A dictionary containing the message indicating error handling.
# #     """

# #     error_prompt = refining_error_query(error_log)
# #     print(error_prompt)
# #     coder.resolve_error(error_prompt)
# #     return {"message": "Runtime error handled"}


# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)


import shutil
import zipfile
import uvicorn
from fastapi import FastAPI, File, UploadFile, Body, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess
import json
import dotenv
from llm.aiderscript import ReactComponentCoder
from llm.aiderscript2 import ReactComponentCoder2
from llm.chatModel import chatAgent
from llm.chatModel2 import chatAgent2
import threading
from errors.extract_errors import refining_error_query
from react_project import start_vite_app
from templates import extract_file_paths
import requests
import logging
from aider.coders import Coder
from aider.models import Model

dotenv.load_dotenv()
app = FastAPI()
coder = None
cnt = 0

# Configure logging
logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/query")
async def upload_query(query: str = Body(...), dir: str = Body(...)):
    """
    Endpoint to process a query using a chat agent.

    Args:
        query (str): The query to be processed.
        dir (str): The directory where the query will be processed.

    Returns:
        dict: A dictionary containing the response message and status.
    """
    global coder
    global cnt  # Declare cnt as global to modify it within the function
    cnt = 0
    dir = "..//templates//src//user_templates//" + dir

    if cnt == 0:
        logging.info("Initializing coder in /query endpoint")
        coder = ReactComponentCoder()
        coder.init_aider(dir)

    cnt += 1
    src = str(os.path.abspath(dir))
    query += "do not use materail ui and styled components for generating the ui"
    response = chatAgent(query=query, coder=coder, dir=src)
    
    return {"message": response, "status": True}

@app.get("/run")
async def run_react_app(dir: str):
    """
    Endpoint to initialize and run a React application.

    Args:
        dir (str): The directory of the React application.

    Returns:
        dict: A dictionary containing the status and port information.
    """
    dir = "..//templates//src//user_templates//" + dir
    global coder
    logging.info("Initializing coder in /run endpoint")
    coder = ReactComponentCoder()
    coder.init_aider(dir)
    src = str(os.path.abspath(dir))
    os.system("FOR /F \"tokens=5\" %a IN ('netstat -aon ^| find \":3001\" ^| find \"LISTENING\"') DO taskkill /f /pid %a")
    threading.Thread(target=start_vite_app, args=(dir, coder)).start()
    return {"status": True, "PORT": 3001}

@app.post("/upload-image/{project_name}")
async def upload_image(project_name:str,file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="File must be a JPEG or PNG image")

    global cnt  # Declare cnt as global to modify it within the function
    cnt = 0
    
    directory_path = f"../templates/src/user_templates/{project_name}/images"
    
    os.makedirs(directory_path, exist_ok=True)
    file_location = os.path.join(directory_path, file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}


@app.delete("/delete-image/{project_name}/{image_name}")
async def delete_image(project_name: str, image_name: str):
    """
    Endpoint to delete an image by its name within a specific project.

    Args:
        project_name (str): The name of the project.
        image_name (str): The name of the image to be deleted.

    Returns:
        dict: A dictionary containing the status of the deletion.
    """
    file_location = f"../templates/src/user_templates/{project_name}/images/{image_name}"
    if os.path.exists(file_location):
        os.remove(file_location)
        return {"status": "success", "message": f"Image '{image_name}' deleted successfully from project '{project_name}'."}
    else:
        raise HTTPException(status_code=404, detail="Image not found")
    
@app.get("/projects")
async def get_projects():
    """
    Endpoint to retrieve available templates.

    Returns:
        list: A list of file paths for available templates.
    """

    templates = extract_file_paths(os.path.dirname(os.path.abspath(__file__))+"\\..\\templates\\src\\user_templates")
    return templates


@app.post("/new_project")
async def new_react_app(project_name: str = Body(...), project_desc: str = Body(...)):
    """
    Endpoint to create a new React application.

    Args:
        project_name (str): The name of the new project.
        project_desc (str): The description of the new project.

    Returns:
        dict: A dictionary containing the status and message of the creation.
    """
    
    project_dir = f"..\\templates\\src\\user_templates\\{project_name}"

    if os.path.exists(project_dir):
        raise HTTPException(status_code=400, detail="Project with the same name already exists!")
    
    
    os.system(f"xcopy /s /e /y /i template_folder\\new_project ..\\templates\\src\\user_templates\\{project_name}")
    json_desc = {
        "name": project_name, 
        "description": project_desc, 
        "dir": f"..\\templates\\src\\user_templates\\{project_name}", 
        "image": "https://us-tuna-sounds-images.voicemod.net/d907fb84-bc33-4801-960f-4d4db01c0ed5-1670526673405.png"
    }
    with open(f"{json_desc['dir']}\\details.json", "w") as f:
        json.dump(json_desc, f, indent=4)
    with open(f"{json_desc['dir']}\\package.json", "r+") as f:
        packageJson = json.loads(f.read())
        packageJson["name"] = project_name
        f.seek(0)
        f.truncate()
        json.dump(packageJson, f, indent=4)
    
    # Initialize coder if not already initialized
    global cnt
    cnt = 0
    global coder
    if coder is None:
        coder = ReactComponentCoder()
        coder.init_aider(json_desc['dir'])

    # Ensure coder is properly initialized before calling clear_history_files
    if coder is not None:
        coder.clear_history_files()
    else:
        return {"Status": False, "Message": "Failed to initialize coder"}
    
    git_intilisation = execute_git_commands(json_desc['dir'])
    if git_intilisation['status'] == "error":
         return git_intilisation
    return {"Status": True, "Message": "New Project Added!"}

import stat
import time

def remove_readonly(func, path, exc_info):
    """
    Clear the readonly bit and reattempt the removal.
    """
    os.chmod(path, stat.S_IWRITE)
    try:
        func(path)
    except PermissionError:
        time.sleep(1)  # Wait for 1 second before retrying
        func(path)

@app.delete("/delete-project/{project_name}")
async def delete_project(project_name: str):
    """
    Endpoint to delete a project by its name.

    Args:
        project_name (str): The name of the project to be deleted.

    Returns:
        dict: A dictionary containing the status of the deletion.
    """
    os.system(f"FOR /F \"tokens=5\" %a IN ('netstat -aon ^| find \":3001\" ^| find \"LISTENING\"') DO taskkill /f /pid %a")

    project_dir = os.path.join("..", "templates", "src", "user_templates", project_name)

    if os.path.exists(project_dir) and os.path.isdir(project_dir):
        shutil.rmtree(project_dir, onerror=remove_readonly)
        return {"status": "success", "message": f"Project '{project_name}' deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Project not found")


from fastapi.responses import StreamingResponse
@app.get("/download-project/{project_name}")
async def download_project(project_name: str):
    """
    Endpoint to download a project as a zip file.

    Args:
        project_name (str): The name of the project to be downloaded.

    Returns:
        StreamingResponse: A streaming response with the zip file.
    """
    project_dir = os.path.join("..", "templates", "src", "user_templates", project_name)

    if not os.path.exists(project_dir) or not os.path.isdir(project_dir):
        raise HTTPException(status_code=404, detail="Project not found")

    zip_filename = f"{project_name}.zip"
    zip_filepath = os.path.join("..", "templates", "src", "user_templates", zip_filename)


    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.join(project_dir, '..'))
                zipf.write(file_path, arcname)

    def iterfile():
        with open(zip_filepath, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="application/zip", headers={"Content-Disposition": f"attachment; filename={zip_filename}"})

@app.get("/stop-project")
async def stop_project():
    """
    Endpoint to stop the project running on port 3001.

    Returns:
        dict: A dictionary containing the status of the operation.
    """
    try:
        # Command to find and kill the process running on port 3001
        os.system("FOR /F \"tokens=5\" %a IN ('netstat -aon ^| find \":3001\" ^| find \"LISTENING\"') DO taskkill /f /pid %a")
        return {"status": "success", "message": "Project stopped successfully on port 3001."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop project: {str(e)}")
    
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from transformers import GPT2Tokenizer
from langchain_openai import ChatOpenAI
import aiofiles
 
GPT_LLM = ChatOpenAI(temperature=0, model_name="gpt-4o")
 
# Initialize the tokenizer (using GPT-2 tokenizer as an example)
tokenizer = GPT2Tokenizer.from_pretrained("openai-community/gpt2")
 
class PromptInput(BaseModel):
    prompt: str
 
async def read_text_file(file_path):
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            return await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {e}")
   
def summarize_text(text):
    try:
        response = GPT_LLM.invoke(f"Summarize the following text:\n\n{text} keep the code part in the summary")
        summary = response.content.strip()  # Accessing the content of the AIMessage object
        return summary
    except Exception as e:
        logging.error(f"Error summarizing text: {e}")
        raise HTTPException(status_code=500, detail=f"Error summarizing text: {e}")
 
def generate_code_from_summary(summary, user_prompt):
    response = GPT_LLM.invoke(f"Generate a react app for the user promt : \n\n{user_prompt} and use following summary for styling:\n\nSummary: {summary}").content
    # code = response.choices[0].message['content'].strip()
    # return code
    code = response
    return code
 
async def chunk_text_by_tokens(text, max_tokens):
    try:
        tokens = tokenizer.tokenize(text)
        print(len(tokens))
        chunks = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]
        return [" ".join(chunk) for chunk in chunks]
    except Exception as e:
        logging.error(f"Error chunking text: {e}")
        raise HTTPException(status_code=500, detail=f"Error chunking text: {e}")
 
def rectify_info(text):
      response = GPT_LLM.invoke(f"""this {text} is chunk of component library
                                You are provided with a text file that contains detailed information about the implementation and usage of a CSS library. Your task is to extract only the information related to how to use different components of the library. The extracted documentation should include:
                                1.) Component Name: The name of the component.
                                2.) Usage Instructions: Step-by-step instructions on how to use the component.
                                3.) Examples: Code examples demonstrating the usage of the component.
                               
                                As i am making documentation of the library i do not care about it's implementation
                                so if the current chunk have uneccessary information
                                please return empty string""")
    #   print(response)
      return response
 
@app.post("/process-file")
async def process_file(prompt_input: PromptInput):
   
    file_path = 'industrial-ui.txt'
    try:
        text = await read_text_file(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
   
    # Step 1: Preprocess and Chunk the Text
    max_tokens =  50000  # Set chunk size to the model's max token limit
    chunks = await chunk_text_by_tokens(text, max_tokens)
   
    # docs = [rectify_info(chunk) for chunk in chunks]
   
    output_file_path = 'industrial-ui-docs.txt'
    async with aiofiles.open(output_file_path, 'w' , encoding='utf-8') as file:
        for chunk in chunks:
            doc = rectify_info(chunk)
            await file.write(doc.content + '\n')  # Write each document followed by a newline
   
 
    # # Step 2: Summarize Each Chunk
    # chunk_summaries = [summarize_text(chunk) for chunk in chunks]
 
    # # Step 3: Generate a Higher-Level Summary
    # higher_level_summary = summarize_text(" ".join(chunk_summaries))
 
    # # Step 4: Generate Code Based on the Higher-Level Summary and User Prompt
    # generated_code = generate_code_from_summary(higher_level_summary, prompt_input.prompt)
 
    return {
        # 'higher_level_summary': higher_level_summary,
        # 'generated_code': generated_code
    }
   
class UserPrompt(BaseModel):
    prompt: str
    
@app.delete("/delete-doc/{project_name}/{doc_name}")
async def delete_doc(project_name: str, doc_name: str):
    """
    Endpoint to delete a document by its name within a specific project.

    Args:
        project_name (str): The name of the project.
        doc_name (str): The name of the document to be deleted.

    Returns:
        dict: A dictionary containing the status of the deletion.
    """
    file_location = f"../templates/src/user_templates/{project_name}/docs/{doc_name}"
    if os.path.exists(file_location):
        os.remove(file_location)
        return {"status": "success", "message": f"Document '{doc_name}' deleted successfully from project '{project_name}'."}
    else:
        raise HTTPException(status_code=404, detail="Document not found")
    
@app.get("/get-docs/{project_name}")
async def get_docs(project_name: str):
    """
    Endpoint to retrieve documents within a specific project.

    Args:
        project_name (str): The name of the project.

    Returns:
        dict: A dictionary containing the list of documents or an error message.
    """
    directory_path = f"../templates/src/user_templates/{project_name}/docs"
    
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        raise HTTPException(status_code=404, detail="Document folder not found")
    
    docs = os.listdir(directory_path)
    if not docs:
        raise HTTPException(status_code=404, detail="No documents found in the folder")
    
    return {"documents": docs}
   
@app.post("/upload-doc/{project_name}")
async def upload_doc(project_name: str, file: UploadFile = File(...)):
    if file.content_type not in ["text/plain", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="File must be a TXT or DOC/DOCX document")

    directory_path = f"../templates/src/user_templates/{project_name}/docs"
    os.makedirs(directory_path, exist_ok=True)
    
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
    file_location = os.path.join(directory_path, file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    return {"info": f"file '{file.filename}' saved at '{file_location}'"}


@app.post("/process-prompt/{project_name}")
async def process_prompt(project_name: str,user_prompt:str = Body(...),dir: str = Body(...)):
       
        # Combine the user prompt and the CSS library documentation
    dir = "..//templates//src//user_templates//" + dir
    global coder
    global cnt 
    cnt = 0
    if coder is None:
        logging.info("Initializing coder in /query endpoint")
        coder = ReactComponentCoder2()
        coder.init_aider(dir)
    elif cnt == 0:
        logging.info("Initializing coder in /query endpoint")
        coder = ReactComponentCoder2()
        coder.init_aider(dir)
 
    src = str(os.path.abspath(dir))
    docs_folder_path = f'../templates/src/user_templates/{project_name}/docs/'
    doc_file = next((f for f in os.listdir(docs_folder_path) if os.path.isfile(os.path.join(docs_folder_path, f))), None)
    print(doc_file,"doc")
    response = chatAgent2(query=user_prompt, coder=coder, dir=src,docs=doc_file)
       
    return {"message": response, "status": True}
 
 
class ErrorMessage(BaseModel):
    error: str
 
@app.post("/resolve-error/")
async def resolve_error(error_message: ErrorMessage):
    try:
        # Read the CSS library documentation from a text file
        async with aiofiles.open('docs.txt', mode='r', encoding='utf-8') as file:
            docs = await file.read()
       
        # Combine the error message and the CSS library documentation
        combined_prompt = f"CSS Library Documentation:\n{docs}\n\nError Message:\n{error_message.error}\n\n resolve this error using the "
 
        # Pass the combined prompt to the OpenAI API
        response = GPT_LLM.invoke(combined_prompt)
 
        # Extract the resolution from the response
        resolution = response
 
        return {"error": error_message.error, "resolution": resolution}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
