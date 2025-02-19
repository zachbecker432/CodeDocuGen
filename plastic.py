import os
import subprocess

def get_latest_main_branch(repo_path):
    """ Fetch the latest code from the main branch of a Plastic SCM repository. """
    os.chdir(repo_path)
    
    # Switch to main branch and update
    subprocess.run(["cm", "switch", "main"], check=True)
    subprocess.run(["cm", "update"], check=True)

    return repo_path  # Returns the directory with the latest code