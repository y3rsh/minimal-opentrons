import os
import shutil
import subprocess
import sys
import venv

def run_command(command, cwd=None):
    print(f"Running command: {' '.join(command)}")
    subprocess.check_call(command, cwd=cwd)

def is_git_repo(path):
    """Check if a directory is a Git repository."""
    try:
        subprocess.check_call(["git", "-C", path, "status"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def on_rm_error(func, path, exc_info):
    """Error handler for `shutil.rmtree`."""
    import stat
    if not os.access(path, os.W_OK):
        # Change the file to be writable (stat.S_IWRITE)
        os.chmod(path, stat.S_IWRITE)
        # Retry the deletion
        func(path)
    else:
        raise

def main(commit_hash):
    repo_url = "https://github.com/Opentrons/opentrons"  # Replace with your repository URL
    repo_name = repo_url.split("/")[-1]

    if os.path.exists(repo_name):
            print(f"Deleting non-git directory '{repo_name}'...")
            shutil.rmtree(repo_name, onerror=on_rm_error)

    print("Cloning the repository...")
    run_command(["git", "clone", repo_url, "--depth", "1", "--branch", commit_hash])

    print(f"Creating a virtual environment named '{commit_hash}'...")
    venv_dir = os.path.join(".venv_", commit_hash)  # Venv directory in the current folder
    venv.create(venv_dir, with_pip=True)

    pip_install_cmd = [os.path.join(venv_dir, "bin", "python"), "-m", "pip", "install", "-U"]

    print("Installing dependencies...")
    run_command(pip_install_cmd + ["./opentrons/shared-data/python"], cwd=repo_name)
    run_command(pip_install_cmd + ["./opentrons/hardware[flex]"], cwd=repo_name)
    run_command(pip_install_cmd + ["./opentrons/api"], cwd=repo_name)
    run_command(pip_install_cmd + ["pandas==1.4.3"], cwd=repo_name)

    print("Setup complete.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <commit_hash>")
        sys.exit(1)
    
    commit_hash = sys.argv[1]
    main(commit_hash)
