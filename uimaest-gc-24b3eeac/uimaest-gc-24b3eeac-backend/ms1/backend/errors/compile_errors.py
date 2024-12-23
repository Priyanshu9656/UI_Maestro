from fastapi import FastAPI
import subprocess

app = FastAPI()

def error_handling_function(dir):
    """
    Starts a Vite server and logs compile-time errors to a file.

    This function initiates a Vite server for a React application located in the specified directory.
    It captures the server's output, including any compile-time errors, and writes them to a file named
    'compile_time_errors.txt'.

    Args:
        dir (str): The directory where the React application is located.

    The function merges stderr with stdout to capture all output and logs it line by line.
    """

    # Open a file to write the errors
    with open('compile_time_errors.txt', 'w', buffering=1) as log_file:
        # Start the Vite server process
        process = subprocess.Popen(
            ['npx', 'vite', '--port', '3001'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge stderr with stdout
            text=True,
            shell=True,
            cwd=dir
        )

        # Read and log the output line by line
        for line in process.stdout:
            log_file.write(line + '\n')

        # Wait for the process to complete and get the exit code
        process.wait()
        log_file.write(f'\nVite process exited with code {process.returncode}\n')