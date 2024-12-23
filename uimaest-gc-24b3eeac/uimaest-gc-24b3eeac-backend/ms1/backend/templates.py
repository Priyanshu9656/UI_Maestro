import os
import json

def extract_file_paths(relativeSource):
    """
    Extracts file paths and details from JSON files within a specified directory.

    This function traverses the directory tree starting from the given source directory (`src`),
    looking for files named "details.json". It reads each of these JSON files and appends their
    contents to a list.

    Args:
        src (str): The source directory path to start the search from.

    Returns:
        list: A list of dictionaries, where each dictionary contains the data from a "details.json" file.
    """
    src = str(os.path.abspath(relativeSource))
    template_list = []
    for root, dirs, files in os.walk(src):
        for file in files:
            if file == "details.json":
                f = open(root+"\\"+file)
                data = json.load(f)
                f.close()
                template_list.append(data)
    return template_list