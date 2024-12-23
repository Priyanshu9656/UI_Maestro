from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
import os

class ReactComponentCoder:
    """
    A class to facilitate the development and error resolution of React components using AI models.

    This class provides methods to initialize a coding environment, generate UI components, and resolve
    errors in React applications. It leverages AI models to assist in these tasks.
    """

    def __init__(self, model_name="gpt-4o", weak_model_name="gpt-4-turbo"):
        """
        Initializes the ReactComponentCoder with specified AI models.

        Args:
            model_name (str): The name of the main AI model to use.
            weak_model_name (str): The name of the weaker AI model to use for certain tasks.
        """

        self.io = InputOutput(yes=True)
        self.model = Model(model_name, weak_model=weak_model_name)
        self.coder = None

    def extract_file_paths(self, src):
        """
        Extracts file paths of JSX components from a specified source directory.

        Args:
            src (str): The source directory to search for JSX files.

        Returns:
            list: A list of file paths for JSX components found in the directory.
        """
        
        print(src)
        # Define the images directory
        images_dir = os.path.abspath(os.path.join(src, "images"))
        src = f"{src}/src/Components"
        
        file_paths = []
        file_paths.append("https://picsum.photos/200")
        for root, dirs, files in os.walk(src):
            for file in files:
                if file.split(".")[-1] == "jsx":
                    file_paths.append((root + "/" + file).replace("../", "").replace("\\", "/"))
        
        # Walk through the images directory tree
        print(images_dir,"img dir");
        for root, dirs, files in os.walk(images_dir):
          for file in files:
            if file.split(".")[-1] in ["jpg", "jpeg", "png", "gif", "bmp"]:
                file_paths.append((root + "/" + file).replace("../", "").replace("\\", "/"))
                
        print(file_paths)
        return file_paths

    def init_aider(self, dir):
        """
        Initializes the coding environment with the specified directory.

        Args:
            dir (str): The directory containing the React application.

        This method extracts file paths of JSX components and initializes the Coder with these files.
        """

        fnames = self.extract_file_paths(dir)
        fnames.append(f"{dir}/src/App.jsx")
        print(fnames)

        self.coder = Coder.create(main_model=self.model, io=self.io, fnames=fnames)

    def generate_ui(self, inp, dir):
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
            Use tailwind css for styling , do not use material UI
            For navigation use react-router-dom, like BrowserRouter, Routes and Route.
            If any existing component is being updated, carefully make the required changes and imports in the existing components.
            If you create any new component add that component file in the chat.
            Also import that component in App.jsx.
            Always create new components inside {dir}/src/Components folder.
        """
        query = inp
        input = system1 + query
        self.coder.run(input)

    def resolve_error(self, inp):
        """
        Resolves errors in React code based on the provided error input.

        Args:
            inp (str): The error message or description to be resolved.

        This method uses AI to analyze and resolve errors in React applications.
        """

        system1 = f"""
            You are a smart React js developer who can understand and resolve errors in React js code
            your task is to analyze the error {inp} and perform necessary actions to resolve the error.
        """
        query = inp
        input = system1 + query
        self.coder.run(input)
        
    def clear_history_files(self):
        """ Clear the history files"""
        
        self.coder.run("/reset")
