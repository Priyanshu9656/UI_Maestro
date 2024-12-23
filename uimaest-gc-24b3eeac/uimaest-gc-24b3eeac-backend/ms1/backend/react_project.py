import subprocess
import threading
from errors.extract_errors import refining_error_query

def analyze_and_rectify_error(error_message):
    """
    Analyzes and attempts to rectify the given error message.

    This function is a placeholder for logic that would analyze the error message
    and take appropriate actions to rectify it.

    Args:
        error_message (str): The error message to be analyzed.
    """

    print(f"Analyzing error: {error_message}")

def start_vite_app(dir, coder):
    """
    Starts a Vite React application and monitors for errors.

    This function initiates a Vite server for a React application located in the specified directory.
    It monitors the server's stderr for specific error patterns, analyzes them, and attempts to resolve
    them using the provided coder.

    Args:
        dir (str): The directory where the React application is located.
        coder: An instance of a coder object used to resolve errors.

    The function uses threading to monitor the stderr stream for errors and processes them in real-time.
    """

    # Command to start the Vite React application
    cmd = 'npx vite --port 3001'
    
    # Start the subprocess
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True, shell=True, cwd=dir)
    
    def monitor_errors(stream):
        """
        Monitors the given stream for errors and processes them.

        Args:
            stream: The stream to monitor for error messages.
        """
        
        errors = ""
        required_error_content = True
        for line in iter(stream.readline, ''):
            if "at constructor" in line:
                required_error_content = False
                analyze_and_rectify_error(errors)
                error_prompt = refining_error_query(errors)
                coder.resolve_error(error_prompt)
                errors = ""
            if "Pre-transform error:" in line or "Internal server error:" in line or "File:" in line:
                required_error_content = True
            if required_error_content:
                errors += line

    # Create a thread to monitor stderr
    stderr_thread = threading.Thread(target=monitor_errors, args=(process.stderr,))
    
    # Start the thread
    stderr_thread.start()
    
    # Wait for the process to complete
    process.wait()
    
    # Wait for the thread to complete
    stderr_thread.join()